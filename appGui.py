# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import sys
import os

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

class EmittingStream(QtCore.QObject):

    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))
        
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.dane = {}
        
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1291, 813)
        
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))      
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        
        self.vtk_panel = QtGui.QFrame(self.tab)
        self.vtk_panel.setFrameShape(QtGui.QFrame.StyledPanel)
        self.vtk_panel.setFrameShadow(QtGui.QFrame.Raised)
        self.vtk_panel.setObjectName(_fromUtf8("vtk_panel"))
        self.verticalLayout.addWidget(self.vtk_panel)
        
        self.groupBox = QtGui.QGroupBox(self.tab)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.groupBox_2 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout_15 = QtGui.QVBoxLayout()
        self.verticalLayout_15.setObjectName(_fromUtf8("verticalLayout_15"))
        self.alfa = QtGui.QLineEdit(self.groupBox_2)
        self.alfa.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.alfa.sizePolicy().hasHeightForWidth())
        self.alfa.setSizePolicy(sizePolicy)
        self.alfa.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.alfa.setObjectName(_fromUtf8("alfa"))
        self.verticalLayout_15.addWidget(self.alfa)
        self.beta_1 = QtGui.QLineEdit(self.groupBox_2)
        self.beta_1.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.beta_1.sizePolicy().hasHeightForWidth())
        self.beta_1.setSizePolicy(sizePolicy)
        self.beta_1.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.beta_1.setObjectName(_fromUtf8("beta_1"))
        self.verticalLayout_15.addWidget(self.beta_1)
        self.beta_2 = QtGui.QLineEdit(self.groupBox_2)
        self.beta_2.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.beta_2.sizePolicy().hasHeightForWidth())
        self.beta_2.setSizePolicy(sizePolicy)
        self.beta_2.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.beta_2.setObjectName(_fromUtf8("beta_2"))
        self.verticalLayout_15.addWidget(self.beta_2)
        self.ilLop = QtGui.QLineEdit(self.groupBox_2)
        self.ilLop.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ilLop.sizePolicy().hasHeightForWidth())
        self.ilLop.setSizePolicy(sizePolicy)
        self.ilLop.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.ilLop.setObjectName(_fromUtf8("ilLop"))
        self.verticalLayout_15.addWidget(self.ilLop)
        self.gridLayout_2.addLayout(self.verticalLayout_15, 1, 5, 1, 1)
        self.verticalLayout_13 = QtGui.QVBoxLayout()
        self.verticalLayout_13.setObjectName(_fromUtf8("verticalLayout_13"))
        self.wysLop = QtGui.QLineEdit(self.groupBox_2)
        self.wysLop.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wysLop.sizePolicy().hasHeightForWidth())
        self.wysLop.setSizePolicy(sizePolicy)
        self.wysLop.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.wysLop.setObjectName(_fromUtf8("wysLop"))
        self.verticalLayout_13.addWidget(self.wysLop)
        self.wysWirnika = QtGui.QLineEdit(self.groupBox_2)
        self.wysWirnika.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wysWirnika.sizePolicy().hasHeightForWidth())
        self.wysWirnika.setSizePolicy(sizePolicy)
        self.wysWirnika.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.wysWirnika.setObjectName(_fromUtf8("wysWirnika"))
        self.verticalLayout_13.addWidget(self.wysWirnika)
        self.naddatek = QtGui.QLineEdit(self.groupBox_2)
        self.naddatek.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.naddatek.sizePolicy().hasHeightForWidth())
        self.naddatek.setSizePolicy(sizePolicy)
        self.naddatek.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.naddatek.setObjectName(_fromUtf8("naddatek"))
        self.verticalLayout_13.addWidget(self.naddatek)
        self.prZaokrag = QtGui.QLineEdit(self.groupBox_2)
        self.prZaokrag.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.prZaokrag.sizePolicy().hasHeightForWidth())
        self.prZaokrag.setSizePolicy(sizePolicy)
        self.prZaokrag.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.prZaokrag.setObjectName(_fromUtf8("prZaokrag"))
        self.verticalLayout_13.addWidget(self.prZaokrag)
        self.gridLayout_2.addLayout(self.verticalLayout_13, 1, 3, 1, 1)
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.label = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_7.addWidget(self.label)
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_7.addWidget(self.label_3)
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_7.addWidget(self.label_4)
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_7.addWidget(self.label_2)
        self.gridLayout_2.addLayout(self.verticalLayout_7, 1, 0, 1, 1)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.srOtworu = QtGui.QLineEdit(self.groupBox_2)
        self.srOtworu.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.srOtworu.sizePolicy().hasHeightForWidth())
        self.srOtworu.setSizePolicy(sizePolicy)
        self.srOtworu.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.srOtworu.setObjectName(_fromUtf8("srOtworu"))
        self.verticalLayout_8.addWidget(self.srOtworu)
        self.srZewn = QtGui.QLineEdit(self.groupBox_2)
        self.srZewn.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.srZewn.sizePolicy().hasHeightForWidth())
        self.srZewn.setSizePolicy(sizePolicy)
        self.srZewn.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.srZewn.setObjectName(_fromUtf8("srZewn"))
        self.verticalLayout_8.addWidget(self.srZewn)
        self.srWyl = QtGui.QLineEdit(self.groupBox_2)
        self.srWyl.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.srWyl.sizePolicy().hasHeightForWidth())
        self.srWyl.setSizePolicy(sizePolicy)
        self.srWyl.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.srWyl.setObjectName(_fromUtf8("srWyl"))
        self.verticalLayout_8.addWidget(self.srWyl)
        self.srLop = QtGui.QLineEdit(self.groupBox_2)
        self.srLop.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.srLop.sizePolicy().hasHeightForWidth())
        self.srLop.setSizePolicy(sizePolicy)
        self.srLop.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.srLop.setObjectName(_fromUtf8("srLop"))
        self.verticalLayout_8.addWidget(self.srLop)
        self.gridLayout_2.addLayout(self.verticalLayout_8, 1, 1, 1, 1)
        self.verticalLayout_14 = QtGui.QVBoxLayout()
        self.verticalLayout_14.setObjectName(_fromUtf8("verticalLayout_14"))
        self.label_13 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.verticalLayout_14.addWidget(self.label_13)
        self.label_14 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.verticalLayout_14.addWidget(self.label_14)
        self.label_15 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.verticalLayout_14.addWidget(self.label_15)
        self.label_16 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)
        self.label_16.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.verticalLayout_14.addWidget(self.label_16)
        self.gridLayout_2.addLayout(self.verticalLayout_14, 1, 2, 1, 1)
        self.verticalLayout_16 = QtGui.QVBoxLayout()
        self.verticalLayout_16.setObjectName(_fromUtf8("verticalLayout_16"))
        self.label_26 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_26.sizePolicy().hasHeightForWidth())
        self.label_26.setSizePolicy(sizePolicy)
        self.label_26.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_26.setObjectName(_fromUtf8("label_26"))
        self.verticalLayout_16.addWidget(self.label_26)
        self.label_17 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)
        self.label_17.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.verticalLayout_16.addWidget(self.label_17)
        self.label_18 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)
        self.label_18.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.verticalLayout_16.addWidget(self.label_18)
        self.label_19 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        self.label_19.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.verticalLayout_16.addWidget(self.label_19)
        self.gridLayout_2.addLayout(self.verticalLayout_16, 1, 4, 1, 1)
        self.verticalLayout_4.addWidget(self.groupBox_2)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.groupBox_3 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout_19 = QtGui.QVBoxLayout()
        self.verticalLayout_19.setObjectName(_fromUtf8("verticalLayout_19"))
        self.label_23 = QtGui.QLabel(self.groupBox_3)
        self.label_23.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.verticalLayout_19.addWidget(self.label_23)
        self.label_24 = QtGui.QLabel(self.groupBox_3)
        self.label_24.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_24.setObjectName(_fromUtf8("label_24"))
        self.verticalLayout_19.addWidget(self.label_24)
    
        self.gmsh_dir = QtGui.QLabel(self.groupBox_3)
        self.gmsh_dir.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.gmsh_dir.setObjectName(_fromUtf8("gmsh_dir"))
        self.verticalLayout_19.addWidget(self.gmsh_dir)
        self.calc_dir = QtGui.QLabel(self.groupBox_3)
        self.calc_dir.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.calc_dir.setObjectName(_fromUtf8("calc_dir"))        
        self.verticalLayout_19.addWidget(self.calc_dir)
        
        self.cgx_dir = QtGui.QLabel(self.groupBox_3)
        self.cgx_dir.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.cgx_dir.setObjectName(_fromUtf8("cgx_dir"))        
        self.verticalLayout_19.addWidget(self.cgx_dir)
       
        self.horizontalLayout_3.addLayout(self.verticalLayout_19)
        self.verticalLayout_20 = QtGui.QVBoxLayout()
        self.verticalLayout_20.setObjectName(_fromUtf8("verticalLayout_20"))
        self.zag = QtGui.QLineEdit(self.groupBox_3)
        self.zag.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zag.sizePolicy().hasHeightForWidth())
        self.zag.setSizePolicy(sizePolicy)
        self.zag.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.zag.setObjectName(_fromUtf8("zag"))
        self.verticalLayout_20.addWidget(self.zag)
        self.obroty = QtGui.QLineEdit(self.groupBox_3)
        self.obroty.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.obroty.sizePolicy().hasHeightForWidth())
        self.obroty.setSizePolicy(sizePolicy)
        self.obroty.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.obroty.setObjectName(_fromUtf8("obroty"))
        self.verticalLayout_20.addWidget(self.obroty)

        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.GMSH_DIR = QtGui.QLineEdit(self.groupBox_3)
        self.GMSH_DIR.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GMSH_DIR.sizePolicy().hasHeightForWidth())
        self.GMSH_DIR.setSizePolicy(sizePolicy)
        self.GMSH_DIR.setObjectName(_fromUtf8("GMSH_DIR"))
        self.gridLayout.addWidget(self.GMSH_DIR, 0, 0, 1, 1)
        self.CCX_DIR = QtGui.QLineEdit(self.groupBox_3)
        self.CCX_DIR.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CCX_DIR.sizePolicy().hasHeightForWidth())
        self.CCX_DIR.setSizePolicy(sizePolicy)
        self.CCX_DIR.setObjectName(_fromUtf8("CCX_DIR"))
        self.gridLayout.addWidget(self.CCX_DIR, 1, 0, 1, 1)
        
        self.CGX_DIR = QtGui.QLineEdit(self.groupBox_3)
        self.CGX_DIR.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CCX_DIR.sizePolicy().hasHeightForWidth())
        self.CGX_DIR.setSizePolicy(sizePolicy)
        self.CGX_DIR.setObjectName(_fromUtf8("CGX_DIR"))
        self.gridLayout.addWidget(self.CGX_DIR, 2, 0, 1, 1)
        
        self.toolButton = QtGui.QToolButton(self.groupBox_3)
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.toolButton.clicked.connect(lambda:
            self.openFileDialog('gmsh'))
        
        self.gridLayout.addWidget(self.toolButton, 0, 1, 1, 1)
        self.toolButton_2 = QtGui.QToolButton(self.groupBox_3)
        self.toolButton_2.setObjectName(_fromUtf8("toolButton_2"))
        self.toolButton_2.clicked.connect(lambda:
            self.openFileDialog('ccx'))
        self.gridLayout.addWidget(self.toolButton_2, 1, 1, 1, 1)
        
        self.toolButton_3 = QtGui.QToolButton(self.groupBox_3)
        self.toolButton_3.setObjectName(_fromUtf8("toolButton_2"))
        self.toolButton_3.clicked.connect(lambda:
            self.openFileDialog('cgx'))
        self.gridLayout.addWidget(self.toolButton_3, 2, 1, 1, 1)        
        self.verticalLayout_20.addLayout(self.gridLayout)

        self.horizontalLayout_3.addLayout(self.verticalLayout_20)
        self.horizontalLayout_4.addWidget(self.groupBox_3)
        self.groupBox_4 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.verticalLayout_17 = QtGui.QVBoxLayout()
        self.verticalLayout_17.setObjectName(_fromUtf8("verticalLayout_17"))
        self.label_20 = QtGui.QLabel(self.groupBox_4)
        self.label_20.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.verticalLayout_17.addWidget(self.label_20)
        self.label_21 = QtGui.QLabel(self.groupBox_4)
        self.label_21.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.verticalLayout_17.addWidget(self.label_21)
        self.label_22 = QtGui.QLabel(self.groupBox_4)
        self.label_22.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.verticalLayout_17.addWidget(self.label_22)
        self.horizontalLayout_5.addLayout(self.verticalLayout_17)
        self.verticalLayout_18 = QtGui.QVBoxLayout()
        self.verticalLayout_18.setObjectName(_fromUtf8("verticalLayout_18"))
        self.mYoung = QtGui.QLineEdit(self.groupBox_4)
        self.mYoung.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mYoung.sizePolicy().hasHeightForWidth())
        self.mYoung.setSizePolicy(sizePolicy)
        self.mYoung.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.mYoung.setObjectName(_fromUtf8("myoung"))
        self.verticalLayout_18.addWidget(self.mYoung)
        self.poiss = QtGui.QLineEdit(self.groupBox_4)
        self.poiss.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.poiss.sizePolicy().hasHeightForWidth())
        self.poiss.setSizePolicy(sizePolicy)
        self.poiss.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.poiss.setObjectName(_fromUtf8("poiss"))
        self.verticalLayout_18.addWidget(self.poiss)
        self.gestosc = QtGui.QLineEdit(self.groupBox_4)
        self.gestosc.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gestosc.sizePolicy().hasHeightForWidth())
        self.gestosc.setSizePolicy(sizePolicy)
        self.gestosc.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.gestosc.setObjectName(_fromUtf8("gestosc"))
        self.verticalLayout_18.addWidget(self.gestosc)
        self.horizontalLayout_5.addLayout(self.verticalLayout_18)
        self.horizontalLayout_4.addWidget(self.groupBox_4)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)
        self.pushButton = QtGui.QPushButton(self.groupBox)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.verticalLayout_5.addWidget(self.pushButton)
        self.verticalLayout.addWidget(self.groupBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.Monitor = QtGui.QWidget()
        self.Monitor.setObjectName(_fromUtf8("Monitor"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.Monitor)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        
        self.scrollArea = QtGui.QScrollArea(self.Monitor)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 963, 740))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.textEdit = QtGui.QTextEdit(self.scrollAreaWidgetContents)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.horizontalLayout_6.addWidget(self.textEdit)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_3.addWidget(self.scrollArea)
        
        self.calculix = QtGui.QPushButton(self.Monitor)
        self.calculix.setObjectName(_fromUtf8("calculix"))
        self.verticalLayout_3.addWidget(self.calculix)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.tabWidget.addTab(self.Monitor, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1009, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.beta_1.textChanged.connect(lambda:
            self.zmienDane(self.beta_1,'beta_1'))
        self.beta_2.textChanged.connect(lambda:
            self.zmienDane(self.beta_2,'beta_2'))
        self.ilLop.textChanged.connect(lambda:
            self.zmienDane(self.ilLop,'ilLop'))
        self.wysLop.textChanged.connect(lambda:
            self.zmienDane(self.wysLop,'wysLop'))
        self.wysWirnika.textChanged.connect(lambda:
            self.zmienDane(self.wysWirnika,'wysWirnika'))
        self.alfa.textChanged.connect(lambda:
            self.zmienDane(self.alfa,'alfa'))
        self.prZaokrag.textChanged.connect(lambda:
            self.zmienDane(self.prZaokrag,'prZaokrag'))
        self.srOtworu.textChanged.connect(lambda:
            self.zmienDane(self.srOtworu,'srOtworu'))
        self.srZewn.textChanged.connect(lambda:
            self.zmienDane(self.srZewn,'srZewn'))
        self.srWyl.textChanged.connect(lambda:
            self.zmienDane(self.srWyl,'srWyl'))
        self.srLop.textChanged.connect(lambda:
            self.zmienDane(self.srLop,'srLop'))
        self.mYoung.textChanged.connect(lambda:
            self.zmienDane(self.mYoung,'myoung'))
        self.poiss.textChanged.connect(lambda:
            self.zmienDane(self.poiss,'poiss'))
        self.gestosc.textChanged.connect(lambda:
            self.zmienDane(self.gestosc,'gestosc'))
        self.naddatek.textChanged.connect(lambda:
            self.zmienDane(self.naddatek,'naddatek'))
        self.obroty.textChanged.connect(lambda:
            self.zmienDane(self.obroty,'obroty'))
        self.zag.textChanged.connect(lambda:
            self.zmienDane(self.zag,'zag'))
        
        self.GMSH_DIR.textChanged.connect(lambda:
            self.zmienDane(self.GMSH_DIR,'GMSH_DIR'))
        self.CCX_DIR.textChanged.connect(lambda:
            self.zmienDane(self.CCX_DIR,'CCX_DIR'))
        self.CGX_DIR.textChanged.connect(lambda:
            self.zmienDane(self.CGX_DIR,'CGX_DIR'))
        self.tabWidget.setCurrentIndex(0)
        
        sys.stdout = EmittingStream(textWritten=self.pokazWynikiWMonitorze)        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def retranslateUi(self, MainWindow):
        fVal = QtGui.QDoubleValidator()
        iVal = QtGui.QIntValidator()
        sVal = QtGui.QRegExpValidator()
        
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.groupBox.setTitle(_translate("MainWindow", "Wirnik", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "Definicja geometrii", None))
        self.alfa.setText(_translate("MainWindow", "13.0", None))
        self.beta_1.setText(_translate("MainWindow", "33.0", None))
        self.beta_2.setText(_translate("MainWindow", "22.0", None))
        self.ilLop.setText(_translate("MainWindow", "9", None))
        self.wysLop.setText(_translate("MainWindow", "54.0", None))
        self.wysWirnika.setText(_translate("MainWindow", "100.0", None))
        self.naddatek.setText(_translate("MainWindow", "96.24", None))
        self.prZaokrag.setText(_translate("MainWindow", "37.0", None))
        self.label.setText(_translate("MainWindow", "Średnica otworu [mm]", None))
        self.label_3.setText(_translate("MainWindow", "Średnica zewnętrzna [mm]", None))
        self.label_4.setText(_translate("MainWindow", "Średnica u wylotu [mm]", None))
        self.label_2.setText(_translate("MainWindow", "Średnica do łopatek [mm]", None))
        self.srOtworu.setText(_translate("MainWindow", "24.0", None))
        self.srZewn.setText(_translate("MainWindow", "317.0", None))
        self.srWyl.setText(_translate("MainWindow", "206.0", None))
        self.srLop.setText(_translate("MainWindow", "225.0", None))
        self.label_13.setText(_translate("MainWindow", "Wysokość łopatki [mm]", None))
        self.label_14.setText(_translate("MainWindow", "Wysokość wirnika [mm]", None))
        self.label_15.setText(_translate("MainWindow", "Wysokość pod naddatek [mm]", None))
        self.label_16.setText(_translate("MainWindow", "Promień zaokrąglenia [deg]", None))
        self.label_26.setText(_translate("MainWindow", "Kąt alfa [deg]", None))
        self.label_17.setText(_translate("MainWindow", "Kąt beta 1 [deg]", None))
        self.label_18.setText(_translate("MainWindow", "Kąt beta 2 [deg]", None))
        self.label_19.setText(_translate("MainWindow", "Ilość łopatek", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "Inne", None))
        self.label_23.setText(_translate("MainWindow", "Stopień zagęszczenia siatki (0.0 - 1.0)", None))
        self.label_24.setText(_translate("MainWindow", "Prędkość obrotowa wirnika [obr/min]", None))
        self.zag.setText(_translate("MainWindow", "1.0", None))
        self.obroty.setText(_translate("MainWindow", "1500.0", None))
        self.groupBox_4.setTitle(_translate("MainWindow", "Właściwości materiałowe", None))
        self.label_20.setText(_translate("MainWindow", "Moduł Younga [MPa]", None))
        self.label_21.setText(_translate("MainWindow", "stała Poisson\'a [-]", None))
        self.label_22.setText(_translate("MainWindow", "gęstość materiału [tona/mm^3]", None))
        self.mYoung.setText(_translate("MainWindow", "2.1e5", None))
        self.poiss.setText(_translate("MainWindow", "0.33", None))
        self.gestosc.setText(_translate("MainWindow", "7.85e-9", None))
        self.pushButton.setText(_translate("MainWindow", "Stwórz!", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Preprocessor", None))
        self.calculix.setText(_translate("MainWindow", "Calculix!", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Monitor), _translate("MainWindow", "Monitor", None))
        
        self.gmsh_dir.setText(_translate("MainWindow", "Ścieżka do GMSH\'a", None))
        self.calc_dir.setText(_translate("MainWindow", "Ścieżka do CCX", None))
        self.cgx_dir.setText(_translate("MainWindow", "Ścieżka do CGX", None))

        self.GMSH_DIR.setText(_translate("MainWindow", ('gmsh'), None))

        self.CCX_DIR.setText(_translate("MainWindow", ('ccx'), None))
        self.CGX_DIR.setText(_translate("MainWindow", ('cgx'), None))
        self.toolButton.setText(_translate("MainWindow", "...", None))
        self.toolButton_2.setText(_translate("MainWindow", "...", None))                
        self.toolButton_3.setText(_translate("MainWindow", "...", None))
        
        self.beta_1.setValidator(fVal)        
        self.dane['beta_1'] = self.beta_1.text()
        self.beta_2.setValidator(fVal)
        self.dane['beta_2'] = self.beta_2.text()        
        self.ilLop.setValidator(iVal)        
        self.dane['ilLop'] = self.ilLop.text()        
        self.wysLop.setValidator(fVal)        
        self.dane['wysLop'] = self.wysLop.text()
        self.wysWirnika.setValidator(fVal)        
        self.dane['wysWirnika'] = self.wysWirnika.text()
        self.naddatek.setValidator(fVal)        
        self.dane['naddatek'] = self.naddatek.text() 
        self.alfa.setValidator(fVal)        
        self.dane['alfa'] = self.alfa.text()  
        self.prZaokrag.setValidator(fVal)        
        self.dane['prZaokrag'] = self.prZaokrag.text()
        self.srOtworu.setValidator(fVal)        
        self.dane['srOtworu'] = self.srOtworu.text()
        self.srZewn.setValidator(fVal)        
        self.dane['srZewn'] = self.srZewn.text()
        self.srWyl.setValidator(fVal)        
        self.dane['srWyl'] = self.srWyl.text()
        self.srLop.setValidator(fVal)        
        self.dane['srLop'] = self.srLop.text()
        self.mYoung.setValidator(fVal)        
        self.dane['myoung'] = self.mYoung.text()
        self.poiss.setValidator(fVal)        
        self.dane['poiss'] = self.poiss.text()        
        self.gestosc.setValidator(fVal)        
        self.dane['gestosc'] = self.gestosc.text()
        self.zag.setValidator(fVal)        
        self.dane['zag'] = self.zag.text()
        self.obroty.setValidator(fVal)        
        self.dane['obroty'] = self.obroty.text()
        self.GMSH_DIR.setValidator(sVal)
        self.dane['GMSH_DIR'] = self.GMSH_DIR.text()
        self.CCX_DIR.setValidator(sVal)
        self.dane['CCX_DIR'] = self.CCX_DIR.text()
        self.CGX_DIR.setValidator(sVal)
        self.dane['CGX_DIR'] = self.CGX_DIR.text()

    def zmienDane(self,obiekt,klucz):
        self.dane[klucz] = obiekt.text()
    
    def __del__(self):
        sys.stdout = sys.__stdout__

    def pokazWynikiWMonitorze(self, text):
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textEdit.setTextCursor(cursor)
        self.textEdit.ensureCursorVisible()
    
    def openFileDialog(self,string):
        directory = str(os.getcwd())
        fname = QtGui.QFileDialog.getOpenFileName(None,
            'Open file',
            directory)
        directory = QtCore.QFileInfo(fname).absolutePath()
        name = QtCore.QFileInfo(fname).baseName()
        full_path = directory + '/' + name
        if string == 'gmsh':
            self.GMSH_DIR.setText(full_path)
        if string == 'ccx':
            self.CCX_DIR.setText(full_path)
        if string == 'cgx':
            self.CGX_DIR.setText(full_path)
