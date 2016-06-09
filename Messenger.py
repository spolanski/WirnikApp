# -*- coding: utf-8 -*-
"""
Created on Sat Feb 06 19:59:31 2016

@author: Slawek
"""
import geomGmsh
import gPunktyWirnika as gPW
import operacjeInp as oI
import os



def posprzatajSmieci(Brain):
    Brain.usunPliki('ccxInp.cvg')
    Brain.usunPliki('ccxInp.dat')
    Brain.usunPliki('ccxInp.frd')
    Brain.usunPliki('ccxInp.inp')
    Brain.usunPliki('ccxInp.sta')
    Brain.usunPliki('spooles.out')

def main(dane,frt):
    
    from SenderClass import Sender
    # Stworz gonca
    Goniec = Sender()
    Goniec.pobierzDane(dane)
    
    wd = os.getcwd()
    
#==============================================================================
#    Pobierz dane z GUI
#==============================================================================
#==============================================================================
#     alfa = d['w_alfa']
#     print type(alfa)
#     r1 = d['prOtworu']
#     r2 = d['prLop']
#     r3 = d['prZewn']
#     r4 = d['prWyl']
#     il_l = d['ilLop']
#     b1 = d['beta_1']
#     b2 = d['beta_2']
#     h1 = d['wysLop']
#     h2 = d['naddatek']
#     h3 = d['wysWirnika']
#     R = d['prZaokrag']
#     factor = d['zag']
#     gmsh_dir = d['GMSH_DIR']
#     ccx_dir = d['CCX_DIR']
#     cgx_dir = d['CGX_DIR']
# 
#==============================================================================
    # Testuj dane
    Goniec.testujDane()
    W = Goniec.Bag.Geo
    I = Goniec.Bag.Info
#==============================================================================
#   Wyslij parametry do funkcji obliczajacych polozenie punktow geometrii
#==============================================================================
    kLop_xyz, kolo_BC = gPW.punktyWylotu(W.alfa,W.b1,W.b2,W.r2,W.r3,
                                         W.r4,W.h1,W.h2,W.h3,W.R)
#==============================================================================
#   Stworz geometrie na podstawie obliczonych parametrow    
#==============================================================================
    geoWirnik, ccxText, stMesh = geomGmsh.stworz(W.r1,W.il_l,kLop_xyz,
                                                 kolo_BC,I['factor'],frt)
    
#==============================================================================
#   Wyslij geometrie do programu GMSH
#==============================================================================
    from SenderClass import SenderBrain    
    Brain = SenderBrain(Goniec,geoWirnik)
    Brain.utworzGeometrie(pokazGmsh=False) 
    Brain.dyskretyzujGeometrie()   

#==============================================================================
#   Instrukcja warunkowa ktora pozwala na rozroznienie siatki do preprocessingu
#   od siatki do obliczen w Calculixie
#==============================================================================
    if frt == 'stl':
        Brain.wizualizacjaObiektu()

    if frt == 'inp':
        posprzatajSmieci(Brain)
        ccxText['nazwa'] = wd + '/' + geoWirnik['nazwa']
        ccxText['obroty'] = float(I['obroty'])
        ccxText['gestosc'] = I['gestosc']
        ccxText['poiss'] = I['poiss']
        ccxText['myoung'] = I['myoung']
        oI.mesh(ccxText, stMesh)
            
#==============================================================================
#       W tym miejscu nastepuje przygotowanie pliku wsadowego do Calculixa na 
#       na bazie pliku z GMSHa
#==============================================================================
        oI.calcInput(ccxText)
        
        Brain.rozwiazProblem(pokazWyniki=True)
    
    return 1

if __name__ == "__main__":
    main()
