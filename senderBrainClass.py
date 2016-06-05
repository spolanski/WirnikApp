# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 22:21:10 2016

@author: slawek
"""
import subprocess
import os, sys

#==============================================================================
#   klasa Gmsh odpowiedzialna jest za przesylanie tworzenie geometrii, siatki
#   oraz wysylanie jej do programu Calculix
#==============================================================================
class SenderBrain(object):
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