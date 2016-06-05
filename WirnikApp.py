#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import vtk
from PyQt4 import QtCore, QtGui
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

#==============================================================================
# Sprobuj zaladowac kodowanie Unicode
#==============================================================================
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

#==============================================================================
# Klasa potrzebna do stworzenia GUI
#==============================================================================
class WirnikApp(QtGui.QMainWindow):
    def __init__(self, data_dir):
        super(WirnikApp, self).__init__()
        self.vtk_widget = None
        self.ui = None
        self.setup(data_dir)

    def setup(self, data_dir):
        import appGui
        self.ui = appGui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.vtk_widget = VtkWirnik(self.ui.vtk_panel, data_dir)
        self.ui.vtk_layout = QtGui.QHBoxLayout()
        self.ui.vtk_layout.addWidget(self.vtk_widget)
        self.ui.vtk_layout.setContentsMargins(0, 0, 0, 0)
        self.ui.vtk_panel.setLayout(self.ui.vtk_layout)
        self.ui.pushButton.clicked.connect(lambda: self.vtk_widget.zmienAktora(self.ui))
        self.ui.calculix.clicked.connect(lambda: self.vtk_widget.policz(self.ui))

    def initialize(self):
        self.vtk_widget.start()

#==============================================================================
# Klasa potrzebna do stworzenia okienka z wirnikiem
#==============================================================================
class VtkWirnik(QtGui.QFrame):
    def __init__(self, parent, data_dir):
        super(VtkWirnik, self).__init__(parent)

        interactor = QVTKRenderWindowInteractor(self)
        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(interactor)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        renderer = vtk.vtkRenderer()
        render_window = interactor.GetRenderWindow()
        render_window.AddRenderer(renderer)

        interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        render_window.SetInteractor(interactor)
        renderer.SetBackground(0.2, 0.2, 0.2)

        filename = "wirnik.stl"
        source = vtk.vtkSTLReader()
        source.SetFileName(filename)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(1, 1, 1)  # (R,G,B)
        renderer.AddActor(actor)

        renderer.GradientBackgroundOn()
        renderer.SetBackground(0.5, .9, 1)  # Jasny niebieski
        renderer.SetBackground2(1, 1, 1)  # Bialy
        renderer.ResetCamera()

        self.source = source
        self.mapper = mapper
        self.renderer = renderer
        self.interactor = interactor
        self.render_window = render_window

    def start(self):
        self.interactor.Initialize()
        self.interactor.Start()
    
#==============================================================================
#     def usunSmieci(symulacja = False):        
#         def usunPliki(nazwa):
#             try:
#                 os.remove(nazwa)
#             except OSError:
#                 pass
#         smieci = ['wirnik.wrl','wirnik.msh','wirnik.geo_unrolled',
#                   'LloydInit.pos']
#         
#         for i in smieci: usunPliki(i)
#         if symulacja == True:
#             symulacja = ['ccxInp.cvg','ccxInp.dat','ccxInp.frd','ccxInp.inp',
#                          'ccxInp.sta','spooles.out']
#             for i in symulacja: usunPliki(i)
#==============================================================================
        
    def zmienAktora(self, menu):
        import senderBrain       
        senderBrain.main(menu, 'stl')

        
        self.source.Modified()
        self.render_window.Render()

    def policz(self, menu):
        import main
        main.main(menu, 'inp')
        

if __name__ == "__main__":
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    app = QtGui.QApplication([])
    main_window = WirnikApp("volume")
    main_window.show()
    main_window.initialize()
    app.exec_()

