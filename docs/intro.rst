Wprowadzenie
============

Do poprawnego uruchomienia aplikacji należy posiadać następujące oprogramowanie:
	* GMSH 2.10 lub nowsze
	* Calculix 2.7 lub nowsze

W przypadku programu Calculix nie stwierdzono wpływu starszej wersji na otrzymywane wyniki. Jeśli chodzi o aplikację GMSH problem pojawia się przy użyciu wersji 2.8 lub starszej, w której ustawienia domyślne generowania siatki są różne od tych zastosowanych w nowszej wersji przez co jakość dyskretyzacji jest niższa.

Aplikacja została napisana przy użyciu języka programowania jakim jest Python z wykorzystaniem następujących modułów:
	* Subprocess
	* NumPy/SciPy
	* Python-Vtk
	* PyQt4

W przypadku próby uruchomienia skryptu pod systemem Linux, instalacja repozytoriów polega na pobraniu powyższych repozytoriów. Uruchomienie WirnikApp na systemie Windows sprawia więcej kłopotów, gdyż instalacja modułu 'Python-Vtk' jest bardziej skomplikowana. Najłatwiejszym sposobem na ominięcie tej niedogodności jest instalacja gotowego zestawu oprogramowania Python(x,y). Pakiet ten zawiera wszystkie wymienione moduły, oraz wiele innych poszerzających zastosowanie Python'a.

Program WirnikApp uruchamiany jest poprzez otwarcie lini komend w folderze głównym aplikacji oraz wpisanie komendy *python wirnikApp*. W momencie pokazania się menu głównego użytkownik ma możliwość zdefiniowania geometrii wirnika, jakości siatki elementów skończonych czy rodzaju materiału. Jeśli WirnikApp został uruchomiony pod systemem Linux wtedy pozostawienie wartości domyślnych w rubrykach zawierających lokalizacje GMSHa i Calculixa będzie funkcjonowało poprawnie. Jest tak, dlatego iż lokalizacja zainstalowanych programów w systemie Linux jest dostępna bezpośrednio po wpisaniu nazwy programu do linii komand. Podczas próby uruchomienia aplikacji pod systemem Windows, lokalizacja preprocessor'a i solver'a musi zostać zdefiniowana przed uruchomieniem polecania wizualizacji lub obliczeń.

W celu wizualizacji geometrii wirnika stworzonego w oparciu o zdefiniowane uprzednio dane należy kliknąć przycisk 'Stwórz!'. Jak tylko przycisk zostanie naciśnięty, 

.. figure:: ./image/Diagram.png
    :align: center
    :alt: Diagram
    :figclass: align-center
    :scale: 95%

    Diagram przedstawiający w jaki sposób działa aplikacja.