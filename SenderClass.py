# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 22:21:10 2016

@author: slawek
"""
import subprocess
import os, sys

#==============================================================================
#   klasa Gmsh odpowiedzialna jest za przesylanie tworzenie geometrii, siatki
#   oraz wysylanie jej do programu Calculix
#==============================================================================
class SenderBrain(object):
    
    def __init__(self,Sender):
        self.part = Sender.Info['Obiekt']
        self.nazwa = self.part['nazwa']
        
        self.gmsh = Sender.Info['GMSH_DIR']
        self.ccx_dir = Sender.Info['CCX_DIR']
        self.cgx_dir = Sender.Info['CGX_DIR']
        
        self.wd = os.getcwd()
              
        if sys.platform == 'linux' or sys.platform == 'linux2':
            self.SHELL = True
        elif sys.platform == 'win32':
            self.SHELL = False  
        
    def wyslijKomende(self,komenda,output=True):
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
        with open(self.nazwa + '.geo','w') as f:
            f.write(self.part['txt'])

        if pokazGmsh == False:
            cmd = '{0} {1} -0'
        else:
            cmd = '{0} {1}'
            
        cmd = cmd.format(self.gmsh,self.nazwa+'.geo')        
        tworzGeometrie = self.wyslijKomende(cmd)
        if tworzGeometrie:
            tekst = 5*" * " + "PROCES TWORZENIA GEOMETRII ZAKONCZONY SUKCESEM" + 5*" * "
            print tekst
        else:
            raise ValueError("!!! NIE ZDOLALALEM UTWORZYC GEOMETRII !!!")  
    
    def dyskretyzujGeometrie(self):
        """Dyskretyzacja sklada sie z dwoch krokow. Najpierw geometria jest
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
        
        if pokazWyniki:
            cmd = self.cgx_dir + ' ' + self.wd + '/ccxInp.frd'
            self.wyslijKomende(cmd,output = False)
        
    def usunPliki(self,nazwa):
        try:
            os.remove(nazwa)
        except OSError:
            pass
    def przygotujSymulacje(self):
        self.usunPliki('ccxInp.cvg')
        self.usunPliki('ccxInp.dat')
        self.usunPliki('ccxInp.frd')
        self.usunPliki('ccxInp.inp')
        self.usunPliki('ccxInp.sta')
        self.usunPliki('spooles.out')

class Geometry(object):
    def __init__(self): pass
        
    def dodajCeche(self,cecha):
        self.cecha = cecha
    def __str__(self):
        t1 = 'Informacje zawarte w geometrii:\n'
        for key, item in self.__dict__.iteritems():
            t1 += '- ' + str(key) + ' - ' + str(item)+'\n'
        return t1
       
class Sender(object):

    def __init__(self):
        self.Geo = Geometry()
        self.Info = {}
    
    def pobierzDane(self,dane):
        for key, item in dane.iteritems():
            if type(item) != str:
                exec("self.Geo.%s = %s" % (key,item))
            else:
                self.Info[key] = item
        
    def testujDane(self):
        G = self.Geo
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