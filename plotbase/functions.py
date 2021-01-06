#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ROOT
from pprint import pprint






def double_gaussian():
    function = "[2]*TMath::Gaus(x,[0],[1]) + [5]*TMath::Gaus(x,[3],[4])"
    return function

def gaussian():
    return "[2]*TMath::Gaus(x,[0],[1])"

#class DoubleGaussian:
#   def __init__( self, s ):
#      self.s = s
#
#   def __call__( self, x, p ):
#      self.s.SetParameters(p[0],p[1],p[2], p[3], p[4], p[5])
#      return self.s.Integral(x[0],10)
#
#ga = Ga( TF1( "s", gax, -10., 10., 3 ) )
