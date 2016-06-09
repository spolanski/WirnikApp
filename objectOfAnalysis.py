# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 21:11:51 2016

@author: slawek
"""

class Geometry(object):
    def __init__(self):
        pass
    
    def wymiar(self,cecha,wartosc):
        self.cecha = wartosc

class FeaModel(object):
    
    def __init__(self):
        self.Geo = Geometry()
        self.Input = {}