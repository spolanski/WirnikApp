# -*- coding: utf-8 -*-
"""
Plik *senderClass.py* zawiera klasy, dzięki którym możliwe jest stworzenie obiektu Gońca zawierającego informacje o analizowanej geometrii. Co więcej dzięki klasie SenderBrain aplikacja będzie potrafiła łączyć się z GMSH'em, oraz Calculix'em.
"""
import subprocess
import os, sys

class SenderBrain(object):
    """
    Klasa odpowiedzialna za przesyłanie poleceń do GMSHa i Calculixa, oraz odbieranie sygnałów zwrotnych z tych programów. Klasa wykorzystuje **subprocess** do komunikowania się z programami zewnętrznymi. Aby zdefiniować obiekt tej klasy *Goniec* powinien zawierać informację o nazwie analizowanego obiektu, oraz ścieżki dostępu do programów GMSH i Calculix.

    :param Sender: obiekt Gońca
    :type Sender: Sender
    """
    
    def __init__(self,Sender):
        """Konstruktor klasy tworzącej obiekt pozwalający na komunikacje z 
        oprogramowaniem zewnętrznym.
        
        :param Sender: obiekt Gońca
        :type Sender: Sender
        """
        # Zdefiniuj analizowany obiekt
        self.part = Sender.Info['Obiekt']
        # Zdefiniuj nazwe analizowanego obiektu
        self.nazwa = self.part['nazwa']
        # Zdefiniuj polozenie GMSH'a
        self.gmsh = Sender.Info['GMSH_DIR']
        # Zdefiniuj polozenie Calculixa (solver)
        self.ccx_dir = Sender.Info['CCX_DIR']
        # Zdefiniuj polozenie Calculix Graphics
        self.cgx_dir = Sender.Info['CGX_DIR']
        # Zdefiniuj folder roboczy
        self.wd = os.getcwd()
        
        # Zdefiniuj platforme operacyjna
        if sys.platform == 'linux' or sys.platform == 'linux2':
            self.SHELL = True
        elif sys.platform == 'win32':
            self.SHELL = False  
        
    def wyslijKomende(self,komenda,output=True):
        """
        Metoda dzięki, której możliwe jest przesyłanie wiadomosci do oprogramowania i odbieranie sygnałów zwrotnych. W celu osiągnięcia tego celu wykorzystany został moduł subprocess.

        :param komenda: komenda jaką użytkownik chciałby uruchomić za pomocą linii kommend danego systemu operacyjnego.
        :type komena: string
        :param output: zmienna, dzięki której możliwe jest wyświetlenie sygnału zwrotnego z programu, z którym aplikacja WirnikApp się łączy.
        :type output: bool
        """
        
        lines = []
        p = subprocess.Popen(komenda, bufsize=1, stdin=open(os.devnull),
                             shell=self.SHELL,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        if output:
            for line in iter(p.stdout.readline, ''):
                print line,
                lines.append(line)
            p.stdout.close()
            p.wait()

        return True
    
    def utworzGeometrie(self, pokazGmsh = True):
        """
        Metoda dzięki, której tworzona jest geometria. Wykonuje ona dwie czynności. Wpierw zostaje stworzony plik *.geo* na podstawie definicji określonej w obiekcie :class:`Geometry` zaimplementowanym w Gońcu. Następnie geometria zostaje zdefiniowana w programie GMSH.

        :param pokazGmsh: zmienna określająca czy GMSH powinien zostać wyświetlony na ekranie
        :type pokazGmsh: bool

        """
        
        # Stworz plik wsadowy .geo
        with open(self.nazwa + '.geo','w') as f:
            f.write(self.part['txt'])

        if pokazGmsh == False:
            cmd = '{0} {1} -0'
        else:
            cmd = '{0} {1}'
        
        print cmd
        cmd = cmd.format(self.gmsh,self.nazwa+'.geo')
        # Wyslij plik wsadowy do GMSH'a
        tworzGeometrie = self.wyslijKomende(cmd)
        if tworzGeometrie:
            tekst = 5*" * " + "PROCES TWORZENIA GEOMETRII ZAKONCZONY SUKCESEM" + 5*" * "
            print tekst
        else:
            raise ValueError("!!! NIE ZDOLALALEM UTWORZYC GEOMETRII !!!")  
    
    def dyskretyzujGeometrie(self):
        """
        Metoda, potrzebna do rozpoczęcia procesu dyskretyzacji. Dyskretyzacja składa sie z dwóch kroków. Najpierw geometria jest tworzona w GMSHu na podstawie pliku wsadowego, następnie zostaje zdyskretyzowana i zapisana jako plik *.msh* i *.inp*.
        """
               
        cmd = self.gmsh + ' ' + self.nazwa + '.geo ' + '-saveall -2'
        print cmd
        tworzSiatke = self.wyslijKomende(cmd)
        if tworzSiatke:
            tekst = 5*" * " + "PROCES TWORZENIA SIATKI ZAKONCZONY SUKCESEM" + 5*" * "
            print tekst
        else:
            raise ValueError("!!! NIE ZDOLALALEM UTWORZYC SIATKI !!!")
        
        self.usunPliki("LloydInit.pos")
        self.usunPliki("wirnik.geo_unrolled")
    
    def wizualizacjaObiektu(self):
        """
        Proces tworzenia obiektu do wizualizacji składa sie ze stworzenia geometrii w formacie wrl a nastepnie przekonwertowania jej do postaci *.stl*. Jest możliwa konwersja bezpośrednia do formatu *.stl*, niestety w przypadku użycia elementów typu *hex* użytkownik uzyskuje wizualizacje niskiej jakości.

        """
        cmd = self.gmsh + ' ' + self.nazwa + '.msh ' + '-o ' + self.nazwa + '.wrl -format wrl -0'
        #print cmd
        self.wyslijKomende(cmd)
        cmd = self.gmsh + ' ' + self.nazwa + '.wrl ' + '-o ' + self.nazwa + '.stl -format stl -0'
        self.wyslijKomende(cmd)
        self.usunPliki(self.nazwa + '.wrl')
    
    def rozwiazProblem(self,pokazWyniki=False):
        """
        Metoda, dzięki której plik wsadowy *.inp* wysyłany jest do Calculix'a. Program ten automatycznie rozpoczyna proces rozwiązywania zdefiniowanego wcześniej problemu.sluzaca wysylaniu pliku do Calculix'a

        :param pokazWyniki: zmienna określająca czy wyniki z Calculix'a powinny się pojawić automatycznie na ekranie monitora jak tylko zostaną uzyskane
        :type pokazWyniki: bool
        """
        cmd = self.ccx_dir + ' ' + self.wd + '/ccxInp'
        self.wyslijKomende(cmd)
        
        # Jesli zmienna 'pokazWyniki' istnieje, otworz wyniki w programie 
        # Calculix Graphics
        if pokazWyniki:
            cmd = self.cgx_dir + ' ' + self.wd + '/ccxInp.frd'
            self.wyslijKomende(cmd,output = False)
        
    def usunPliki(self,nazwa):
        """
        Metoda, dzięki której możliwe jes usunięcie zbędnych plików.

        :param nazwa: nazwa pliku, który powinien zostać usunięty
        :type nazwa: string
        """

        try:
            os.remove(nazwa)
        except OSError:
            pass
        
    def przygotujSymulacje(self):
        """
        Metoda usuwająca zbędne pliki przed symulacją, aby nie było problemów z ich nadpisaniem.
        """
        self.usunPliki('ccxInp.cvg')
        self.usunPliki('ccxInp.dat')
        self.usunPliki('ccxInp.frd')
        self.usunPliki('ccxInp.inp')
        self.usunPliki('ccxInp.sta')
        self.usunPliki('spooles.out')

class Geometry(object):
    """
    Klasa *Geometry* służy do przechowywania wszystkich wielkości opisujących kształt geometrii.
    """

    def __init__(self): pass
        
    def dodajCeche(self,cecha):
        """
        Metoda poszerzająca definicję geometrii o kolejną cechę.

        :param cecha: cecha która ma zostać dodana do definicji analizowanej konstrukcji.
        :type cecha: float/int
        """
        self.cecha = cecha
    
    def __str__(self):
        t1 = 'Informacje zawarte w geometrii:\n'
        for key, item in self.__dict__.iteritems():
            t1 += '- ' + str(key) + ' - ' + str(item)+'\n'
        return t1
       
class Sender(object):
    """
    Klasa Sender służy do tworzenia obiektów posiadających informacje odnośnie badanego obiektu. Obiekt tej klasy będzie dzielił te informacje dzięki klasie :class:`SenderBrain` z oprogramowaniem zewnętrznym.
    """

    def __init__(self):
        """Konstruktor klasy Sender"""
        # Stworz obiekt Geometry
        self.Geo = Geometry()
        # Stworz kontener zawierajacy informacje o modelu numerycznym
        self.Info = {}
    
    def pobierzDane(self,dane):
        """
        Metoda służąca do poprawnego wydobycia danych z GUI.

        :param dane: kontener zawierający definicje pobrany. Kontener powinien zostać przygotowany na etapie pobieranie danych z menu w następujący sposób {'nazwaCechy' : wartość}.
        :type dane: dictionary
        """
        temp = {}
        # Przystosuj wyniki
        for key, item in dane.iteritems():
            if key[0:3] == 'n_r':
                item = float(item) / 2.0
            temp[key] = str(item)
        
        for key, item in temp.iteritems():
            # Zapisz cyfry do obiektu Geometria            
            if key[0] == 'n':
                exec("self.Geo.%s = %s" % (key[2:],item))
            # Zapisz cechy do kontenera Info
            elif key[0] == 's':
                self.Info[key[2:]] = item

    def testujDane(self):
        """
        Dzięki tej metodzie dane pobrane z menu głównego mogą zostać sprawdzone pod kątem ich poprawności.
        """
        Info = self.Info        
        for key, item in Info.iteritems():
            if type(item) != str:
                raise ValueError("Bledny typ danych pobrany z GUI (Geo) - " + 
                    str(key) + ' = ' + str(item) + ' - ' + str(type(item)))
                
        G = self.Geo
        for key, item in G.__dict__.iteritems():
            if type(item) != float and type(item) != int:
                raise ValueError("Bledny typ danych pobrany z GUI (Geo) - " + 
                    str(key) + ' = ' + str(item) + ' - ' + str(type(item)))
                
        if not (G.r1 <= G.r2 <= G.r3):
            text = "Srednica otworu, srednica do lopatek i srednica zewnetrzna \
                jest zle dobrana"
            print G.r1, G.r2, G.r3
            raise ValueError(text)
    
        if G.r4 >= G.r3:
            text = "Srednica wylotu jest nieodpowiednia do srednicy zewnetrznej"
            raise ValueError(text)
    
        if G.r4 >= G.r3:
            text = "Srednica wylotu jest nieodpowiednia do srednicy zewnetrznej"
            raise ValueError(text)
        
        if G.h3-G.h2 < 0.0 :
            text = "Wartosc naddatku nieprawidlowa"
            raise ValueError(text)
    
        if G.il_l < 2:
            text = "Wirnik musi zawierac co najmniej dwie lopatki!"
            raise ValueError(text)