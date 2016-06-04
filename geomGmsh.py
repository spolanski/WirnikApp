# -*- coding: utf-8 -*-
"""
Created on Sat Feb 06 19:59:31 2016

@author: Slawek

W tym pliku zawarta jest definicja wirnika ktora zostanie zinterpretowana w
programie GMSH a nastepnie uzyta jako plik wsadowy w programie Calculix
"""
import numpy as np
from klasa import Part, PSurface, RSurface
 
def stworz(r1,il_l,kLop_xyz,kolo_BC,factor,frt):
    p = Part('wirnik')
    indSet = {}
    structMesh = []
    
    t1 = abs(kLop_xyz[-2][1])
    t2 = np.sqrt(kLop_xyz[-2][0]**2. + t1**2.)
    kat_theta = - np.arccos(t1/t2)
    
    p.pkt(0.0,0.0,0.0)
#==============================================================================
#     KOLO ZEWNETRZNE
#==============================================================================
    st = p.cnt_st()         #----> Wstaw wskaznik
    polLop = [0.0,kLop_xyz[0][1]]
    p.rotacja(polLop,il_l)
    pktyDKola = p.cnt_fnd(st)         #----> Zwroc wskaznik 
    
    st = p.cnt_st()         #----> Wstaw wskaznik
    p.wieleKol(0,pktyDKola)
    lukiZewn = p.cnt_fnd(st)         #----> Zwroc wskaznik
    for i in lukiZewn:
        l_s = i.id
        podzial = str(int(10.0 * (1./float(factor))))
        p.t("Transfinite Line {%s} = %s Using Progression 1;" % (l_s,podzial))

#==============================================================================
#     KOLO WEWNETRZNE
#==============================================================================
    lista = kLop_xyz[-2][0:2]
    st = p.cnt_st()         #----> Wstaw wskaznik
    p.rotacja(lista,il_l)
    pktyMKola = p.cnt_fnd(st)         #----> Zwroc wskaznik
    
    st = p.cnt_st()
    p.wieleKol(0,pktyMKola)
    lukiKola = p.cnt_fnd(st)
    
#==============================================================================
#     PUNKTY POTRZEBNE DO STWORZENIA LOPATKI
#==============================================================================
    lista = kLop_xyz[-1][0:2]
    st = p.cnt_st()         #----> Wstaw wskaznik
    p.rotacja(lista,il_l)
    pktyObrotu = p.cnt_fnd(st)         #----> Zwroc wskaznik
        
#==============================================================================
#     TWORZENIE LUKOW
#==============================================================================
    st = p.cnt_st()         #----> Wstaw wskaznik
    for i in range(len(pktyObrotu)):
        p.kolo(pktyMKola[i].id,
               pktyObrotu[i].id,
                pktyDKola[i].id)
    lopatki = p.cnt_fnd(st)         #----> Zwroc wskaznik
    
    pow_ind = []    
    for i in range(il_l):
        p.lloop(pktyMKola[i].id,
                 lopatki[(i + 1) % (il_l)].id,
                -pktyDKola[i].id,
                -lopatki[i].id)
        p.psurf(p['czesci'][-1].id)
        pow_ind.append(p['czesci'][-1].id)
   
    st = p.cnt_st()
    malyPkt = [0.0,-r1]
    p.rotacja(malyPkt,il_l,0.0,kat_theta)
    pkty = p.cnt_fnd(st)
    
    st = p.cnt_st()
    p.wieleKol(0,pkty)
    wejscie = p.cnt_fnd(st)
    p.physical('Line',[i.id for i in wejscie])
    indSet['wlot'] = (p['czesci'][-1].id)
    
    st = p.cnt_st()
    for i in range(il_l):
        p.line([pkty[i].id,pktyMKola[i].id])
    lnSrod = p.cnt_fnd(st)  
    
    for i in range(il_l):
        t = [wejscie[i].id,
            lnSrod[(i + 1) % (il_l)].id,
            lukiKola[i].id,
            lnSrod[i].id]

        p.lloop([t[0], t[1],
                 -t[2], -t[3]])
        p.psurf(p['czesci'][-1].id)
        id_surf = p['czesci'][-1].id
        structMesh.append(id_surf)
        p.structMesh(t,id_surf,factor)
    
#==============================================================================
#       Stworz zbior
#==============================================================================
    powPodstawy = filter(lambda x: type(x) == PSurface, p['czesci'])
    p.physical('Surface',[i.id for i in powPodstawy])
    indSet['podstawa'] = p['czesci'][-1].id
    
#==============================================================================
#       Tworzenie gornej czesci wirnika
#==============================================================================
    pktGorneL = []
    for i in kLop_xyz[:-1]:
        st = p.cnt_st()
        p.rotacja([i[0],i[1]],il_l,z=i[2])
        p.pkt(i[0],i[1],i[2])
        pktGorneL.append(p.cnt_fnd(st))
    pktGorneL = (np.array(pktGorneL)).transpose()

    bspls = []
    for i in range(il_l):
        p1 = pktGorneL[i][0]
        p6 = pktGorneL[i][-1]
        st = p.cnt_st()
        p.spline([j.id for j in pktGorneL[i]])
        bspls.append(p.cnt_fnd(st)[0])
        bs_ind = p['czesci'][-1].id
        
        p.line([p1.id,pktyDKola[i].id])
        l1 = p['czesci'][-1].id
        p.line([p6.id,pktyMKola[i].id])
        l2 = p['czesci'][-1].id
        
        p.lloop(lopatki[i].id, -l1, bs_ind, l2)
        loop_id = p['czesci'][-1].id
        p.rsurf([loop_id])
        
        surf_id = p['czesci'][-1].id
        structMesh.append(surf_id)
        p.structMesh([lopatki[i].id, l1, bs_ind, l2],surf_id,factor)

    p.pkt(0.0,0.0,kLop_xyz[-2][2])
    up_ind = p['czesci'][-1].id
   
    p.pkt(0.0,0.0,kLop_xyz[0][2])
    dn_ind = p['czesci'][-1].id
    
#==============================================================================
#     Stworz zbior
#==============================================================================
    powLopatek = filter(lambda x: type(x) == RSurface, p['czesci'])
    p.physical('Surface',[i.id for i in powLopatek])
    indSet['lopatki'] = p['czesci'][-1].id
    
#==============================================================================
#     Gorna czesci
#==============================================================================
    k_lacz = []
    for i in range(il_l):
        p.kolo(pktGorneL[i][-1].id,
               up_ind,
               pktGorneL[(i + 1) % (il_l)][-1].id)
        k_lacz.append(p['czesci'][-1])
        gKolo = p['czesci'][-1].id  
        p.kolo(pktGorneL[i][0].id,
               dn_ind,
               pktGorneL[(i + 1) % (il_l)][0].id)
        dKolo = p['czesci'][-1].id
        podzial = str(int(10.0 * (1./float(factor))))
        p.t("Transfinite Line {%s} = %s Using Progression 1;" % (dKolo,
            podzial))
        p.lloop(bspls[i].id,
                gKolo,
                -bspls[(i + 1) % (il_l)].id,
                -dKolo)
        p.rsurf([p['czesci'][-1].id])

#==============================================================================
#     Stworz zbior
#==============================================================================
    powGZ = filter(lambda x: type(x) == RSurface, p['czesci'])
    ind = len(powLopatek)
    powGZ = powGZ[ind:]
    p.physical('Surface',[i.id for i in powGZ])
    indSet['g_zew'] = p['czesci'][-1].id

#==============================================================================
#   WYLOT
#==============================================================================    
    top_pkt = []
    for i in kolo_BC:
        st = p.cnt_st()
        p.rotacja([i[0],i[1]],il_l,z=i[2],theta=kat_theta)
        top_pkt.append(p.cnt_fnd(st))
        
        
    top_pkt = (np.array(top_pkt)).transpose()

    p.pkt(0.0,0.0,kolo_BC[-1][2])
    up_ind = p['czesci'][-1].id
   

    spline_v = []
    kolo_hu = []
    for i in range(il_l):
        temp = [pktGorneL[i][-1].id]
        for j in top_pkt[i]: temp.append(j.id)
        p.spline(temp)
        spline_v.append(p['czesci'][-1])
        
        
        p.kolo(top_pkt[i][-1].id,
               up_ind,
               top_pkt[(i + 1) % (il_l)][-1].id)
        kolo_hu.append(p['czesci'][-1])

    for i in range(il_l):
        t = [k_lacz[i].id,
             spline_v[(i + 1) % (il_l)].id,
             kolo_hu[i].id,
             spline_v[i].id]
        p.lloop(t[0], t[1], -t[2], -t[3])
        p.rsurf([p['czesci'][-1].id])
        id_surf = p['czesci'][-1].id
        structMesh.append(id_surf)
        p.structMesh(t,id_surf,factor)
     
#==============================================================================
#     Stworz Zbior
#==============================================================================
    powWszystkie = filter(lambda x: (type(x) == RSurface or type(x) == PSurface),
                        p['czesci'])
    ind = len(powLopatek) + len(powPodstawy) + len(powGZ)
    powGW = powWszystkie[ind:]
    
    p.physical('Surface',[i.id for i in powGW])
    indSet['g_wew'] = p['czesci'][-1].id
    
    p.physical('Surface',[i.id for i in powWszystkie])
    indSet['all'] = p['czesci'][-1].id

    p.t("Geometry.Surfaces = 1;")
    p.t("Mesh.Algorithm = 1;")
    p.t("Mesh.ElementOrder = 2;")
    p.t("Mesh.CharacteristicLengthFactor = " + factor + ";")
    p.t("Mesh.Lloyd = 1;")

#==============================================================================
#   Miejsce w ktorym program rozpoznaje czy geometria ma byc przechowywana w 
#   w celu jej wyswietlenia czy tez jako plik wsadowy do Calculixa    
#==============================================================================
    if frt == 'stl':
        p.t("Mesh.Format = 10;")
    if frt == 'inp':
        p.t("Mesh.Format = 39;")
    
    p.t("Mesh.SaveGroupsOfNodes = 1;")
    

    p.napiszTekst()
    
    return p, indSet, structMesh


