# -*- coding: utf-8 -*-
"""
W tym pliku następuje konwersja pliku wsadowego z programu GMSH na plik do programu Calculix.
"""
import numpy as np
import os

def zmianaElem(mesh, stMesh):
    """
    Funkcja zmienia formę zapisu elementów na odpowiednia dla Calculix'a.
    """
    np.set_printoptions(threshold='nan')
    quad = []    
    for i in stMesh:
        for wsk, j in enumerate(mesh):
            s = "ELSET=Surface" + str(i)
            if s in j:
                quad.append(wsk)

    for i in quad:
        mesh[i] = mesh[i].replace("type=CPS4", "type=S8")
        mesh[i] = mesh[i].split("\n",1)
        mesh[i][1] = mesh[i][1].replace("\n",", ")
        mesh[i][1] = mesh[i][1][:-1]
        ar = np.fromstring(string = mesh[i][1], dtype=int, sep=',')
        
        div = 10
        if len(ar) % div != 0:
            raise ValueError("Blad w macierzy")
        else:
            row = len(ar)/div
              
        ar = np.reshape(ar, (row,div))
        ar = np.delete(ar,9,1)
        elem = np.array2string(ar, separator=', ')[2:-2]
        elem = elem.replace("],","")
        elem = elem.replace(" [","")
        
        mesh[i] = mesh[i][0] + "\n" + elem + "\n"

    element = "".join(mesh)
    return element

def zmianyWez(nodes):
    """
    Funkcja zmienia formę zapisu węzłów na odpowiednia dla Calculix'a
    """
    nodes = nodes.split("*NODE\n")
    nodes[1] = nodes[1].replace("\n",", ")
    nodes[1] = nodes[1].split(", ")[:-1]
    nodes[1] = [eval(i) for i in nodes[1]]
    
    def sprawdzZero(a):
        b = float(a)
        temp = round(b,4)
        if temp != 0.0000:
            return a
        else:
            return 0
    st = ""
    wsk = 1
    for node in nodes[1]:
        temp = str(sprawdzZero(node))
        if wsk % 4 != 0:
            st += temp + ", "
        else:
            st += temp + "\n"
        wsk += 1
    nodes[1] = "*NODE\n" + st
    nodes = nodes[0] + nodes[1]
    return nodes

def konwertujSiatke(Goniec):
    """
    Funkcja pozwala na przygotowanie pliku *.inp* stworzonego w programie    GMSH, tak aby mógł zostać użyty w Calculixie. Funkcja była testowana na elementach typu SHELL.

    :param Goniec: obiekt Gońca zawierający informacje potrzebne do stworzenia pliku z siatką elementów skończonych.
    """
    
    # Zdefiniuj zmienne
    wd = os.getcwd()
    nazwaPliku = wd + '/' + Goniec.Info['Obiekt']['nazwa']
    indSet = Goniec.Info['indSet']
    stMesh = Goniec.Info['structMesh']
    
    # Wczytaj siatke z pliku
    with open(nazwaPliku+'.inp','r') as f:
        txt = f.read()

    # Podziel dane na czesc zawierajaca elementy i wezly
    nodes, els = txt.split("******* E L E M E N T S *************")
    # Przekonwertuj czesc odpowiedzialna za wezly    
    nodes = zmianyWez(nodes)
    
    # Podziel czesc opisujaca elementy na elementy 1D oraz 2D
    oneD, twoD = els.split("*ELEMENT, type=CPS6, ELSET=Surface1",1)
    twoD = "*ELEMENT, type=CPS6, ELSET=Surface1" + twoD
    
    twoD, sets = twoD.split("*ELSET",1)
    # Zamien nazwe typu elementow z 'CPS6' na 'S6'
    twoD = twoD.replace("CPS6","S6")
    twoD = twoD.split("*ELEMENT")[1:]
    for i in range(len(twoD)): twoD[i] = "*ELEMENT" + twoD[i]
    # Przekonwertuj czesc odpowiedzialna za elementy     
    twoD = zmianaElem(twoD, stMesh)
    
    # Czesc w ktorej przygotowywane zbiory elementow
    elSet, nSet = sets.split("*NSET",1)
    elSet = elSet.split("*ELSET")
    allSet = ""
    temp = indSet.values()
    temp.remove(indSet['wlot'])
    
    for num in temp:    
        allInd = "PhysicalSurface" + str(num)   
        for i in elSet:
            if allInd in i:
                allSet = allSet + "*ELSET" + i
                break
    # Czesc w ktorej przygotowywane zbiory wezlow 
    nSet = nSet.split("*NSET")
    lineSet = ""
    lineInd = "PhysicalLine" + str(indSet['wlot'])   
    
    for i in nSet:
        if lineInd in i:
            lineSet = "*NSET" + i
            break
    
    # Przygotuj caly tekst zawierajacy siatke elementow skonczonych
    text = nodes + twoD + allSet + lineSet
    
    # Zapisz plik zawierajacy siatke elementow skonczonych
    with open(nazwaPliku+'.inp','w') as f:
        f.write(text)

def stworzPlikWsadowy(Goniec):
    """
    Funkcja służąca tworzeniu pliku wsadowego do Calculixa. Również dzięki tej funkcji, wartości pobrane z GUI opisujące warunki brzegowe, oraz obciążenie zostają wyodrębnione z Gońca.

    :param Goniec: obiekt Gońca zawierający informacje potrzebne do stworzenia pliku z siatką elementów skończonych.
    """
    Info = Goniec.Info
    
    inpFile = """
*INCLUDE, INPUT=NAZWA.inp
*Material, name=Stal
*Density
GESTOSC,
*Elastic
MYOUNG,POISS

*Shell Section, elset=PhysicalSurfaceG_WEW, material=Stal, offset=-0.5
1.5
*Shell Section, elset=PhysicalSurfaceG_ZEW, material=Stal, offset=0.5
1.5
*Shell Section, elset=PhysicalSurfacePODSTAWA, material=Stal, offset=-0.5
3.
*Shell Section, elset=PhysicalSurfaceLOPATKI, material=Stal
1.5

*Boundary
PhysicalLineWLOT, 1, 1
PhysicalLineWLOT, 2, 2
PhysicalLineWLOT, 3, 3
PhysicalLineWLOT, 4, 4
PhysicalLineWLOT, 5, 5

*Step
*Static
0.5,1

*DLOAD
PhysicalSurfaceALL, CENTRIF,OBROTY,0.,0.,0.,0.,0.,-1.

*NODE FILE 
U, RF
*EL FILE
S,
*End Step
"""
    Info['obroty'] = str((float(Info['obroty']) *((2.0*np.pi)/60.))**2.)
    
    # Podmien wartosci w pliku wsadowym na wartosci pobrane z GUI, oraz GMSHa
    inpFile = inpFile.replace("GESTOSC",str(Info['gestosc']))
    inpFile = inpFile.replace("MYOUNG",str(Info['myoung']))
    inpFile = inpFile.replace("POISS",str(Info['poiss']))
    
    inpFile = inpFile.replace("G_WEW",str(Info['indSet']['g_wew']))
    inpFile = inpFile.replace("G_ZEW",str(Info['indSet']['g_zew']))
    inpFile = inpFile.replace("PODSTAWA",str(Info['indSet']['podstawa']))
    inpFile = inpFile.replace("LOPATKI",str(Info['indSet']['lopatki']))
    inpFile = inpFile.replace("WLOT",str(Info['indSet']['wlot']))
    inpFile = inpFile.replace("ALL",str(Info['indSet']['all']))
    
    inpFile = inpFile.replace("OBROTY",str(Info['obroty']))
    inpFile = inpFile.replace("NAZWA",str(Info['Obiekt']['nazwa']))
    
    # Stworz plik wsadowy do Calculixa
    with open('ccxInp.inp','w') as f:
        f.write(inpFile)