import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os

import Artus.Utility.jsonTools as jsonTools

import Artus.HarryPlotter.harry as harry

import sys

class XBinning(dict):
    def __init__(self):
        self={}
        self.set_xbinningdict()

    def set_xbinning(self, variable, binning=None):
        if binning !=None:
            return binning
        else:
            try:
                return self[variable]
            except KeyError:
                print "variable not found in dict: \t", variable
                return None
    def set_nbins(self, nbins, variable):
        _bins_s = self[variable][0].split(",")
        _bins_s[0] = str(nbins)
        _bins = [_bins_s.join(",")]

    def set_xbinningdict(self):
        for ext in ["", "_reco", "_reco_a", "_reco_b"]:
            self["u_pol"+ext] = ["8,0,1"]
    		self["z_pol"+ext] = ["8,0,1"]
    		self["xl_pol"+ext] = ["20,0,5"]
    		self["xl_pol_tcm"+ext] = ["8,0,1"]
    		self["CosTheta_xl"+ext] = ["8,-1,1"]
    		self["CosTheta_yl"+ext] = ["8,-1,1"]
    		self["CosTheta_zl"+ext] = ["8,-1,1"]
    		self["CosTheta_ql"+ext] = ["8,-1,1"]
    		self["CosTheta_Tl"+ext] = ["8,-1,1"]
    		self["CosTheta_Nl"+ext] = ["8,-1,1"]

        self["TopPT"] = ["25,0,500"]
    	self["JetPT"] = ["25,0,500"]
    	self["JetE"] = ["25,0,500"]
    	self["BottomPT"] = ["15,0,300"]
