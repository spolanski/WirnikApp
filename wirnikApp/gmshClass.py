# -*- coding: utf-8 -*-
"""
Plik gmshClass.py zawiera klasę Part, której obiekty potrzebne są w celu stworzenia pliku wsadowego do GMSH'a.
"""
from itertools import count
import numpy as np

class Part(dict):
    r"""
    Klasa Part służy do tworzenia obiektów zawierających definicje
    pozwalające napisać plik wsadowy do programu GMSH.

    :param nazwa: nazwa konstrukcji która będzie analizowana
    :type nazwa: string
    """

    def __init__(self,nazwa):
#==============================================================================
#     KONSTRUKTOR    
#==============================================================================
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
        # writeInputFile(). Zawiera on caly plik wsadowy do programu GMSH
        self['txt'] = ''
    
#==============================================================================
#     CZESCI GEOMETRII
#==============================================================================
    def point(self,x,y,z):
        """
        Metoda pośrednia służąca tworzeniu punktów na podstawie
        współrzędnych x,y,z

        :param x: współrzędna X punktu
        :param y: współrzędna Y punktu
        :param z: współrzędna Z punktu
        :type x: float
        :type y: float
        :type z: float
        """
        self.p_id = self.p_ind.next()
        p = Point(x,y,z,self.p_id)
        self['czesci'].append(p)
            
    def circle(self,x,y,z):
        """
        Metoda pośrednia służąca do stworzenia pojedynczych łuków.

        :param x: indeks początkowego punktu
        :param y: indeks środkowego punktu
        :param z: indeks końcowego punktu

        :type x: int
        :type y: int
        :type z: int
        """
        self.l_id = self.l_ind.next()
        k = Circle(x,y,z,self.l_id)
        self['czesci'].append(k)
    
    def manyCircles(self,srodek,kola):
        """
        Metoda pośrednia służąca do tworzenia okręgu na podstawie punktu
        środkowego, oraz punktów na obwodzie.

        :param srodek: indeks punktu środkowego
        :type srodek: int
        :param kola: lista zawierająca obiekty typu :class:`Point`.
        :type kola: list
        """
        n = range(0,len(kola))
        for i in n:
            self.l_id = self.l_ind.next()
            t = Circle(kola[i].id,
                       srodek,
                       kola[(i + 1) % len(kola)].id, self.l_id)
            self['czesci'].append(t)

    def line(self,*args):
        """
        Metoda pośrednia służąca do tworzenia obiektów Line.

        :param args: lista zawierająca indeksy punktów, które mają być ze sobą połączone za pomocą linii.
        :type args: list
        """
        self.l_id = self.l_ind.next()
        k = Line(self.l_id,args)
        self['czesci'].append(k)

    def spline(self,*args):
        """
        Metoda pośrednia służąca do tworzenia obiektów Spline.

        :param args: lista zawierająca indeksy punktów, które mają być ze sobą połączone za pomocą splajnu.
        :type args: list
        """
        self.l_id = self.l_ind.next()
        k = Spline(self.l_id,args)
        self['czesci'].append(k)

    def lloop(self,*args):
        """
        Metoda pośrednia służąca do tworzenia obiektów Line Loop.

        :param args: lista zawierająca indeksy, które mają być zawarte w obiekcie LineLoop.
        :type args: list
        """
        self.ll_id = self.ll_ind.next()
        k = LLoop(self.ll_id,args)
        self['czesci'].append(k)

    def psurf(self,*args):
        """
        Metoda pośrednia służąca do tworzenia obiektów Plane Surface.

        :param args: lista zawierająca indeks obiektu LineLoop, który służy jako baza do stworzenia powierzchni.
        :type args: list
        """
        self.r_id = self.r_ind.next()
        k = PSurface(self.r_id,args)
        self['czesci'].append(k)

    def rsurf(self,*args):
        """
        Metoda pośrednia służąca do tworzenia obiektów Ruled Surface.

        :param args: lista zawierająca indeks obiektu LineLoop, który służy jako baza do stworzenia powierzchni.
        :type args: list
        """
        self.r_id = self.r_ind.next()
        k = RSurface(self.r_id,args)
        self['czesci'].append(k)

    def physical(self,nazwa,*args):
        """
        Metoda pośrednia służąca do tworzenia obiektów typu Physical (zbiorów elementów skończonych w pliku wsadowym).

        :param nazwa: nazwa obiektu jaki ma zostać stworzony. Przykładowo, jeżeli nazwa jest równa 'Surface' to zostanie zbiór elementów na płaszczyźnie.
        :type nazwa: string
        :param args: lista zawierająca indeksy obiektów (linii lub powierzchni) dla których ma zostać stworzony zbiór.
        :type args: list
        """
        self.l_id = self.l_ind.next()
        k = Physical(self.l_id,nazwa,args)
        self['czesci'].append(k)
    
#==============================================================================
#     METODY
#==============================================================================
    def text(self,text):
        """
        Metoda wymagana do implementowania dowolnej komendy lub komentarza w pliku wsadowym.

        :param text: tekst, który zostanie umieszczony w pliku wsadowym
        :type text: string
        """
        self['czesci'].append(text+'\n')
    
    def writeInputFile(self):
        """
        Metoda służąca do stworzenia pliku wsadowego do GMSH'a. Procedura polega na wydrukowaniu kontenera zawartego w obiekcie klasy :class:`Part` do pliku.
        """
        for i in self['czesci']:
            self['txt'] += str(i)
    
    def prStart(self):
        """
        Metoda służąca do wstawienia wskaźnika, dzięki któremu użytkownik
        może grupować powstające obiekty. Wskaźnik zapamiętuje długość słownika
        części

        :return: zwróć długość słownika zawartego w klasie :class:`Part` w konkretnym momencie kodu.
        :rtype: int
        """
        # Ustaw poczatek naliczania
        prStart = len(self['czesci'])
        # Zwróć wskaźnik        
        return prStart
    
    def prEnd(self,prStart):
        """
        Metoda dzięki, dzięki której uzyskujemy dostęp do poszczególnych
        obiektów. Rezultat ten jest otrzymywany poprzez tworzenie wektora
        obiektów na podstawie indeksu początkowego 'prStart', oraz indeksu
        'prEnd.'

        :param prStart: zmienna określająca długość kontenera w momencie gdy został użyty wskaźnik.
        :rtype: int
        """
        
        # Ustaw koniec naliczania
        prEnd = len(self['czesci'])
        # Stworz liste punktow
        vec = self['czesci'][prStart:prEnd]
        return vec
    
    def rotation(self,punkt,iloscPunktow,theta=0.0, z=0.0):
        """
        Stwórz nowe punkty poprzez rotację punktu wokół punktu (0.0,0.0,0.0). Funkcja dodaje nowo powstałe punkty do obiektu Part. Dodatkowe opcje:

        * zmiana wartości 'z' - zmień współrzędna początkową 'z'
        * zmiana wartości :math:`\theta` - rozpocznij rotację z kątem początkowym różnym od zera.

        :param punkt: obiekt zawierający trzy współrzędne punktu który ma zostać obrócony.
        :type punkt: Point / list
        :param iloscPunktow: ilość współrzędnych, które mają zostać zwrócone.
        :type iloscPunktow: int

        """
        # Podziel 360 stopni na ilosc punktow ktore maja powstac        
        ob = (2*np.pi)/float(iloscPunktow)

        # Funkcja służąca rotacji punktow wobec dowolnej osi
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
            self.point(vec[0],vec[1],z)
            theta += ob
    
    def createStructuredMesh(self,lloop,surf_id,num=1.0):
        """
        Metoda służąca do stworzenia siatki z elementów typu Quad.

        :param lloop: obiekt zawierający krawędzie płaszczyzny, która ma zostać zdyskretyzowana.
        :type lloop: LLoop
        :param surf_id: indeks płaszczyzny, która zostanie zdyskretyzowana.
        :type surf_id: int
        :param num: liczba określająca stopień jakości siatki.
        :type num: float

        """       
        lloop = [abs(i) for i in lloop]
        l_s = "{0}, {1}, {2}, {3}".format(*lloop)
        # Zmienna podzial określa ilość części na które ma zostać podzielona krawędź
        podzial = str(int(10.0 * (1./float(num))))
        self.text("Transfinite Line {%s} = %s Using Progression 1;" % (l_s,podzial))
        self.text("Transfinite Surface {%d};" % surf_id)
        self.text("Recombine Surface {%d};" % surf_id)


class Point(Part):
    """
    Klasa Point zawierająca definicję punktu odpowiednią do tej zawartej 
    w programie GMSH. W celu stworzenia obiektu Point należy wywołać metodę :func:`point` zawartą w klasie Part.
    """

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
    """
    Klasa Circle zawierająca definicję okręgu odpowiednią do tej zawartej w programie GMSH. W celu stworzenia obiektu Circle należy wywołać metodę :func:`circle` zawartą w klasie Part.
    """
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
    """
    Klasa Line zawierająca definicje linii odpowiednią do tej zawartej w programie GMSH. W celu stworzenia obiektu Line należy wywołać metodę :func:`line` zawartą w klasie Part.
    """
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
    """
    Klasa Spline zawierająca definicje splajnu odpowiednią do tej zawartej w programie GMSH. W celu stworzenia obiektu Spline należy wywołać metodę :func:`spline` zawartą w klasie Part.
    """
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
    """
    Klasa LLoop zawierająca definicje obiektu LineLoop odpowiednią do tej zawartej w programie GMSH. W celu stworzenia obiektu LLoop należy wywołać metodę :func:`llop` zawartą w klasie Part.
    """
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
        t = "Line Loop(%d)" % self.id
        t =  t + '= {' + self.args + '};\n'
        return t
    
    def __repr__(self):
        txt = 'LineLoop-'+str(self.id)
        return txt

class PSurface(Part):
    """
    Klasa PSurface zawierająca definicje płaszczyzny odpowiednią do tej zawartej w programie GMSH. W celu stworzenia obiektu PSurface należy wywołać metodę :func:`psurf` zawartą w klasie Part.
    """
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
    """
    Klasa RSurface zawierająca definicje płaszczyzny rozwiniętej odpowiednią do tej zawartej w programie GMSH. W celu stworzenia obiektu RSurface należy wywołać metodę :func:`rsurf` zawartą w klasie Part.
    """
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
    """
    Klasa Physical służy do tworzenia obiektów typu Physical zawartych
    w programie GMSH. Dzięki tej klasie możemy definiować zbiory płaszczyzn, 
    które powinny być wyszczególnione w pliku opisującym siatkę elementów 
    skończonych.
    """
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