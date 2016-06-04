# WirnikApp
Projekt stworzony na potrzeby mojej pracy magisterskiej.

Potrzebne do uruchomienie skryptu:
- komenda -> python vtkView.py
- GMSH 2.12
- Calculix 2.7

Sposób otwierania programów w programie przedstawiony na video:
- [Uruchamianie programu pod Linuxem](https://youtu.be/xUxkJkCM8zA)
- [Uruchamianie programu pod Windowsem](https://youtu.be/viwu7dmtKDI)

Windows:
- zainstaluj Python(x,y)
- uruchom skrypt vtkView.py

Linux:
- potrzebne moduly: python-vtk, subprocess, numpy, scipy, pyqt4
- moze byc potrzebne ustawienie chmod u+x gmsh w folderze Software
- uruchom skrypt vtkView.py

Dobrym nawykiem jest monitorowanie konsoli Python'a oraz Menedzera Zadan(aktualnie rozpoczetych procesow).

*** Uwaga dla uzytkownikow Windows'a ***

Aby wyłączyć graficzne środowisko Calculixa należy najechać kursorem myszki na okienko z rezultatami i wpisać komendę 'quit' lub wybrać opcję QUIT z menu. W przeciwnym razie, program cgx.exe będzie widniał w menedżerze zadań. Problem nie występuje podczas pracy w środowisku Linux.

