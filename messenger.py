# -*- coding: utf-8 -*-
"""
Created on Sat Feb 06 19:59:31 2016

@author: Slawek
"""

def main(dane,frt):
    """Funkcja glowna sluzaca do tworzenia geometrii, oraz operacji przy
    uzyciu GMSH'a i Calculix'a."""
    
    from senderClass import Sender
    # Stworz gonca
    Goniec = Sender()
    # Pobierz dane z GUI
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
    gmshInputFile.przygotujPlik(Goniec,frt)
    
#==============================================================================
#   Wyslij geometrie do programu GMSH
#==============================================================================
    from senderClass import SenderBrain    
    Brain = SenderBrain(Goniec)
    Brain.utworzGeometrie(pokazGmsh=False) 
    Brain.dyskretyzujGeometrie()   

#==============================================================================
#   Instrukcja warunkowa ktora pozwala na rozroznienie sygnalu od uzytkownika 
#   wyslanego w celu wizualizacji wynikow od sygnalu z prosba o rozpoczecie
#   symulacji
#==============================================================================
    if frt == 'stl':
        # Wizualizuj obiekt
        Brain.wizualizacjaObiektu()

    if frt == 'inp':
        # Usun pozostalosci po poprzedniej symulacji jesli istnieja
        Brain.przygotujSymulacje()
        
        import calculix
        # Przystosuj siatke w pliku wsadowym do Calculixa
        calculix.konwertujSiatke(Goniec)
        # Stworz plik wsadowy do Calculixa
        calculix.stworzPlikWsadowy(Goniec)
        # Rozwiaz problem przy uzyciu Calculixa i zaprezentuj wyniki
        Brain.rozwiazProblem(pokazWyniki=True)
    return 1

if __name__ == "__main__":
    main()
