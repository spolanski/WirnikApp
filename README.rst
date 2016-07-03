*********
WirnikApp
*********

Projekt stworzony na potrzeby mojej pracy magisterskiej.
########################################################

Potrzebne do uruchomienie skryptu:
	- komenda -> python wirnikApp.py
	- GMSH 2.12
	- Calculix 2.7
	Windows:
		- zainstaluj Python(x,y)
		- uruchom skrypt wirnikApp.py
	Linux:
		- potrzebne moduly: python-vtk, subprocess, numpy, scipy, pyqt4
		- moze byc potrzebne ustawienie chmod u+x gmsh w folderze Software
		- uruchom skrypt wirnikApp.py


Sposób otwierania programów w programie przedstawiony na video:
	- Uruchamianie programu pod Linuxem - https://youtu.be/xUxkJkCM8zA
	- Uruchamianie programu pod Windowsem - https://youtu.be/viwu7dmtKDI

Dobrym nawykiem jest monitorowanie konsoli Python'a oraz Menedzera Zadan(aktualnie rozpoczetych procesow).

*** Uwaga dla użytkowników Windows'a ***

Aby wyłączyć graficzne środowisko Calculixa należy najechać kursorem myszki na okienko z rezultatami i wpisać komendę 'quit' lub wybrać opcję QUIT z menu. W przeciwnym razie, program cgx.exe będzie widniał w menedżerze zadań. Problem nie występuje podczas pracy w środowisku Linux.

