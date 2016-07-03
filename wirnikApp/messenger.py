# -*- coding: utf-8 -*-
"""
W niniejszym pliku wykonywane są wszystkie operacje związane z tworzeniem modelu numerycznego, oraz rozwiązywanie założonego problemu. 

Skrypt wykorzystuje ideę gońca - zostaje stworzony obiekt zawierający informacje o geometrii, warunkach brzegowych, lokalizacji GMSH'a i Calculix. Tak określony kontener na informacje zostaje wykorzystany w dalszych modułach dzięki czemu uzyskuje się lepszą przejrzystość i zwartość kodu.
"""
def main(dane,frt):
    """
    Funkcja służąca do tworzenia geometrii, oraz przeprowadzania operacji przy
    użyciu GMSH'a i Calculix'a.

    :param dane: kontener zawierający dane pobrane z GUI. Wartości w kontenerze
        zapisane są w formacie klucz (typ string) : wartość (typ string).
    :type dane: dictionary
    :param frt: zmienna decydująca o tym czy użytkownik chce zmienić wizualizację obiektu czy też uruchomić symulację. Zmienna przyjmuje wartości *stl* lub *inp*. W przypadku pierwszej opcji wykonywane są operacje mające na celu zmianę wyświetlanego obiektu. Wartość *inp* odpowiada za uruchomienie symulacji.
    :type frt: string

    :return: Funkcja zwraca wartość True lub False określając tym samy poprawność wykonanych operacji
    :rtype: bool
    """
    from senderClass import Sender
    # Stworz gońca
    Goniec = Sender()
    # Pobierz dane z GUI
    Goniec.pobierzDane(dane)
    # Testuj dane
    Goniec.testujDane()
#==============================================================================
#   Wyślij parametry do funkcji obliczających położenie punktów geometrii
#==============================================================================
    import objectGeometry
    objectGeometry.obliczWymaganeParametry(Goniec)
#==============================================================================
#   Stwórz geometrię na podstawie obliczonych parametrów    
#==============================================================================
    import gmshInputFile
    gmshInputFile.przygotujPlik(Goniec,frt)
#==============================================================================
#   Wyślij geometrię do programu GMSH
#==============================================================================
    from senderClass import SenderBrain
    # Przekaż wiadomości z gońca do obiektu wykonującego operacje na programach zewnętrznych 
    Brain = SenderBrain(Goniec)
    Brain.utworzGeometrie(pokazGmsh=False) 
    Brain.dyskretyzujGeometrie()   
#==============================================================================
#   Instrukcja warunkowa która pozwala na rozróżnienie sygnału wysłanego w celu
#   wizualizacji wyników od sygnału z prośbą o rozpoczęcie symulacji
#==============================================================================
    if frt == 'stl':
        # Wizualizuj obiekt
        Brain.wizualizacjaObiektu()
    if frt == 'inp':
        # Usun pozostalosci po poprzedniej symulacji jeśli istnieją
        Brain.przygotujSymulacje()
        
        import calculix
        # Przystosuj siatke z pliku wsadowego do użycia w Calulixie
        calculix.konwertujSiatke(Goniec)
        # Stwórz plik wsadowy do Calculixa
        calculix.stworzPlikWsadowy(Goniec)
        # Rozwiąż problem przy użyciu Calculixa i zaprezentuj wyniki
        Brain.rozwiazProblem(pokazWyniki=True)
    return True

if __name__ == "__main__":
    main()
