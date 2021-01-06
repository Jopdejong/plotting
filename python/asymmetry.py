import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os

import Artus.Utility.jsonTools as jsonTools

import Artus.HarryPlotter.harry as harry

import sys

class Asymmetry(dict):
    def __init__(self):
        self={}
        self.set_asymmetrydict()

    def set_assymetrypoint(self, variable):
        try:
            return self[variable]
        except KeyError:
            print "variable not found in dict: \t", variable
            return None

    def set_asymmetrydict(self):
        for ext in ["", "_reco", "_reco_a", "_reco_b"]:
    		self["u_pol"+ext] = 0.5
    		self["z_pol"+ext] = 0.5
    		self["xl_pol"+ext] = 0.5
    		self["xl_pol_tcm"+ext] = 0.5
    		self["CosTheta_xl"+ext] = 0
    		self["CosTheta_yl"+ext] = 0
    		self["CosTheta_zl"+ext] = 0
    		self["CosTheta_ql"+ext] = -0.25
    		self["CosTheta_Tl"+ext] = 0
    		self["CosTheta_Nl"+ext] = 0

        #These are not very good vars for asymetry, however it is not impossible, so here are some reasonable points
        asymmetrypoints["TopPT"] = 100
    	asymmetrypoints["JetPT"] = 75
    	asymmetrypoints["JetE"] = 150
