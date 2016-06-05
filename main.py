# -*- coding: utf-8 -*-
"""
Created on Sat Feb 06 19:59:31 2016

@author: Slawek
"""
from klasa import Gmsh
import geomGmsh
import gPunktyWirnika as gPW
import operacjeInp as oI
import os

def main(menu,frt):
    d = menu.dane    
    wd = os.getcwd()
    
    def usunPliki(nazwa):
        try:
            os.remove(nazwa)
        except OSError:
            pass
    
    usunPliki('ccxInp.cvg')
    usunPliki('ccxInp.dat')
    usunPliki('ccxInp.frd')
    usunPliki('ccxInp.inp')
    usunPliki('ccxInp.sta')
    usunPliki('spooles.out')

#==============================================================================
#    Pobierz dane z GUI
#==============================================================================
    
    alfa = float(d['alfa'])
    r1 = float(d['srOtworu'])/2.
    r2 = float(d['srLop'])/2.
    r3 = float(d['srZewn'])/2.
    r4 = float(d['srWyl'])/2.
    il_l = int(d['ilLop'])
    b1 = float(d['beta_1'])
    b2 = float(d['beta_2'])
    h1 = float(d['wysLop'])
    h2 = float(d['naddatek'])
    h3 = float(d['wysWirnika'])
    R = float(d['prZaokrag'])
    factor = str(d['zag'])
    
    gmsh_dir = str(d['GMSH_DIR'])
    if gmsh_dir == '...':
        gmsh_dir = 'gmsh'
    
    ccx_dir = str(d['CCX_DIR'])
    if ccx_dir == '...':
        ccx_dir = 'ccx'
    
    cgx_dir = str(d['CGX_DIR'])
    if cgx_dir == '...':
        cgx_dir = 'cgx'    
    
#==============================================================================
#   Wyjatki
#==============================================================================
    if not (r1 <= r2 <= r3):
        text = "Srednica otworu, srednica do lopatek i srednica zewnetrzna \
            jest zle dobrana"
        raise ValueError(text)

    if r4 >= r3:
        text = "Srednica wylotu jest nieodpowiednia do srednicy zewnetrznej"
        raise ValueError(text)

    if r4 >= r3:
        text = "Srednica wylotu jest nieodpowiednia do srednicy zewnetrznej"
        raise ValueError(text)
    
    if h3-h2 < 0.0 :
        text = "Wartosc naddatku nieprawidlowa"
        raise ValueError(text)

    if il_l < 2:
        text = "Wirnik musi zawierac co najmniej dwie lopatki!"
        raise ValueError(text)
#==============================================================================
#   Wyslij parametry do funkcji obliczajacych polozenie punktow geometrii
#==============================================================================
    kLop_xyz, kolo_BC = gPW.punktyWylotu(alfa,b1,b2,r2,r3,r4,h1,h2,h3,R)
#==============================================================================
#   Stworz geometrie na podstawie obliczonych parametrow    
#==============================================================================
    geoWirnik, ccxText, stMesh = geomGmsh.stworz(r1,il_l,kLop_xyz,
                                                 kolo_BC,factor,frt)
    # Pobierz nazwe wirnika
    n = geoWirnik['nazwa']
    
#==============================================================================
#   Wyslij geometrie do programu GMSH
#==============================================================================
    gmsh = Gmsh(geoWirnik,wd,gmsh_dir)
    gmsh.napiszGeo()
    
    # W przypadku usuniecia wartosci true bedzie wyskawilo okienko GMSH
    gmsh.przeslijGeometrie(True) 

    cmd = n + '.geo ' + '-saveall -2'
#==============================================================================
#   W tym miejscu geometria zostaje zamieniona na siatke elementow skonczonych    
#==============================================================================
    gmsh.gmshCmd(cmd)
    
#==============================================================================
#   Instrukcja warunkowa ktora pozwala na rozroznienie siatki do preprocessingu
#   od siatki do obliczen w Calculixie
#==============================================================================
    if frt == 'stl':
        cmd = n + '.msh ' + '-o ' + n + '.wrl -format wrl -0'
        print cmd
        gmsh.gmshCmd(cmd)
        cmd = n + '.wrl ' + '-o ' + n + '.stl -format stl -0'
        print cmd
        gmsh.gmshCmd(cmd)

    if frt == 'inp':       
        ccxText['nazwa'] = wd + '/' + n
        ccxText['obroty'] = float(d['obroty'])
        ccxText['gestosc'] = float(d['gestosc'])
        ccxText['poiss'] = float(d['poiss'])
        ccxText['myoung'] = float(d['myoung'])        
        oI.mesh(ccxText, stMesh)
            
#==============================================================================
#       W tym miejscu nastepuje przygotowanie pliku wsadowego do Calculixa na 
#       na bazie pliku z GMSHa
#==============================================================================
        oI.calcInput(ccxText)
        
        # Rozwiaz problem
        solve = ccx_dir + ' ' + wd + '/ccxInp'
        gmsh.cmd(solve)
        
        # Wyswietl rozwiazanie w Calculixie
        show = cgx_dir + ' ' + wd + '/ccxInp.frd'
        gmsh.cgx(show)
    
    return 1

if __name__ == "__main__":
    main()
