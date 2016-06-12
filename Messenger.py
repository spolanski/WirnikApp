# -*- coding: utf-8 -*-
"""
Created on Sat Feb 06 19:59:31 2016

@author: Slawek
"""

def main(dane,frt):
    """Funkcja glowna sluzaca do tworzenia geometrii, oraz operacji przy
    uzyciu GMSH'a i Calculix'a."""
    
    from SenderClass import Sender
    # Stworz gonca
    Goniec = Sender()
    Goniec.pobierzDane(dane)

    # Testuj dane
    Goniec.testujDane()
#==============================================================================
#   Wyslij parametry do funkcji obliczajacych polozenie punktow geometrii
#==============================================================================
    import objectGeometry
    objectGeometry.obliczPotrzebneParametry(Goniec)
    
#==============================================================================
#   Stworz geometrie na podstawie obliczonych parametrow    
#==============================================================================
    import gmshInputFile
    #geoWirnik, ccxText(indSet), stMesh = gmshInputFile.stworz(Goniec,frt)
    gmshInputFile.przygotujPlik(Goniec,frt)
    #Geo.r1,Geo.il_l,Geo.kLop_xyz,Geo.kolo_BC,Info['factor'],frt)
    
#==============================================================================
#   Wyslij geometrie do programu GMSH
#==============================================================================
    from SenderClass import SenderBrain    
    Brain = SenderBrain(Goniec)
    Brain.utworzGeometrie(pokazGmsh=False) 
    Brain.dyskretyzujGeometrie()   

#==============================================================================
#   Instrukcja warunkowa ktora pozwala na rozroznienie siatki do preprocessingu
#   od siatki do obliczen w Calculixie
#==============================================================================
    if frt == 'stl':
        Brain.wizualizacjaObiektu()

    if frt == 'inp':
        Brain.przygotujSymulacje()
        import calculix
        calculix.konwertujSiatke(Goniec)            
#==============================================================================
#       W tym miejscu nastepuje przygotowanie pliku wsadowego do Calculixa na 
#       na bazie pliku z GMSHa
#==============================================================================
        calculix.stworzPlikWsadowy(Goniec)
        
        Brain.rozwiazProblem(pokazWyniki=True)
    
    return 1

if __name__ == "__main__":
    main()
