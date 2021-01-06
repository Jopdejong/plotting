import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os

import Artus.Utility.jsonTools as jsonTools

import Artus.HarryPlotter.harry as harry

import labels as lb
import binnings as bn
import asymmetry as as

import sys



class PlotConfigs:
    def __init__(self):
        #plotconfig initiation
        self.xbinning = bn.XBinning()
        self.xlabel = lb.XLabel()
        self.asymmetry =as.Asymmetry()
        ## TODO:
        #nickconfig initiation

    # function for 1 nick specific like legend-label, color and linestyle
    # regarding the color think about colourblind eric
    def set_nickconfig(self, nickname, variable):
        pass

    # function to set general things for the plot like binning, xlabel, ylabel.
    # you can also do self.xlabel.set_xlabel(variable) to only get the xlabel
    # use: xbinning, xlabel = self.set_plotconfig(var)
    def set_plotconfig(self, variable):
        _xbinning = self.xbinning.set_xbinning(variable)
        _xlabel = self.xlabel.set_xlabel(variable)
        return _xbinning, _xlabel
