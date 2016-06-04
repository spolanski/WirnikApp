# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 21:39:43 2016

@author: Slawek

W tym pliku zawarte sa wszystkie funkcje ktore zostaly uzyte do obliczen
polozenia poszczegolnych punktow wirnika. W tym celu zostal wykorzystany 
modul SymPy, ktory pozwala na obliczenia z bardzo duza dokladnoscia.
"""
import numpy as np
import sympy
import sympy.geometry as sg
from scipy.optimize import fsolve
M = np.array
#==============================================================================
# 
#==============================================================================
def krzywizna(wek, pkt_B):
    srOk = M([wek[2][0],wek[2][1]])
    L1 = sg.Point(wek[0][0],wek[0][1])
    L6 = sympy.N(sg.Point(wek[1][0],wek[1][1]))
    L_cent = sg.Point(srOk[0],srOk[1])
    
    # Okrag -> Lopatka    
    promien = sympy.N(L1.distance(L_cent))
    
    
    def krzywiznaParametrycznie(t):
        x = srOk[0]+promien*np.cos(t)
        y = srOk[1]+promien*np.sin(t)
        return [x,y]
    
    hl = sg.Line(sg.Point(0.,0.),sg.Point(1.,0.))
    l_6 = sg.Line(L6,L_cent)
    l_1 = sg.Line(L1,L_cent)
    
    ang_6_hl = float(sympy.N(l_6.angle_between(hl)) + np.pi)
    ang_1_hl = float(sympy.N(l_1.angle_between(hl)) + np.pi)
    podzial = 8
    vec_I = np.linspace(ang_6_hl,
                         ang_1_hl,
                         num=podzial)[1:-1]

    L1 = [L1.x,L1.y]
    L6 = [L6.x,L6.y]
    
    r_temp = [L6,]
    for i in vec_I:
        krzyw = krzywiznaParametrycznie(i)
        r_temp.append(krzyw)
    
    r_temp.append(L1)
    r_temp.reverse()
    r_temp.append(srOk)

    return r_temp
    
def PunktLopatki(*args):  
    al_1 = np.deg2rad(args[0])
    al_2 = np.deg2rad(args[1])
    r = args[2]
    R = args[3]  
    pktOkr = args[4]  
    kat_pol = np.deg2rad(180.)
       
    def equations(p):
        theta = p
        f1 = (al_2 + al_1 + theta - kat_pol +
            2.*(np.arctan((r*np.sin(theta))/(R-r*np.cos(theta)))))
        return f1
        
    theta = fsolve(equations,(0))
    theta = theta[0]
    
    A = M([0.,-R])
    B = M([-r*np.sin(theta),-r*np.cos(theta)])
    
    
    A_B = M([((A[0]+B[0])/2.),  ((A[1]+B[1])/2.)])
    a_1 = (A[0]-B[0])/(B[1]-A[1])
    b_1 = A_B[1]-a_1*A_B[0]
    
    a_2 = 1./np.tan(al_1)
    b_2 = -R
    
    C_x = (b_2-b_1)/(a_1-a_2)
    C_y = a_1*C_x+b_1
    R_l = M([C_x,C_y])
    
    lop = krzywizna([A,B,R_l],pktOkr)
    for i in lop: i[0], i[1] = float(i[0]), float(i[1])
    
    return lop

#==============================================================================
#   
#==============================================================================
def punktyWylotu(alfa,b1,b2,r2,r3,r4,h1,h2,h3,R):
    A = M([r3, h1])
    C = M([r4, h2])
    D = M([r4, h3])
    R_pos = M([(r4 + R), C[1]])
    
    a = np.tan(np.deg2rad(-alfa))
    b = h1 - a*r3
    Z = lambda x: a*x + b
    
    p1 = sg.Point(A[0], A[1])
    p2 = sg.Point(r3-2.0, Z(r3-2.0))

    l = sg.Line(p1,p2)
    pc = sg.Point(R_pos[0],R_pos[1])    
    c = sg.Circle(pc,R)
    
    punkty = sg.intersection(c,l)
    
    if len(punkty)==0:
        text = "Powierzchnia wylotu nie moze zostać stworzona. Zmien wartosc \
            wymiaru wysokosci lopatki, kat alfa, badz promien zaokraglenia"
        raise ValueError(text)

    if len(punkty) == 2:
        w = min(punkty, key=lambda p: p.y)
        B = [sympy.N(w).x,sympy.N(w).y]
    else:
        w = punkty
        B = [sympy.N(punkty).x,
             sympy.N(punkty).y]
    
    B = M(B)
    Pl_yz = M([A,B,C,D,R_pos])

    krzywaLop_xy = PunktLopatki(b1,b2,r2,r3,Pl_yz[1])
    
    for i in Pl_yz:
        i[0], i[1] = float(i[0]), float(i[1])
        i[0] = -i[0]
    
    Pl_xyz = np.insert(Pl_yz, 0, 0.0, axis=1)

#==============================================================================
#     Obliczanie wspolrzednej Z dla lopatki    
#==============================================================================    
    def wspolrzednaZ(p):
        odl = np.sqrt(p[0]**2. + p[1]**2.)
        
        
        if abs(Pl_xyz[2][1]) <= odl <= abs(Pl_xyz[1][1]):
            z = -np.sqrt(R**2. - (-odl - Pl_xyz[4][1])**2.) + Pl_xyz[4][2]
            return z
        elif abs(Pl_xyz[1][1]) <= odl <= abs(Pl_xyz[0][1]):
            z = Z(odl)
            return z
        else:
            print 'Brak takiej wspolrzednej'
    
    kLop_xyz = []   
    for i in krzywaLop_xy[:-1]:
        z = wspolrzednaZ(i)
        kLop_xyz.append([i[0],i[1],z])
    
    kLop_xyz.append([krzywaLop_xy[-1][0],krzywaLop_xy[-1][1]])
    kLop_xyz = M(kLop_xyz)
    

    def krzywiznaParametrycznie(t):
        x = (-R_pos[0]+R*np.cos(t))
        y = R_pos[1]+R*np.sin(t)
        return M([x,y])
    
    R_C = sg.Line(pc,sg.Point(C[0],C[1]))
    R_B = sg.Line(pc,sg.Point(r2,kLop_xyz[-2][2]))
    ang = 2*np.pi - float(sympy.N(R_C.angle_between(R_B)))

    vec_I = np.linspace(ang,
                        2.*np.pi,
                        num=5)

    kolo_BC = []
    for i in vec_I:
        temp = [0.0]
        temp.extend(krzywiznaParametrycznie(i))
        kolo_BC.append(temp)
    kolo_BC.append(Pl_xyz[-2])
    kolo_BC = np.array(kolo_BC)[1:]
    return kLop_xyz, kolo_BC