# -*- coding: utf-8 -*-
"""
Created on Sun Feb 07 14:37:42 2016

@author: Slawek
"""
from itertools import count
import numpy as np
import subprocess
import os, sys

#==============================================================================
#   klasa Gmsh odpowiedzialna jest za przesylanie tworzenie geometrii, siatki
#   oraz wysylanie jej do programu Calculix
#==============================================================================
class Gmsh(object):
    def __init__(self,part,wd,gmwd):
        self.part = part
        self.nazwa = part['nazwa']
        self.wd = wd
        self.gmwd = gmwd
        
        
        if sys.platform == 'linux' or sys.platform == 'linux2':
            self.SHELL = True
        elif sys.platform == 'win32':
            self.SHELL = False

    
    def napiszGeo(self):
        with open(self.nazwa + '.geo','w') as f:
            f.write(self.part['txt'])
    
    def przeslijGeometrie(self,bgm=False):

        if bgm == True:
            cmd = '{0} {1} -0'
        else:
            cmd = '{0} {1}'

        lines = []
        p = subprocess.Popen(cmd.format(self.gmwd,self.nazwa+'.geo'),
                             bufsize=1, stdin=open(os.devnull),
                             shell=self.SHELL,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        
        for line in iter(p.stdout.readline, ''):
            print line,          
            lines.append(line)   
        p.stdout.close()
        p.wait()
    
    def gmshCmd(self,com):   
        cmd = self.gmwd + ' ' + com
        lines = []
        p = subprocess.Popen(cmd, bufsize=1, stdin=open(os.devnull),
                             shell=self.SHELL,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        for line in iter(p.stdout.readline, ''):
            print line,          
            lines.append(line)   
        p.stdout.close()
        p.wait()
    
    def cmd(self,com):
        lines = []
        p = subprocess.Popen(com, bufsize=1, stdin=open(os.devnull),
                             shell=self.SHELL,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        for line in iter(p.stdout.readline, ''):
            print line,          # print to stdout immediately
            lines.append(line)   # capture for later
        p.stdout.close()
        p.wait()
    
    def cgx(self,com):   
        p = subprocess.Popen(com, stdin=open(os.devnull),
                             shell=self.SHELL,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
#==============================================================================
#   Klasa Part ma na celu przechowywanie wiadomosci o geometrii w postaci 
#   slow kluczowych uzytych w pliku wsadowym programu GMSH. 
#==============================================================================
class Part(dict):

#==============================================================================
#     KONSTRUKTOR    
#==============================================================================
    def __init__(self,nazwa):
        
        self.p_ind = count(0)
        self.l_ind = count(1)
        self.ll_ind = count(1)
        self.r_ind = count(1)

        self['nazwa'] = nazwa        
        self['czesci'] = []
        self['txt'] = ''
    
#==============================================================================
#     CZESCI GEOMETRII
#==============================================================================
    def pkt(self,x,y,z):
        self.p_id = self.p_ind.next()
        p = Point(x,y,z,self.p_id)
        self['czesci'].append(p)
            
    def kolo(self,x,y,z):
        self.l_id = self.l_ind.next()
        k = Circle(x,y,z,self.l_id)
        self['czesci'].append(k)
    
    def wieleKol(self,srodek,kola):
        n = range(0,len(kola))
        for i in n:
            self.l_id = self.l_ind.next()
            t = Circle(kola[i].id,
                       srodek,
                       kola[(i + 1) % len(kola)].id, self.l_id)
            self['czesci'].append(t)
    
    def line(self,*args):
        self.l_id = self.l_ind.next()
        k = Line(self.l_id,args)
        self['czesci'].append(k)
    
    def spline(self,*args):
        self.l_id = self.l_ind.next()
        k = Spline(self.l_id,args)
        self['czesci'].append(k)
        
    def lloop(self,*args):
        self.ll_id = self.ll_ind.next()
        k = LLoop(self.ll_id,args)
        self['czesci'].append(k)
    
    def psurf(self,*args):
        self.r_id = self.r_ind.next()
        k = PSurface(self.r_id,args)
        self['czesci'].append(k)
    
    def rsurf(self,*args):
        self.r_id = self.r_ind.next()
        k = RSurface(self.r_id,args)
        self['czesci'].append(k)

    def physical(self,nazwa,*args):
        self.l_id = self.l_ind.next()
        k = Physical(self.l_id,nazwa,args)
        self['czesci'].append(k)
    
#==============================================================================
#     METODY
#==============================================================================
    def t(self,text):
        self['czesci'].append(text+'\n')
    
    def napiszTekst(self):
        for i in self['czesci']:
            self['txt'] += str(i)
    
    def cnt_st(self):
        # Ustaw poczatek naliczania
        cnt_st = len(self['czesci'])
        return cnt_st
    
    def cnt_fnd(self,cnt_st):
        # Ustaw koniec naliczania
        cnt_fnd = len(self['czesci'])
        # Stworz liste punktow
        vec = self['czesci'][cnt_st:cnt_fnd]
        return vec
    
    def rotacja(self,punkt,il_l,z=0.0,theta=0.0):
        ob = (2*np.pi)/float(il_l)
        
        def rotY(theta,rotPoint):
            x = rotPoint[0]
            z = rotPoint[1]
            rotPoint[0] = x*np.cos(theta) - z*np.sin(theta)
            rotPoint[1] = x*np.sin(theta) + z*np.cos(theta)
            return rotPoint

        for i in range(il_l):
            temp = [punkt[0], punkt[1]]
            vec = rotY(theta,temp)
            self.pkt(vec[0],vec[1],z)
            theta += ob
    def structMesh(self,lloop, surf_id,num=1.0,ref=False):
        if ref==False:        
            lloop = [abs(i) for i in lloop]
            l_s = "{0}, {1}, {2}, {3}".format(*lloop)
            podzial = str(int(10.0 * (1./float(num))))
            self.t("Transfinite Line {%s} = %s Using Progression 1;" % (l_s,podzial))
            self.t("Transfinite Surface {%d};" % surf_id)
            self.t("Recombine Surface {%d};" % surf_id)
        else:
            lloop = [abs(i) for i in lloop]
            l_s = "{0}, {1}, {2}, {3}".format(*lloop)
            podzial = str(int(10.0 * (1./float(ref))))
            self.t("Transfinite Line {%s} = %s Using Progression 1;" % (l_s,podzial))
            self.t("Transfinite Surface {%d};" % surf_id)
            self.t("Recombine Surface {%d};" % surf_id)
            
    
    def koniecCzesci(self):
        self.p_ind = count(0)
        self.l_ind = count(1)
        self.r_ind = count(1)
        self.ll_ind = count(1)
           

class Point(Part):

    def __init__(self,x,y,z,ind):
        self.x = x
        self.y = y
        self.z = z
        self.id = ind
    
    def __str__(self):
        t = (self.id, self.x, self.y, self.z)
        t = "Point(%d) = {%.5f,%.5f,%.5f};\n" % t
        return t
        
    def __repr__(self):
        txt = 'Point-'+str(self.id)
        return txt

class Circle(Part):
    
    def __init__(self,x,y,z,ind):
        self.x = x
        self.y = y
        self.z = z

        self.id = ind
    
    def __str__(self):
        t = (self.id, self.x, self.y, self.z)
        t = "Circle(%d) = {%d,%d,%d};\n" % t
        return t
        
    def __repr__(self):
        txt = 'Circle-'+str(self.id)
        return txt

class Line(Part):

    def __init__(self,ind,*args):
        if type(args[0][0])==list:
            
            temp = args[0][0]
            self.args = str(temp)[1:-1]
        
        elif len(args[0]) == 1:
            self.args = str(args[0][0])

        else:
            self.args = str(args[0])[1:-1]
        
        self.id = ind
    
    def __str__(self):
        t = "Line(%d)" % self.id
        t =  t + '= {' + self.args + '};\n'
        return t
    
    def __repr__(self):
        txt = 'Line-'+str(self.id)
        return txt
        
class Spline(Part):

    def __init__(self,ind,*args):
        if type(args[0][0])==list:
            
            temp = args[0][0]
            self.args = str(temp)[1:-1]
        
        elif len(args[0]) == 1:
            self.args = str(args[0][0])

        else:
            self.args = str(args[0])[1:-1]
        
        self.id = ind
    
    def __str__(self):
        t = "Spline(%d)" % self.id
        t =  t + '= {' + self.args + '};\n'
        return t
    
    def __repr__(self):
        txt = 'Spline-'+str(self.id)
        return txt

class LLoop(Part):
    
    def __init__(self,ind,*args):
        if type(args[0][0])==list:
            
            temp = args[0][0]
            self.args = str(temp)[1:-1]
        
        elif len(args[0]) == 1:
            self.args = str(args[0][0])

        else:
            self.args = str(args[0])[1:-1]
        
        self.id = ind#self._ids.next()

    def __str__(self):
        t = "Line Loop(%d)" % self.id
        t =  t + '= {' + self.args + '};\n'
        return t
    
    def __repr__(self):
        txt = 'LineLoop-'+str(self.id)
        return txt

class PSurface(Part):
    
    def __init__(self,ind,*args):
        if type(args[0][0])==list:
            
            temp = args[0][0]

            self.args = str(temp)[1:-1]
        
        elif len(args[0]) == 1:
            
            self.args = str(args[0][0])

        else:
            self.args = str(args[0])[1:-1]
        
        self.id = ind
    
    
    def __str__(self):
        t = "Plane Surface(%d)" % self.id
        t =  t + '= {' + self.args + '};\n'
        return t
    def __repr__(self):
        txt = 'PlaneSurface-'+str(self.id)
        return txt

class RSurface(Part):

    def __init__(self,ind,*args):
        if type(args[0][0])==list:
            
            temp = args[0][0]

            self.args = str(temp)[1:-1]
        
        elif len(args[0]) == 1:
            
            self.args = str(args[0][0])

        else:
            self.args = str(args[0])[1:-1]
        
        self.id = ind
    
    
    def __str__(self):
        t = "Ruled Surface(%d)" % self.id
        t =  t + '= {' + self.args + '};\n'
        return t
    def __repr__(self):
        txt = 'RuledSurface-'+str(self.id)
        return txt

class Physical(Part):

    def __init__(self,ind,nazwa,*args):
        if type(args[0][0])==list:
            
            temp = args[0][0]
            self.args = str(temp)[1:-1]
        
        elif len(args[0]) == 1:
            self.args = str(args[0][0])

        else:
            self.args = str(args[0])[1:-1]
        
        self.nazwa = nazwa
        self.id = ind
    
    def __str__(self):
        t = "Physical %s(%d)" % (self.nazwa,self.id)
        t =  t + '= {' + self.args + '};\n'
        return t
    
    def __repr__(self):
        txt = 'Physical %s-%d' % (self.nazwa,self.id)
        return txt