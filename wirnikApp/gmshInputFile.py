# -*- coding: utf-8 -*-
"""
W tym pliku zawarta jest definicja wirnika, która zostanie zinterpretowana w programie GMSH, a następnie użyta jako plik wsadowy w programie Calculix.
"""
import numpy as np
from gmshClass import Part, PSurface, RSurface
 
def przygotujPlik(Goniec,frt):
    """
    Idea zawartej procedury polega na zgromadzeniu informacji o budowie geometrii w obiekcie klasy Part. Następnym krokiem jest zamianych uzyskanych danych na polecenia tekstowe, które są zrozumiałe przez program GSMH. Ze względu na skomplikowaną procedurę budowy pliku wsadowego, dodatkowe komentarze są zawarte w niniejszym skrypcie.

    :param Goniec: obiekt zawierający informacje odnośnie wymiarów geometrii, oraz sposobu jej dyskretyzacji.
    :type Goniec: Sender
    :param frt: zmienna określająca czy rezultatem przeprowadzanego procesu ma być wizualizacja geometrii czy też obliczenia numeryczne.
    :type frt: string
    """
    # Deklaracja zmiennych
    Geo = Goniec.Geo
    Info = Goniec.Info

    lop_XYZ = Geo.lopatka_XYZ
    zaokr   = Geo.zaokr
    il_l    = Geo.il_l
    factor  = Info['factor']
    kat_theta = -Geo.theta
    
    # Stwórz obiekt wirnika zawierąjacy wszystkie informacje mające zostać
    # przesłane do programu GMSH
    p = Part('wirnik')
    
    # Stwórz kontener na odpowiednie zbiory elementów skończonych
    Info['indSet'] = {}
    Info['structMesh'] = []

    # Stwórz punkt centralny      
    p.point(0.0,0.0,0.0)
#==============================================================================
#   KOŁO ZEWNETRZNE
#==============================================================================
    # Stwórz koło dzięki użyciu łuków
    st = p.prStart()                     #----> Wstaw wskaźnik
    # Stwórz punkt
    polLop = [0.0,lop_XYZ[0][1]]
    # Stwórz punkty poprzez rotacje pojedynczego punktu
    p.rotation(polLop,il_l)
    # Stwórz wektor pktyDKola zawierający punkty koła zewnętrznego
    pktyDKola = p.prEnd(st)             #----> Zwróć wskaźnik 
    
    st = p.prStart()                   #----> Wstaw wskaźnik
    # Stwórz koło używajac punkty zawarte w wektorze pktyDKola
    p.manyCircles(0,pktyDKola)
    # Zapisz koło zewnetrzne w wektorze lukiZewn
    lukiZewn = p.prEnd(st)            #----> Zwróć wskaźnik
    for i in lukiZewn:
        l_s = i.id
        # Podziel krawędź na segmenty
        podzial = str(int(10.0 * (1./float(factor))))
        p.text("Transfinite Line {%s} = %s Using Progression 1;" % (l_s,podzial))

#==============================================================================
#   Poniższa geometria zostala stworzona wg podobnego wzorca
#==============================================================================
#==============================================================================
#   KOŁO WEWNĘTRZNE
#==============================================================================
    lista = lop_XYZ[-2][0:2]
    st = p.prStart()
    p.rotation(lista,il_l)
    pktyMKola = p.prEnd(st)
    
    st = p.prStart()
    p.manyCircles(0,pktyMKola)
    lukiKola = p.prEnd(st)
    
#==============================================================================
#   PUNKTY POTRZEBNE DO STWORZENIA ŁOPATKI
#==============================================================================
    lista = lop_XYZ[-1][0:2]
    st = p.prStart()
    p.rotation(lista,il_l)
    pktyObrotu = p.prEnd(st)
        
#==============================================================================
#   TWORZENIE GEOMETRII ŁUKÓW
#==============================================================================
    st = p.prStart()
    # Stwórz krzywe, do których przyczepiona zostanie łopatka 
    for i in range(len(pktyObrotu)):
        p.circle(pktyMKola[i].id,
            pktyObrotu[i].id,
            pktyDKola[i].id)
    # Stwórz wektor krzywych
    lopatki = p.prEnd(st)

    # Dla danej ilości łopatek stwórz pętle krawędzi Line Loop a następnie
    # użyj danej pętli krawędzi do stworzenia płaszczyzny Plane Surface   
    pow_ind = []
    for i in range(il_l):
        p.lloop(pktyMKola[i].id,
                 lopatki[(i + 1) % (il_l)].id,
                -pktyDKola[i].id,
                -lopatki[i].id)
        p.psurf(p['czesci'][-1].id)
        pow_ind.append(p['czesci'][-1].id)

#==============================================================================
#   Tworzenie płaszczyzn w podstawie okręgu 
#==============================================================================
    # Stwórz punkty potrzebne do określenia najmniejszej średnicy. Proces 
    # tworzenia rozpocznij z rotacją wstępną równą kątowi theta
    st = p.prStart()
    malyPkt = [0.0,-Geo.r1]
    p.rotation(malyPkt,il_l,theta = kat_theta,z = 0.0)
    pkty = p.prEnd(st)
    
    # Stwórz okręgi na podstawie określonych wcześniej punktów
    st = p.prStart()
    p.manyCircles(0,pkty)
    wejscie = p.prEnd(st)
    # Poinformuj program o tym że wektor 'wejscie' powinien być wyszczegolniony
    # w pliku wyjściom z GMSH'a
    p.physical('Line',[i.id for i in wejscie])
    # Dodaj wektor 'wejscie' do czesci informacyjnej gonca
    Info['indSet']['wlot'] = (p['czesci'][-1].id)
    
    # Połącz liniami odpowiednie punkty
    st = p.prStart()
    for i in range(il_l):
        p.line([pkty[i].id,pktyMKola[i].id])
    lnSrod = p.prEnd(st)  
    
    # Stwórz płaszczyznę podstawy, oraz dodaj informacje o siatce 'quad'
    # do gońca
    for i in range(il_l):
        t = [wejscie[i].id,
            lnSrod[(i + 1) % (il_l)].id,
            lukiKola[i].id,
            lnSrod[i].id]

        p.lloop([t[0], t[1],
                 -t[2], -t[3]])
        p.psurf(p['czesci'][-1].id)
        id_surf = p['czesci'][-1].id
        # Dodaj informacje do gońca o siatce quad
        Info['structMesh'].append(id_surf)
        # Stwórz siatkę typu quad i użyj stopnia zagęszczenia 'factor'
        p.createStructuredMesh(t,id_surf,factor)
    
#==============================================================================
#   Utwórz zbiór zawierający elementy podstawy wirnika
#==============================================================================
    # Wyselekcjonuj z pośród wszystkich obiektów w obiekcie Part tylko te,
    # które są powierzchniami (Plane Surface)
    powPodstawy = filter(lambda x: type(x) == PSurface, p['czesci'])
    # Stwórz obiekty typu Physical dla uzyskanych płaszczyzn    
    p.physical('Surface',[i.id for i in powPodstawy])
    # Poinformuj gońca o nazwie obiektu Physical Surface
    Info['indSet']['podstawa'] = p['czesci'][-1].id

#==============================================================================
#   Poniższa geometria została stworzona wg wzorca przedstawionego wcześniej.
#   Ewentualne zmiany zostaną uwzględnione w postaci komentarza    
#==============================================================================
#==============================================================================
#   Tworzenie górnej części wirnika
#==============================================================================
    pktGorneL = []
    for i in lop_XYZ[:-1]:
        st = p.prStart()
        rt_pkt = [i[0],i[1]]
        p.rotation(punkt = rt_pkt, iloscPunktow = il_l, z=i[2])
        p.point(i[0],i[1],i[2])
        pktGorneL.append(p.prEnd(st))
    pktGorneL = (np.array(pktGorneL)).transpose()

    bspls = []
    for i in range(il_l):
        p1 = pktGorneL[i][0]
        p6 = pktGorneL[i][-1]
        st = p.prStart()
        # Stwórz splajn
        p.spline([j.id for j in pktGorneL[i]])
        bspls.append(p.prEnd(st)[0])
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
        p.createStructuredMesh([lopatki[i].id, l1, bs_ind, l2],surf_id,factor)

    p.point(0.0,0.0,lop_XYZ[-2][2])
    up_ind = p['czesci'][-1].id
   
    p.point(0.0,0.0,lop_XYZ[0][2])
    dn_ind = p['czesci'][-1].id
    
#==============================================================================
#   Stwórz zbiór i poinformuj gońca
#==============================================================================
    powLopatek = filter(lambda x: type(x) == RSurface, p['czesci'])
    p.physical('Surface',[i.id for i in powLopatek])
    Info['indSet']['lopatki'] = p['czesci'][-1].id
    
#==============================================================================
#   Górna część geometrii wirnika - pochylenie
#==============================================================================
    k_lacz = []
    for i in range(il_l):
        p.circle(pktGorneL[i][-1].id,
            up_ind,
            pktGorneL[(i + 1) % (il_l)][-1].id)
        k_lacz.append(p['czesci'][-1])
        gKolo = p['czesci'][-1].id  
        p.circle(pktGorneL[i][0].id,
            dn_ind,
            pktGorneL[(i + 1) % (il_l)][0].id)
        dKolo = p['czesci'][-1].id
        podzial = str(int(10.0 * (1./float(factor))))
        p.text("Transfinite Line {%s} = %s Using Progression 1;" % (dKolo,
            podzial))
        p.lloop(bspls[i].id,
                gKolo,
                -bspls[(i + 1) % (il_l)].id,
                -dKolo)
        p.rsurf([p['czesci'][-1].id])

#==============================================================================
#   Stwórz zbiór
#==============================================================================
    powGZ = filter(lambda x: type(x) == RSurface, p['czesci'])
    ind = len(powLopatek)
    powGZ = powGZ[ind:]
    p.physical('Surface',[i.id for i in powGZ])
    Info['indSet']['g_zew'] = p['czesci'][-1].id

#==============================================================================
#   Górna cześć geometrii wirnika - zaokrąglenie
#==============================================================================    
    top_pkt = []
    for i in zaokr:
        st = p.prStart()
        p.rotation([i[0],i[1]],il_l,z=i[2],theta=kat_theta)
        top_pkt.append(p.prEnd(st))
    top_pkt = (np.array(top_pkt)).transpose()

    p.point(0.0,0.0,zaokr[-1][2])
    up_ind = p['czesci'][-1].id
   
    spline_v = []
    kolo_hu = []
    for i in range(il_l):
        temp = [pktGorneL[i][-1].id]
        for j in top_pkt[i]: temp.append(j.id)
        p.spline(temp)
        spline_v.append(p['czesci'][-1])
        
        p.circle(top_pkt[i][-1].id,
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
        p.createStructuredMesh(t,id_surf,factor)
     
#==============================================================================
#   Stwórz zbiór
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
#   Definiuj wlaściwości geometrii, oraz siatki
#==============================================================================
    # Wyświetl powierzchnie w GMSH'u    
    p.text("Geometry.Surfaces = 1;")
    # Zdefiniuj algorytm użyty podczas dyskretyzacji - MeshAdapt
    p.text("Mesh.Algorithm = 1;")
    # Zdefiniuj stopień użytych elementów
    p.text("Mesh.ElementOrder = 2;")
    # Zdefiniuj wielkość charakterystyczną slużąca do poprawienia siatki
    p.text("Mesh.CharacteristicLengthFactor = " + factor + ";")
    # Użyj optymalizacji Lloyd'a w celu poprawienia jakości siatki
    # na powierzchniach
    p.text("Mesh.Lloyd = 1;")
    # Zapisz grupy elementow skończonych w pliku wyjsciowym GMSH'a
    p.text("Mesh.SaveGroupsOfNodes = 1;")
#==============================================================================
#   Miejsce w ktorym program rozpoznaje czy geometria ma być przechowywana w 
#   w celu jej wyświetlenia czy tez jako plik wsadowy do Calculixa    
#==============================================================================
    if frt == 'stl':
        p.text("Mesh.Format = 10;")
    if frt == 'inp':
        p.text("Mesh.Format = 39;")
    
    # Zdefiniuj zawartość pliku wsadowego GMSH'a
    p.writeInputFile()
    Info['Obiekt'] = p



