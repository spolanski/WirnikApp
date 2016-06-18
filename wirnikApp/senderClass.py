# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 22:21:10 2016

@author: slawek
"""
import subprocess
import os, sys

class SenderBrain(object):
    """Klasa odpowiedzialna za przesylanie polecen do GMSHa i Calculixa, oraz 
    odbieranie sygnalow zwrotnych z tych programow. Klasa wykorzystuje modul
    subprocess."""
    
    def __init__(self,Sender):
        """Konstruktor klasy tworzace obiekt pozwalajacy na komunikacje z 
        oprogramowaniem"""
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
        """Metoda dzieki, ktorej mozliwe jest przesylanie wiadomosci do 
        oprogramowania i odbieranie sygnalow powrotnych"""
        
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
        """Metod sluzaca do tworzenia geometrii w programie GMSH"""
        
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
        """Metod, potrzebna do rozpoczecia procesu dyskretyzacji. 
        Dyskretyzacja sklada sie z dwoch krokow. Najpierw geometria jest 
        tworzona w GMSHu na podstawie pliku wsadowego, następnie zostaje 
        zdyskretyzowana i zapisana jako plik msh i inp"""
               
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
        """Proces tworzenia obiektu do wizualizacji sklada sie ze stworzenia
        geometrii w formacie wrl a nastepnie przekonwertowania jej do postaci
        stl. Jest mozliwa konwersja bezposrednia do formatu stl, niestety w
        przypadku uzycia elementow typu hex uzytkownik uzyskuje zlej jakosci
        wizualizacje"""
        cmd = self.gmsh + ' ' + self.nazwa + '.msh ' + '-o ' + self.nazwa + '.wrl -format wrl -0'
        print cmd
        self.wyslijKomende(cmd)
        cmd = self.gmsh + ' ' + self.nazwa + '.wrl ' + '-o ' + self.nazwa + '.stl -format stl -0'
        self.wyslijKomende(cmd)
        self.usunPliki(self.nazwa + '.wrl')
    
    def rozwiazProblem(self,pokazWyniki=False):
        """Metoda sluzaca wysylaniu pliku do Calculix'a"""
        cmd = self.ccx_dir + ' ' + self.wd + '/ccxInp'
        self.wyslijKomende(cmd)
        
        # Jesli zmienna 'pokazWyniki' istnieje, otworz wyniki w programie 
        # Calculix Graphics
        if pokazWyniki:
            cmd = self.cgx_dir + ' ' + self.wd + '/ccxInp.frd'
            self.wyslijKomende(cmd,output = False)
        
    def usunPliki(self,nazwa):
        """Metoda sluzaca do usuwania zbednych plikow"""
        try:
            os.remove(nazwa)
        except OSError:
            pass
        
    def przygotujSymulacje(self):
        """Metoda usuwajaca zbedne pliki przed symulacja"""
        self.usunPliki('ccxInp.cvg')
        self.usunPliki('ccxInp.dat')
        self.usunPliki('ccxInp.frd')
        self.usunPliki('ccxInp.inp')
        self.usunPliki('ccxInp.sta')
        self.usunPliki('spooles.out')

class Geometry(object):
    """Klasa Geometry sluzy do przechowywania wszystkich wielkosci opisujacych 
    ksztalt geometrii."""

    def __init__(self): pass
        
    def dodajCeche(self,cecha):
        self.cecha = cecha
    
    def __str__(self):
        t1 = 'Informacje zawarte w geometrii:\n'
        for key, item in self.__dict__.iteritems():
            t1 += '- ' + str(key) + ' - ' + str(item)+'\n'
        return t1
       
class Sender(object):
    """Klasa Sender sluzy do tworzenia obiektow posiadajacych informacje
    odnosnie badanego obiektu, ktory bedzie dzielil te informacje dzieki 
    klasie SenderBrain z oprogramowaniem zewnetrznym"""

    def __init__(self):
        """Konstruktor klasy Sender"""
        # Stworz obiekt Geometry
        self.Geo = Geometry()
        # Stworz kontener zawierajacy informacje o modelu numerycznym
        self.Info = {}
    
    def pobierzDane(self,dane):
        """Metoda sluzaca do poprawanego wydobycia danych z GUI"""
        
        temp = {}
        # Przystosuj wyniki
        for key, item in dane.iteritems():
            temp[key] = str(item)
        
        for key, item in temp.iteritems():
            # Zapisz cyfry do obiektu Geometria            
            if key[0] == 'n':
                exec("self.Geo.%s = %s" % (key[2:],item))
            # Zapisz cechy do kontenera Info
            elif key[0] == 's':
                self.Info[key[2:]] = item
        
    def testujDane(self):
        """Metoda ktora umozliwia wstepne testowanie poprawnosci danych"""
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