# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 19:29:48 2016

@author: slawek
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 21:39:43 2016

@author: Slawek

W tym pliku zawarte sa wszystkie funkcje ktore zostaly uzyte do obliczen
polozenia poszczegolnych punktow wirnika. W tym celu zostal wykorzystany 
modul SymPy, ktory pozwala na obliczenia z bardzo duza dokladnoscia.
"""
import numpy as np
import sympy
import sympy.geometry as sg
from scipy.optimize import fsolve
M = np.array

def dodajWspolrzedne(wek, pkt_B):
    """Funkcja wykorzystuje modul Sympy w celu obliczenia punktow lezacych na
    krzywiznie lopatki. W tym celu tworzony jest obiekt okregu wraz z dwoma
    punktami wyznaczajacymi poczatek i koniec lopatki. Dzieki temu mozliwe jest 
    obliczenie punktow posrednich pomiedzy wspomnianym poczatkiem a koncem"""
    
    # Deklaracja zmiennych
    srOk = M([wek[2][0],wek[2][1]])
    L1 = sg.Point(wek[0][0],wek[0][1])
    L6 = sympy.N(sg.Point(wek[1][0],wek[1][1]))
    
    # Srodek okregu, ktory zawiera krzywizne wirnika    
    L_cent = sg.Point(srOk[0],srOk[1])
    # Zwroc promien wirnika  
    promien = sympy.N(L1.distance(L_cent))
    # Prosta pozioma przechodzaca przez srodek ukladu wspolrzednych
    hl = sg.Line(sg.Point(0.,0.),sg.Point(1.,0.))
    # Prosta przechodzaca przez srodek krzywizny i punkt poczatkowy lopatki
    l_6 = sg.Line(L6,L_cent)
    # Prosta przechodzaca przez srodek krzywizny i punkt koncowy lopatki
    l_1 = sg.Line(L1,L_cent)
    
    # Oblicz kat pomiedzy prosta l_6 a prosta pozioma
    ang_6_hl = float(sympy.N(l_6.angle_between(hl)) + np.pi)
    # Oblicz kat pomiedzy prosta l_1 a prosta pozioma    
    ang_1_hl = float(sympy.N(l_1.angle_between(hl)) + np.pi)
    
    # Zdefiniuj w ilu punktach krzywizna wirnika powinna zostac obliczona    
    podzial = 8
    # Stworz wektor zawierajacy katy, ktore zostana uzyte do obliczenia punktow
    vec_I = np.linspace(ang_6_hl,ang_1_hl,num=podzial)[1:-1]

    # Funkcja opisujace krzywizne lopatki w sposob parametryczny
    def krzywiznaParametrycznie(t):
        x = srOk[0]+promien*np.cos(t)
        y = srOk[1]+promien*np.sin(t)
        return [x,y]
    
    # Stworz wektor zawierajacy wspolrzedne punktow opisujacych lopatke
    r_temp = [[L6.x,L6.y],]
    for i in vec_I:
        # Oblicz polozenie punktu na podstawie parametrycznej funkcji opisujacej
        # krzywizne lopatki i kata okreslajacego wspolrzedne.
        krzyw = krzywiznaParametrycznie(i)
        r_temp.append(krzyw)
    
    r_temp.append([L1.x,L1.y])
    r_temp.reverse()
    r_temp.append(srOk)

    return r_temp
    
def obliczPunktyKrzywej(geometria,pktOkr):
    """Funkcja oblicza wspolrzedne na plaszczyznie 2D - XZ. Algorytm polega
    na rozwiazaniu rownania nieliniowego dzieki uzyciu funkcji fsolve
    z modulu SciPy. Dzieki rozwiazaniu rownania uzytkownik otrzyma punkt 3 
    punkty okreslajace polozenie lopatki. W celu doklaniejszego odwzorowania
    krzywizny zostala wykorzystana funkcja."""
    # Zdefiniuj parametry rownania
    al_1 = np.deg2rad(geometria.b1)
    al_2 = np.deg2rad(geometria.b2)
    r = geometria.r2
    R = geometria.r3
    kat_pol = np.pi
    
    # Rownanie opisujace zaleznosc trygonometryczna od ksztaltu lopatek
    def rownanieTrygonometryczne(p):
        theta = p
        f1 = (al_2 + al_1 + theta - kat_pol +
            2.*(np.arctan((r*np.sin(theta))/(R-r*np.cos(theta)))))
        return f1
    
    # Oblicz kat wg rysunku z dokumentacji
    theta = fsolve(rownanieTrygonometryczne,(0))
    theta = theta[0]
    
    # Zdefiniuj polozenie punktow 
    A = M([0.,-R])
    B = M([-r*np.sin(theta),-r*np.cos(theta)])
    
    A_B = M([((A[0]+B[0])/2.),  ((A[1]+B[1])/2.)])
    a_1 = (A[0]-B[0])/(B[1]-A[1])
    b_1 = A_B[1]-a_1*A_B[0]
    
    a_2 = 1./np.tan(al_1)
    b_2 = -R
    
    C_x = (b_2-b_1)/(a_1-a_2)
    C_y = a_1*C_x+b_1
    R_l = M([C_x,C_y])
    
    # Zdefiniuj wspolrzedne punktow na lopatce
    pktyLopatki = dodajWspolrzedne([A,B,R_l],pktOkr)
    for i in pktyLopatki: i[0], i[1] = float(i[0]), float(i[1])  
    
    return pktyLopatki

def wspolrzednePktLopatki(geometria,pkty_XYZ,temp):
    """Funkcja ma na celu okreslenie punktow tworzacych lopatke wirnika"""
    
    # Deklaracja zmiennych
    r2 = geometria.r2   
    R = geometria.R
    funLin = temp['funLin']
    pc = temp['pc']
    C = temp['C']
    R_pos = temp['R_pos']
    
    krzywaLop_xy = obliczPunktyKrzywej(geometria,pkty_XYZ[1,1:])
    
    def wspolrzednaZ(p):
        odl = np.sqrt(p[0]**2. + p[1]**2.)
        if abs(pkty_XYZ[2][1]) <= odl <= abs(pkty_XYZ[1][1]):
            z = -np.sqrt(R**2. - (-odl - pkty_XYZ[4][1])**2.) + pkty_XYZ[4][2]
            return z
        elif abs(pkty_XYZ[1][1]) <= odl <= abs(pkty_XYZ[0][1]):
            z = funLin(odl)
            return z
        else:
            print 'Brak takiej wspolrzednej'
    
    
    kLop_xyz = []   
    for i in krzywaLop_xy[:-1]:
        z = wspolrzednaZ(i)
        kLop_xyz.append([i[0],i[1],z])
    
    kLop_xyz.append([krzywaLop_xy[-1][0],krzywaLop_xy[-1][1]])
    kLop_xyz = M(kLop_xyz)
    
    def krzywiznaParametrycznie(t):
        x = (-R_pos[0]+R*np.cos(t))
        y = R_pos[1]+R*np.sin(t)
        return M([x,y])
    
    R_C = sg.Line(pc,sg.Point(C[0],C[1]))
    R_B = sg.Line(pc,sg.Point(r2,kLop_xyz[-2][2]))
    ang = 2*np.pi - float(sympy.N(R_C.angle_between(R_B)))

    vec_I = np.linspace(ang,
                        2.*np.pi,
                        num=5)

    kolo_BC = []
    for i in vec_I:
        temp = [0.0]
        temp.extend(krzywiznaParametrycznie(i))
        kolo_BC.append(temp)
    kolo_BC.append(pkty_XYZ[-2])
    kolo_BC = np.array(kolo_BC)[1:]
    return kolo_BC, kLop_xyz
    
def wspolrzednePktPrzekroju(geometria,temp):
    # Deklaracja zmiennych
    alfa = geometria.alfa    
    h1 = geometria.h1
    h2 = geometria.h2
    h3 = geometria.h3
    r3 = geometria.r3
    r4 = geometria.r4
    R = geometria.R
    
    # Deklaracja punktow na przekroju    
    A = M([r3, h1])
    C = M([r4, h2])
    D = M([r4, h3])
    R_pos = M([(r4 + R), C[1]])
    temp['C'] = C
    temp['R_pos'] = R_pos
    
    # Tworzenie funkcji liniowej okreslajacej pochylenie wirnika    
    a = np.tan(np.deg2rad(-alfa))
    b = h1 - a*r3
    funLin = lambda x: a*x + b
    temp['funLin'] = funLin 
    
    # Wykorzystanie biblioteki Sympy do okreslenia punktu przeciecia sie
    # zaokraglonej czesci wirnika z pochylona plaszczyzna
    p1 = sg.Point(A[0], A[1])
    p2 = sg.Point(r3-2.0, funLin(r3-2.0))

    l = sg.Line(p1,p2)
    pc = sg.Point(R_pos[0],R_pos[1])    
    c = sg.Circle(pc,R)
    temp['pc'] = pc
    # Punkty przeciecia sie okregu z prosta
    punkty = sg.intersection(c,l)
    
    # Okresl czy istnieja punkty przeciecia i wybierz poprawne
    if len(punkty)==0:
        text = "Powierzchnia wylotu nie moze zostać stworzona. Zmien wartosc \
            wymiaru wysokosci lopatki, kat alfa, badz promien zaokraglenia"
        raise ValueError(text)

    if len(punkty) == 2:
        w = min(punkty, key=lambda p: p.y)
        B = M([sympy.N(w).x,sympy.N(w).y])
    else:
        w = punkty
        B = M([sympy.N(punkty).x,
               sympy.N(punkty).y])

    # Zbierz wszystkie punkty w jednej macierzy 'pkty_YZ'
    pkty_YZ = M([A,B,C,D,R_pos])
    
    # Przystosuj zmienne do obliczen w GMSH'u
    for i in pkty_YZ:
        i[0], i[1] = float(i[0]), float(i[1])
        i[0] = -i[0]
    
    # Dodaj trzeci wymiar do obliczonych punktow
    pkty_XYZ = np.insert(pkty_YZ, 0, 0.0, axis=1)
    return temp, pkty_XYZ

def oblicz(geometria):  
    # Stworz tymczasowy pojemnik na dane
    temp = {}
#==============================================================================
#   Obliczenia majace na celu ustalenie polozenia punktow na przekroju YZ 
#   wirnika (rysunek w dokumentacji)
#==============================================================================
    temp, pkty_XYZ = wspolrzednePktPrzekroju(geometria,temp)
#==============================================================================
#   Obliczenia majace na celu ustalenie wspolrzednych Lopatki
#==============================================================================
    kolo_BC, kLop_xyz = wspolrzednePktLopatki(geometria,pkty_XYZ,temp)
    geometria.kolo_BC = kolo_BC
    geometria.kLop_xyz = kLop_xyz
    
    return geometria

if __name__ == "__main__":
    main()