# -*- coding: utf-8 -*-
"""
Created on Sat Feb 06 19:59:31 2016

@author: Slawek

W tym pliku zawarta jest definicja wirnika ktora zostanie zinterpretowana w
programie GMSH a nastepnie uzyta jako plik wsadowy w programie Calculix
"""
import numpy as np
from gmshClass import Part, PSurface, RSurface
 
def przygotujPlik(Goniec,frt):
    """Funkcja sluzaca tworzeniu pliku wsadowego do GMSH'a."""
    
    # Deklaracja zmiennych
    Geo = Goniec.Geo
    Info = Goniec.Info
    
    lop_XYZ = Geo.lopatka_XYZ
    zaokr   = Geo.zaokr
    il_l    = Geo.il_l
    factor  = Info['factor']
    
    # Stworz obiekt wirnika zawierajacy wszystkie informacje majace zostac
    # przeslane do programu GMSH
    p = Part('wirnik')
    
    # Stworz kontener na odpowiednie zbiory elementow skonczonych
    Info['indSet'] = {}
    Info['structMesh'] = []

    # Stworz punkt centralny      
    p.pkt(0.0,0.0,0.0)
#==============================================================================
#   KOLO ZEWNETRZNE
#==============================================================================
    # Stworz kolo dzieki uzyciu lukow
    st = p.cnt_st()                     #----> Wstaw wskaznik
    # Stworz punkt
    polLop = [0.0,lop_XYZ[0][1]]
    # Stworz punkty poprzez rotacje pojedynczego punktu
    p.rotacja(polLop,il_l)
    # Stworz wektor pktyDKola zawierajacy punkty kola zewnetrznego
    pktyDKola = p.cnt_fnd(st)           #----> Zwroc wskaznik 
    
    st = p.cnt_st()                     #----> Wstaw wskaznik
    # Stworz kolo uzywajaca punkty zawarte w wektorze pktyDKola
    p.wieleKol(0,pktyDKola)
    # Zapisz kolo zewnetrzne w wektorze lukiZewn
    lukiZewn = p.cnt_fnd(st)            #----> Zwroc wskaznik
    for i in lukiZewn:
        l_s = i.id
        # Podziel krawedz na segmenty
        podzial = str(int(10.0 * (1./float(factor))))
        p.t("Transfinite Line {%s} = %s Using Progression 1;" % (l_s,podzial))

#==============================================================================
#   Ponizsza geometria zostala stworzona wg podobnego wzorca
#==============================================================================
#==============================================================================
#   KOLO WEWNETRZNE
#==============================================================================
    lista = lop_XYZ[-2][0:2]
    st = p.cnt_st()
    p.rotacja(lista,il_l)
    pktyMKola = p.cnt_fnd(st)
    
    st = p.cnt_st()
    p.wieleKol(0,pktyMKola)
    lukiKola = p.cnt_fnd(st)
    
#==============================================================================
#   PUNKTY POTRZEBNE DO STWORZENIA LOPATKI
#==============================================================================
    lista = lop_XYZ[-1][0:2]
    st = p.cnt_st()
    p.rotacja(lista,il_l)
    pktyObrotu = p.cnt_fnd(st)
        
#==============================================================================
#   TWORZENIE GEOMETRII LUKOW
#==============================================================================
    st = p.cnt_st()
    # Stworz krzywe, do ktorych przyczepiona zostanie lopatka 
    for i in range(len(pktyObrotu)):
        p.kolo(pktyMKola[i].id,
               pktyObrotu[i].id,
                pktyDKola[i].id)
    # Stworz wektor krzywych
    lopatki = p.cnt_fnd(st)

    # Dla danej ilosci lopatek stworz petle krawedzi Line Loop a nastepnie
    # uzyj danej petli krawedzi do stworzenia plaszczyzny Plane Surface   
    pow_ind = []
    for i in range(il_l):
        p.lloop(pktyMKola[i].id,
                 lopatki[(i + 1) % (il_l)].id,
                -pktyDKola[i].id,
                -lopatki[i].id)
        p.psurf(p['czesci'][-1].id)
        pow_ind.append(p['czesci'][-1].id)

#==============================================================================
#   Tworzenie plaszczyzn w podstawie okregu 
#==============================================================================
    # Na tym etapie zostana stworzone linie laczace punkt centralny wirnika
    # z poczatkiem lopatki. Aby to zrobic, nalezalo okreslic kat theta
    # przedstawiony w dokumentacji.    
    t1 = abs(lop_XYZ[-2][1])
    t2 = np.sqrt(lop_XYZ[-2][0]**2. + t1**2.)
    kat_theta = - np.arccos(t1/t2)   
    
    # Stworz punkty potrzebne do stworzenia najmniejszej srednicy. Proces 
    # tworzenia rozpocznij z rotacja wstepna rowna katowi theta
    st = p.cnt_st()
    malyPkt = [0.0,-Geo.r1]
    p.rotacja(malyPkt,il_l,theta = kat_theta,z = 0.0)
    pkty = p.cnt_fnd(st)
    
    # Stworz okregi na podstawie stworzonych wczesniej punktow
    st = p.cnt_st()
    p.wieleKol(0,pkty)
    wejscie = p.cnt_fnd(st)
    # Poinformuj program ze wektor 'wejscie' powinien byc wyszczegolniony
    # w pliku wyjsciom z GMSH'a
    p.physical('Line',[i.id for i in wejscie])
    # Dodaj wektor 'wejscie' do czesci informacyjnej gonca
    Info['indSet']['wlot'] = (p['czesci'][-1].id)
    
    # Polacz liniami odpowiednie punkty
    st = p.cnt_st()
    for i in range(il_l):
        p.line([pkty[i].id,pktyMKola[i].id])
    lnSrod = p.cnt_fnd(st)  
    
    # Stworz plaszczyzne podstawy, oraz dodaj informacje o siatce 'quad'
    # do gonca
    for i in range(il_l):
        t = [wejscie[i].id,
            lnSrod[(i + 1) % (il_l)].id,
            lukiKola[i].id,
            lnSrod[i].id]

        p.lloop([t[0], t[1],
                 -t[2], -t[3]])
        p.psurf(p['czesci'][-1].id)
        id_surf = p['czesci'][-1].id
        # Dodaj informacje do gonca o siatce quad
        Info['structMesh'].append(id_surf)
        # Stworz siatke typu quad i uzyj stopnia zageszczenia 'factor'
        p.structMesh(t,id_surf,factor)
    
#==============================================================================
#   Utworz zbior zawierajacy elementy podstawy wirnika
#==============================================================================
    # Wyselekcjonuj z posrod wszystkich obiektow w obiekcie Part tylko te, ktore
    # sa powierzchniami (Plane Surface)
    powPodstawy = filter(lambda x: type(x) == PSurface, p['czesci'])
    # Stworz obiekty typu Physical dla uzyskanych plaszczyzn    
    p.physical('Surface',[i.id for i in powPodstawy])
    # Poinformuj gonca o nazwie obiektu Physical Surface
    Info['indSet']['podstawa'] = p['czesci'][-1].id

#==============================================================================
#   Ponizsza geometria zostala tworzona wg wzorca przedstawionego wczesniej.
#   Ewentualne zmiana zostana uwzglednione w postaci komentarza    
#==============================================================================
#==============================================================================
#   Tworzenie gornej czesci wirnika
#==============================================================================
    pktGorneL = []
    for i in lop_XYZ[:-1]:
        st = p.cnt_st()
        rt_pkt = [i[0],i[1]]
        p.rotacja(punkt = rt_pkt, iloscPunktow = il_l, z=i[2])
        p.pkt(i[0],i[1],i[2])
        pktGorneL.append(p.cnt_fnd(st))
    pktGorneL = (np.array(pktGorneL)).transpose()

    bspls = []
    for i in range(il_l):
        p1 = pktGorneL[i][0]
        p6 = pktGorneL[i][-1]
        st = p.cnt_st()
        # Stworz splajn
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
        Info['structMesh'].append(surf_id)
        p.structMesh([lopatki[i].id, l1, bs_ind, l2],surf_id,factor)

    p.pkt(0.0,0.0,lop_XYZ[-2][2])
    up_ind = p['czesci'][-1].id
   
    p.pkt(0.0,0.0,lop_XYZ[0][2])
    dn_ind = p['czesci'][-1].id
    
#==============================================================================
#   Stworz zbior i poinformuj gonca
#==============================================================================
    powLopatek = filter(lambda x: type(x) == RSurface, p['czesci'])
    p.physical('Surface',[i.id for i in powLopatek])
    Info['indSet']['lopatki'] = p['czesci'][-1].id
    
#==============================================================================
#   Gorna czesci geometrii wirnika - pochylenie
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
#   Stworz zbior
#==============================================================================
    powGZ = filter(lambda x: type(x) == RSurface, p['czesci'])
    ind = len(powLopatek)
    powGZ = powGZ[ind:]
    p.physical('Surface',[i.id for i in powGZ])
    Info['indSet']['g_zew'] = p['czesci'][-1].id

#==============================================================================
#   Gorna czesci geometrii wirnika - zaokraglenie
#==============================================================================    
    top_pkt = []
    for i in zaokr:
        st = p.cnt_st()
        p.rotacja([i[0],i[1]],il_l,z=i[2],theta=kat_theta)
        top_pkt.append(p.cnt_fnd(st))
    top_pkt = (np.array(top_pkt)).transpose()

    p.pkt(0.0,0.0,zaokr[-1][2])
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
        Info['structMesh'].append(id_surf)
        p.structMesh(t,id_surf,factor)
     
#==============================================================================
#   Stworz Zbior
#==============================================================================
    powWszystkie = filter(lambda x: (type(x) == RSurface or type(x) == PSurface),
                        p['czesci'])
    ind = len(powLopatek) + len(powPodstawy) + len(powGZ)
    powGW = powWszystkie[ind:]
    
    p.physical('Surface',[i.id for i in powGW])
    Info['indSet']['g_wew'] = p['czesci'][-1].id
    
    p.physical('Surface',[i.id for i in powWszystkie])
    Info['indSet']['all'] = p['czesci'][-1].id

#==============================================================================
#   Definiuj wlasciwosci geometrii, oraz siatki
#==============================================================================
    # Wyswietl powierzchnie w GMSH'u    
    p.t("Geometry.Surfaces = 1;")
    # Zdefiniuj algorytm uzyty podczas dyskretyzacji - MeshAdapt
    p.t("Mesh.Algorithm = 1;")
    # Zdefiniuj stopien uzytych elementow
    p.t("Mesh.ElementOrder = 2;")
    # Zdefiniuj wielkosc charakterystyczna sluzaca do poprawienia siatki
    p.t("Mesh.CharacteristicLengthFactor = " + factor + ";")
    # Uzyj optymalizacji Lloyd'a w celu poprawienia jakosci siatki
    # na powierzchniach
    p.t("Mesh.Lloyd = 1;")
    # Zapisz grupy elementow skonczonych w pliku wyjsciowym GMSH'a
    p.t("Mesh.SaveGroupsOfNodes = 1;")
#==============================================================================
#   Miejsce w ktorym program rozpoznaje czy geometria ma byc przechowywana w 
#   w celu jej wyswietlenia czy tez jako plik wsadowy do Calculixa    
#==============================================================================
    if frt == 'stl':
        p.t("Mesh.Format = 10;")
    if frt == 'inp':
        p.t("Mesh.Format = 39;")
    
    # Zdefiniuj zawartosc pliku wsadowego GMSH'a
    p.napiszPlikWsadowy()
    Info['Obiekt'] = p
    
    return Info


