import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os

import Artus.Utility.jsonTools as jsonTools

import Artus.HarryPlotter.harry as harry

import sys

class XLabels(dict):
    def __init__(self):
        self={}
        self.set_xlabeldict()

    def set_xlabel(self, variable):
        try:
            return self[variable]
        except KeyError:
            print "variable not found in dict: \t", variable
            return variable

    def set_xlabeldict(self):
    	self["u_pol"] = "u"
    	self["z_pol"] = "z"
    	self["xl_pol"] = "x_{l}^{lab}"
    	self["xl_pol_tcm"] = "x_{l}^{top}"

    	self["CosTheta_xl"] = "cos(#theta_{xl})"
    	self["CosTheta_yl"] = "cos(#theta_{yl})"
    	self["CosTheta_zl"] = "cos(#theta_{zl})"
    	self["CosTheta_ql"] = "cos(#theta_{ql})"
    	self["CosTheta_Tl"] = "cos(#theta_{Tl})"
    	self["CosTheta_Nl"] = "cos(#theta_{Nl})"

    	self["CosTheta_xl_reco"] = "reco cos(#theta_{xl})"
    	self["CosTheta_yl_reco"] = "reco cos(#theta_{yl})"
    	self["CosTheta_zl_reco"] = "reco cos(#theta_{zl})"
    	self["CosTheta_ql_reco"] = "reco cos(#theta_{ql})"
    	self["CosTheta_Tl_reco"] = "reco cos(#theta_{Tl})"
    	self["CosTheta_Nl_reco"] = "reco cos(#theta_{Nl})"
    	self["xl_pol_tcm_reco"]  = "reco x_{l}^{top}"
    	self["z_pol_reco"] = "reco z"

    	self["CosTheta_xl_reco_a"] = "reco_a cos(#theta_{xl})"
    	self["CosTheta_yl_reco_a"] = "reco_a cos(#theta_{yl})"
    	self["CosTheta_zl_reco_a"] = "reco_a cos(#theta_{zl})"
    	self["CosTheta_ql_reco_a"] = "reco_a cos(#theta_{ql})"
    	self["CosTheta_Tl_reco_a"] = "reco_a cos(#theta_{Tl})"
    	self["CosTheta_Nl_reco_a"] = "reco_a cos(#theta_{Nl})"
    	self["xl_pol_tcm_reco_a"]  = "reco_a x_{l}^{top}"
    	self["z_pol_reco_a"] = "reco_a z"

    	self["CosTheta_xl_reco_b"] = "reco_b cos(#theta_{xl})"
    	self["CosTheta_yl_reco_b"] = "reco_b cos(#theta_{yl})"
    	self["CosTheta_zl_reco_b"] = "reco_b cos(#theta_{zl})"
    	self["CosTheta_ql_reco_b"] = "reco_b cos(#theta_{ql})"
    	self["CosTheta_Tl_reco_b"] = "reco_b cos(#theta_{Tl})"
    	self["CosTheta_Nl_reco_b"] = "reco_b cos(#theta_{Nl})"
    	self["xl_pol_tcm_reco_b"]  = "reco_b x_{l}^{top}"
    	self["z_pol_reco_b"] = "reco_b z"

    	self["TopPT"] = "p_{T}^{top}"
    	self["BottomPT"] = "p_{T}^{b}"
    	self["JetPT"] = "p_{T}^{jet}"
