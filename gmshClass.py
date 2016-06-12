# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 22:17:42 2016

@author: slawek
"""
from itertools import count
import numpy as np

class Part(dict):
#==============================================================================
#     KONSTRUKTOR    
#==============================================================================
    def __init__(self,nazwa):
        """Klasa Part sluzy do tworzenia obiektow zawierajacych definicje
        pozwalajace napisac plik wsadowy do programu GMSH."""
        
        # Implementacja automatycznego naliczania powstajacych obiektow
        self.p_ind = count(0)
        self.l_ind = count(1)
        self.ll_ind = count(1)
        self.r_ind = count(1)

        # Kontener zawierajacy nazwe obiektu     
        self['nazwa'] = nazwa        
        # Kontener zawierajacy definicje geometrii        
        self['czesci'] = []
        # Kontener, ktory zostaje wypelniony po uruchomieniu metody
        # napiszPlikWsadowy(). Zawiera on caly plik wsadowy do programu GMSH
        self['txt'] = ''
    
#==============================================================================
#     CZESCI GEOMETRII
#==============================================================================
    def pkt(self,x,y,z):
        """Metoda posrednia sluzaca tworzeniu punktow na podstawie
        wspolrzednych x,y,z"""
        self.p_id = self.p_ind.next()
        p = Point(x,y,z,self.p_id)
        self['czesci'].append(p)
            
    def kolo(self,x,y,z):
        """Metoda posrednia sluzaca do stworzenia pojedynczych lukow"""
        self.l_id = self.l_ind.next()
        k = Circle(x,y,z,self.l_id)
        self['czesci'].append(k)
    
    def wieleKol(self,srodek,kola):
        """Metoda posrednia sluzaca do tworzenia okregu na podstawie punktu
        srodkowego, oraz punktow na obwodzie."""
        n = range(0,len(kola))
        for i in n:
            self.l_id = self.l_ind.next()
            t = Circle(kola[i].id,
                       srodek,
                       kola[(i + 1) % len(kola)].id, self.l_id)
            self['czesci'].append(t)
    
    def line(self,*args):
        """Metoda posrednia sluzaca do tworzenia obiektow Line"""
        self.l_id = self.l_ind.next()
        k = Line(self.l_id,args)
        self['czesci'].append(k)
    
    def spline(self,*args):
        """Metoda posrednia sluzaca do tworzenia obiektow Spline"""
        self.l_id = self.l_ind.next()
        k = Spline(self.l_id,args)
        self['czesci'].append(k)
        
    def lloop(self,*args):
        """Metoda posrednia sluzaca do tworzenia obiektow Line Loop"""
        self.ll_id = self.ll_ind.next()
        k = LLoop(self.ll_id,args)
        self['czesci'].append(k)
    
    def psurf(self,*args):
        """Metoda posrednia sluzaca do tworzenia obiektow Plane Surface"""
        self.r_id = self.r_ind.next()
        k = PSurface(self.r_id,args)
        self['czesci'].append(k)
    
    def rsurf(self,*args):
        """Metoda posrednia sluzaca do tworzenia obiektow Ruled Surface"""
        self.r_id = self.r_ind.next()
        k = RSurface(self.r_id,args)
        self['czesci'].append(k)

    def physical(self,nazwa,*args):
        """Metoda posrednia sluzaca do tworzenia obiektow typu Physical"""
        self.l_id = self.l_ind.next()
        k = Physical(self.l_id,nazwa,args)
        self['czesci'].append(k)
    
#==============================================================================
#     METODY
#==============================================================================
    def t(self,text):
        """Metoda sluzace do tworzenia komentarzy w pliku wsadowym"""
        self['czesci'].append(text+'\n')
    
    def napiszPlikWsadowy(self):
        """Metoda sluzaca do stworzenia pliku wsadowego do GMSH'a"""
        for i in self['czesci']:
            self['txt'] += str(i)
    
    def cnt_st(self):
        """Metoda sluzaca do wstawienia wskaznika, dzieki ktoremu uzytkownik
        moze grupowac powstajace obiekty. Wskaznik zapamietuje dlugosc slownika
        czesci"""
        # Ustaw poczatek naliczania
        cnt_st = len(self['czesci'])
        # Zwroc wskaznik        
        return cnt_st
    
    def cnt_fnd(self,cnt_st):
        """Metoda dzieki, dzieki ktorej uzyskujemy dostep do poszczegolnych
        obiektow. Rezultat ten jest otrzymywany poprzez tworzenie wektora
        obiektow na podstawie indeksu poczatkowego 'cnt_st', oraz indeksu
        cnt_fnd.'"""
        
        # Ustaw koniec naliczania
        cnt_fnd = len(self['czesci'])
        # Stworz liste punktow
        vec = self['czesci'][cnt_st:cnt_fnd]
        return vec
    
    def rotacja(self,punkt,iloscPunktow,theta=0.0, z=0.0):
        """Stworz nowe punkty poprzez rotacje punktu. Dodatkowe opcje:
        - zmiana wartosci 'z' - zmien wspolrzedna poczatkowa 'z'
        - zmiana wartosci 'theta' - rozpocznij rotacje z katem poczatkowym
            roznym od zera
        """
        # Podziel 360 stopni na ilosc punktow ktore maja powstac        
        ob = (2*np.pi)/float(iloscPunktow)

        # Funkcja sluzaca rotacji punktow wobec dowolnej osi
        def rot(theta,rotPoint):
            x = rotPoint[0]
            z = rotPoint[1]
            rotPoint[0] = x*np.cos(theta) - z*np.sin(theta)
            rotPoint[1] = x*np.sin(theta) + z*np.cos(theta)
            return rotPoint
        
        # Oblicz wspolrzedne punktow powstalych poprzez rotacje
        for i in range(iloscPunktow):
            temp = [punkt[0], punkt[1]]
            vec = rot(theta,temp)
            self.pkt(vec[0],vec[1],z)
            theta += ob
    
    def structMesh(self,lloop,surf_id,num=1.0):
        """Metoda sluzaca do stworzenia siatki z elementow typu Quad. Wartosci:
        - lloop - obiekt LineLoop zawierajacy krawedzie plaszczyzny, ktora ma 
            zostac zdyskretyzowana
        - surf_id - indeks plaszczyzny ktora zostanie zdyskretyzowana
        - num - liczba okreslajaca stopien jakosci siatki
        """       
        lloop = [abs(i) for i in lloop]
        l_s = "{0}, {1}, {2}, {3}".format(*lloop)
        podzial = str(int(10.0 * (1./float(num))))
        self.t("Transfinite Line {%s} = %s Using Progression 1;" % (l_s,podzial))
        self.t("Transfinite Surface {%d};" % surf_id)
        self.t("Recombine Surface {%d};" % surf_id)          

class Point(Part):
    """Klasa Point zawierajaca definicje punktu odpowiednia do tej zawartej 
    w programie GMSH"""

    def __init__(self,x,y,z,ind):
        self.x = x
        self.y = y
        self.z = z
        self.id = ind
    
    def __str__(self):
        t = (self.id, self.x, self.y, self.z)
        t = "Point(%d) = {%.5f,%.5f,%.5f};\n" % t
        return t
        
    def __repr__(self):
        txt = 'Point-'+str(self.id)
        return txt

class Circle(Part):
    """Klasa Circle zawierajaca definicje okregu odpowiednia do tej zawartej 
    w programie GMSH"""
    def __init__(self,x,y,z,ind):
        self.x = x
        self.y = y
        self.z = z

        self.id = ind
    
    def __str__(self):
        t = (self.id, self.x, self.y, self.z)
        t = "Circle(%d) = {%d,%d,%d};\n" % t
        return t
        
    def __repr__(self):
        txt = 'Circle-'+str(self.id)
        return txt

class Line(Part):
    """Klasa Line zawierajaca definicje linii odpowiednia do tej zawartej 
    w programie GMSH"""
    def __init__(self,ind,*args):
        if type(args[0][0])==list:
            
            temp = args[0][0]
            self.args = str(temp)[1:-1]
        
        elif len(args[0]) == 1:
            self.args = str(args[0][0])

        else:
            self.args = str(args[0])[1:-1]
        
        self.id = ind
    
    def __str__(self):
        t = "Line(%d)" % self.id
        t =  t + '= {' + self.args + '};\n'
        return t
    
    def __repr__(self):
        txt = 'Line-'+str(self.id)
        return txt
        
class Spline(Part):
    """Klasa Spline zawierajaca definicje splajnu odpowiednia do tej zawartej 
    w programie GMSH"""
    def __init__(self,ind,*args):
        if type(args[0][0])==list:
            
            temp = args[0][0]
            self.args = str(temp)[1:-1]
        
        elif len(args[0]) == 1:
            self.args = str(args[0][0])

        else:
            self.args = str(args[0])[1:-1]
        
        self.id = ind
    
    def __str__(self):
        t = "Spline(%d)" % self.id
        t =  t + '= {' + self.args + '};\n'
        return t
    
    def __repr__(self):
        txt = 'Spline-'+str(self.id)
        return txt

class LLoop(Part):
    """Klasa LLoop zawierajaca definicje petli krawedzi (Line Loop) odpowiednia
    do tej zawartej w programie GMSH"""
    def __init__(self,ind,*args):
        if type(args[0][0])==list:
            
            temp = args[0][0]
            self.args = str(temp)[1:-1]
        
        elif len(args[0]) == 1:
            self.args = str(args[0][0])

        else:
            self.args = str(args[0])[1:-1]
        
        self.id = ind#self._ids.next()

    def __str__(self):
        t = "Line Loop(%d)" % self.id
        t =  t + '= {' + self.args + '};\n'
        return t
    
    def __repr__(self):
        txt = 'LineLoop-'+str(self.id)
        return txt

class PSurface(Part):
    """Klasa PSurface zawierajaca definicje plaszczyzny (Plain Surface)
    odpowiednia do tej zawartej w programie GMSH"""
    def __init__(self,ind,*args):
        if type(args[0][0])==list:
            
            temp = args[0][0]

            self.args = str(temp)[1:-1]
        
        elif len(args[0]) == 1:
            
            self.args = str(args[0][0])

        else:
            self.args = str(args[0])[1:-1]
        
        self.id = ind
    
    
    def __str__(self):
        t = "Plane Surface(%d)" % self.id
        t =  t + '= {' + self.args + '};\n'
        return t
    def __repr__(self):
        txt = 'PlaneSurface-'+str(self.id)
        return txt

class RSurface(Part):
    """Klasa RSurface zawierajaca definicje powierzchni zaokraglonej (Ruled
    Surface) odpowiednia do tej zawartej w programie GMSH"""
    def __init__(self,ind,*args):
        if type(args[0][0])==list:
            
            temp = args[0][0]

            self.args = str(temp)[1:-1]
        
        elif len(args[0]) == 1:
            
            self.args = str(args[0][0])

        else:
            self.args = str(args[0])[1:-1]
        
        self.id = ind
    
    def __str__(self):
        t = "Ruled Surface(%d)" % self.id
        t =  t + '= {' + self.args + '};\n'
        return t
    def __repr__(self):
        txt = 'RuledSurface-'+str(self.id)
        return txt

class Physical(Part):
    """Klasa Physical zawierajaca definicje obiektow typu Physical zawartych
    w programie GMSH. Dzieki tej klasie mozemy definiowac zbiory plaszczyzn, 
    ktore powinny byc wyszczegolnione w pliku opisujacym siatke elementow 
    skonczonych."""
    def __init__(self,ind,nazwa,*args):
        if type(args[0][0])==list:
            
            temp = args[0][0]
            self.args = str(temp)[1:-1]
        
        elif len(args[0]) == 1:
            self.args = str(args[0][0])

        else:
            self.args = str(args[0])[1:-1]
        
        self.nazwa = nazwa
        self.id = ind
    
    def __str__(self):
        t = "Physical %s(%d)" % (self.nazwa,self.id)
        t =  t + '= {' + self.args + '};\n'
        return t
    
    def __repr__(self):
        txt = 'Physical %s-%d' % (self.nazwa,self.id)
        return txt