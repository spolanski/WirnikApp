# -*- coding: utf-8 -*-
"""
W niniejszym pliku zawarte zostały wszystkie funkcje które zostały użyte w celu określenia położenia poszczególnych punktów wirnika. Podczas tej procedury wykorzystany został moduł SymPy.
"""
import numpy as np
import sympy
import sympy.geometry as sg
from scipy.optimize import fsolve
M = np.array

def policzPktyZaokraglenia(geometria, temp):
    """
    Funkcja ma na celu obliczenie punktów na krzywej wirnika w górnej jego części (zob. krzywą :math:`ED` na rysunku przekroju wirnika). Procedura obliczania punktów na krzywej jest identyczna jak w przypadku funkcji :func:`dodajWspolrzedne`.

    :param geometria: obiekt klasy Geometry zawierający dane geometryczne wirnika
    :type geometria: Geometry
    :param temp: tymczasowy kontener na dane, użyty w celu przechowywania informacji.
    :type temp: dictionary

    :return kolo_BC: obiekt *list* zawierający punkty leżące na zaokrągleniu w górnej części wirnika.
    """
    lopatka_XYZ = geometria.lopatka_XYZ
    r2 = geometria.r2
    R = geometria.R
    C = temp['C']
    R_pos = temp['R_pos']
    pc = temp['pc']
    pkty_XYZ = temp['pkty_XYZ']
    
    def krzywiznaParametrycznie(t):
        x = (-R_pos[0] + R*np.cos(t))
        y = R_pos[1] + R*np.sin(t)
        return M([x,y])

    R_C = sg.Line(pc,sg.Point(C[0],C[1]))
    R_B = sg.Line(pc,sg.Point(r2,lopatka_XYZ[-2][2]))
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
    
    return kolo_BC
    
def dodajWspolrzedne(wek):
    r"""
    Funkcja zawiera opis krzywizny łopatki we współrzędnych parametrycznych. W pierwszym etapie zostają wyznaczone kąty :math:`{\kappa}_{1}` i :math:`{\kappa}_{2}`. Następnie tworzona jest tablica zawierająca osiem równoodległych wartości z pomiędzy tych kątów. Tak otrzymane dane zostają użyte przy określaniu punktów leżących na krzywej :math:`AC`.

    .. figure:: ./image/kat.png
        :align: center
        :alt: Krzywizna łopatki
        :figclass: align-center
        :scale: 18%

        Szkic krzywizny łopatki

    :param wek: tablica zawierająca położenie punktów :math:`A`, :math:`B` i :math:`C`.
    :type wek: lista zawierająca współrzędne punktów na krzywiźnie łopatki
    """
    
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
    
def obliczPunktyKrzywej(geometria):
    r"""
    Funkcja obliczająca wspołrzędne punktów A, B, C łopatki. Algorytm wykorzystuje funckcję *fsolve* z modułu SciPy w celu rozwiązania równania nieliniowego przedstawionego poniżej. W oparciu o współrzędne wymienionych punktów funkcja :func:`dodajWspolrzedne` oblicza osiem punktów leżących na krzywiźnie łopatki.

    .. figure:: ./image/lopatka.png
        :align: center
        :alt: Położenie łopatki
        :figclass: align-center
        :scale: 70%

        Szkic wirnika w płaszczyźnie XY

    W celu określenia współrzędnej punktu :math:`A` należy wpierw określić kąt :math:`\theta`. Kąt można określić następującą zależnością:

    .. math::
        \delta = \arctan(\tfrac{r-sin\theta}{R-rsin\theta}) \\
        \gamma = \delta + {\beta}_{1} \\
        \gamma + {\beta}_{2} + \theta + \delta = 180^{\circ} \implies {\beta}_{1} + {\beta}_{2} + \theta + 2\cdot\delta = 180^{\circ}

    .. math::
        {\beta}_{1} + {\beta}_{2} + \theta + 2\arctan(\tfrac{r-sin\theta}{R-rsin\theta}) - 180^{\circ} = 0

    :param geometria: obiekt klasy Geometry zawierający dane geometryczne wirnika
    :type geometria: Geometry
    
    :return pktyLopatki: tablica zawierająca punkty znajdujące się na krzywej łopatki.
"""
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
    pktyLopatki = dodajWspolrzedne([A,B,R_l])
    for i in pktyLopatki: i[0], i[1] = float(i[0]), float(i[1])      
    return pktyLopatki, theta

def wspolrzednePktLopatki(geometria,temp):
    """
    Funkcja służąca do określenia punktów krzywizny łopatki. W pierwszym etapie wywoływana jest funkcja :func:`obliczPunktyKrzywej` w celu określenia punktów na krzywej. Następnym krokiem jest obliczenie trzeciej współrzędnej każdego punktu, tak aby możliwe było stworzenie geometrii trójwymiarowej.

    :param geometria: obiekt klasy Geometry zawierający dane geometryczne wirnika
    :type geometria: Geometry
    :param temp: tymczasowy kontener na dane, użyty w celu przechowywania informacji.
    :type temp: dictionary

    :return lopatka_XYZ: lista zawierająca współrzędne punktów określających krzywiznę łopatki.
    """
  
    # Deklaracja zmiennych
    R = geometria.R
    funLin = temp['funLin']
    pkty_XYZ = temp['pkty_XYZ']
#==============================================================================
#   W tym miejscu liczone sa punkty okreslajace na w plaszczyznie XY
#==============================================================================
    lopatka_XY, theta = obliczPunktyKrzywej(geometria)
    
    def okreslWspolrzednaZ(p):
        odl = np.sqrt(p[0]**2. + p[1]**2.)
        if abs(pkty_XYZ[2][1]) <= odl <= abs(pkty_XYZ[1][1]):
            z = -np.sqrt(R**2. - (-odl - pkty_XYZ[4][1])**2.) + pkty_XYZ[4][2]
            return z
        elif abs(pkty_XYZ[1][1]) <= odl <= abs(pkty_XYZ[0][1]):
            z = funLin(odl)
            return z
        else:
            print 'Brak takiej wspolrzednej'
    
    lopatka_XYZ = []   
    for i in lopatka_XY[:-1]:
        z = okreslWspolrzednaZ(i)
        lopatka_XYZ.append([i[0],i[1],z])
    
    lopatka_XYZ.append([lopatka_XY[-1][0],
                     lopatka_XY[-1][1]])
    lopatka_XYZ = M(lopatka_XYZ)
    
    return lopatka_XYZ, theta
    
def wspolrzednePktPrzekroju(geometria,temp):
    r"""
    Funkcja służąca do obliczenia niezbędnych wymiarów wirnika. Na poniższym rysunku został przedstawiony przekrój wirnika i punkty określające jego wymiary.
    
    .. figure:: ./image/przekroj.png
        :align: center
        :alt: Szkic przekroju wirnika
        :figclass: align-center
        :scale: 20%

        Szkic przekroju wirnika

    Punkty te odpowiadają następującym wymiarowm pobranym z GUI:

    * Promień otworu - odl. od osi pionowej do punktu A
    * Promień zewnętrzny - odl. od osi pionowej do punktu B
    * Promień u wylotu - odl. od osi pion
    * Wysokość łopatki - odcinek :math:`|BC|`
    * Kąt alfa - kąt :math:`\alpha`
    * Promień zaokrąglenia - odcinek :math:`|RD|=|RE|`
    * Wysokość pod naddatek - odcinek :math:`|EF|` 
    * Wysokość wirnika - odległość od punktu F do osi poziomej.

    W celu stworzenia geometrii w programie GMSH należy obliczyć położenie punktu :math:`D`. Punkt ten jest określane poprzez sprawdzenie punktów wspólnych okręglu zakreślonego w punkcie :math:`R` o promieniu :math:`|RD|` z prostą przechodzącą przez punkt :math:`C` odchyloną od poziomu o kąt :math:`\alpha`. Zadanie to zostało wykonane przy użyciu modułu SymPy.

    :param geometria: obiekt klasy Geometry zawierający dane geometryczne wirnika
    :type geometria: Geometry
    :param temp: tymczasowy kontener na dane, użyty w celu przechowywania informacji.
    :type temp: dictionary

    :return temp: uaktualniony kontener na dane.
    """

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
    temp['pkty_XYZ'] = pkty_XYZ
    return temp

def obliczWymaganeParametry(Goniec):
    r"""
    Funkcja mająca na celu określenie położenia punktów głównych wirnika. Są to między innymi punkty określające przekrój poprzeczny wirnika, zakrzywienie łopatki, oraz zaokrąglenie w górnej części konstrukcji.

    :param Goniec: obiekt Gońca zawierający informacje wymagane w przygotowaniu analizy numerycznej.
    :type Goniec: Sender
    """  
    # Stworz tymczasowy pojemnik na dane
    geometria = Goniec.Geo
    temp = {}
#==============================================================================
#   Obliczenia majace na celu ustalenie polozenia punktow na przekroju YZ 
#   wirnika (rysunek w dokumentacji)
#==============================================================================
    temp = wspolrzednePktPrzekroju(geometria,temp)
#==============================================================================
#   Obliczenia majace na celu ustalenie wspolrzednych Lopatki
#==============================================================================
    lopatka_XYZ, theta = wspolrzednePktLopatki(geometria,temp)
    geometria.lopatka_XYZ = lopatka_XYZ
    geometria.theta = theta
#==============================================================================
#   Obliczenia pozwalajace okreslic punkty na zaokragleniu przy gornej czesci
#   wirnika    
#==============================================================================
    zaokr = policzPktyZaokraglenia(geometria, temp)
    geometria.zaokr = zaokr

if __name__ == "__main__":
    main()