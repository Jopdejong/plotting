#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
#import ROOT

import os

from plotbase import plotclass
from plotbase import plotdefaults

from pprint import pprint

import argparse
#from Artus.HarryPlotter.utility.roottools import RootTools

p=plotclass.Plotter()

parser = argparse.ArgumentParser(parents=[plotclass.Plotter.argparser()])
#change parser with additional arguments here
args = parser.parse_args()

#print args

plotdict = {}
plottingdict= {}
plotdictlist = []
plotlist=[]

rootfiles = ["/dcache/atlas/top/jdegens/output/test3_truth/410658_PhPy8EG_tch_BW50_l_t/el.root"]

plottingdict["output_dir"] = os.getcwd()+"/plots/2020-09-23/test_el_selection_test3/"

plottingdict["filetype"]="pdf"
plottingdict["xbins"]= 50

plottingdict["ymin"] = 0

plottingdict["ymax"] = None

plottingdict["normalize"] = True


weights0 = "(nGoodLightJets==1)*(nGoodBJets==1)*(combinedWeight) " # *(eventSelectionBitSet==15)*(abs(reco_spectquark_eta_tag)>2.5) *(eventSelectionBitSet==1) *(loglikelihood_kfit>-35)

particles = ["top", "spectquark", "wbosonfromtop", "leptonfromtop", "bquarkfromtop", "nufromtop"]
variables = ["pt", "pz", "E", "m", "eta", "phi"]
suffixes = ["tag", "klfit"]

plotdict["input_files"] = rootfiles
plotdict["folder"] = "nominal"

names = ["tag", "klfit"]
plottingdict["filename"]= "comparisons_nosel"


for particle in particles:
    weights=weights0+"*("+"reco_"+particle+"_pt_tag>0)" +"*("+"truth_"+particle+"_pt_tag>0)"
    plotdict["weights"]=weights


    for variable in variables:
        plotdictlist=[]
        if variable == "eta" and particle in ["spectquark", "bquarkfromtop"]:
            plottingdict["xmin"] = -0.3
            plottingdict["xmax"] = 0.3
        elif particle == "leptonfromtop":
            plottingdict["xmin"] = -0.3
            plottingdict["xmax"] = 0.3
        else:
            plottingdict["xmin"] = -1
            plottingdict["xmax"] = 1

        xvar_tag="reco_"+particle+"_"+ variable+"_tag"
        xvar_kin="reco_"+particle+"_"+ variable+"_klfit"
        #if particle == "bquarkfromtop":
        #    xvar_part="part_"+particle+"_"+ variable+"_tag"
        #else:
        xvar_part="truth_"+particle+"_"+ variable+"_tag"
        diffvars=[ "("+ xvar_part+"-"+xvar_tag+")/"+ xvar_part, "("+ xvar_part+"-"+xvar_kin+")/"+ xvar_part]
        for l, var in enumerate(diffvars):
            plotdict["name"] = names[l]
            plotdict["linecolor"] = l+1
            plotdict["xvar"]=var
            pprint( plotdict)
            plotdictlist.append(copy.deepcopy(plotdict))


        	#plotdict["name"] = "klfit - tag"
        	#plotdict["stack"] = "stack_{}".format(t)
            #plotdictlist.append(copy.deepcopy(plotdict))

        plottingdict["xvar"] = var
        plottingdict["xlabel"] = "#Delta"+ variable+"_{"+particle+"}"
        finaldict = {"histdictslist" : plotdictlist, "plottingdict" : plottingdict}
        pprint( finaldict)
        p.create_plot(finaldict)
        p.save_plot_1pdf()
        #plotlist.append(copy.deepcopy(finaldict))

#p.create_multiplots(plotlist)

pol_var = ["cos_lx", "cos_ly", "angle_phi", "angle_phi_star"]

for var in pol_var:
    plotdictlist=[]

    weights=weights0 +"*(truth_spectquark_pt_tag>0)*(reco_spectquark_pt_tag>0)*(abs(reco_spectquark_eta_tag)>2.5)"
    plotdict["weights"]=weights
    truthvar = "truth_"+var
    recovar = "reco_tag_"+var
    klfitvar = "reco_tag_"+ var+ "_klfit"

    for l, x in enumerate(["("+recovar+ "-"+ truthvar+")/("+truthvar+ ")", "("+klfitvar+ "-"+ truthvar+")/("+truthvar+ ")"]):
        plotdict["xvar"]=x
        plotdict["name"] = names[l]
        plotdict["linecolor"] = l+1
        plotdictlist.append(copy.deepcopy(plotdict))



    #plottingdict["filename"] = var
    plottingdict["xlabel"] = "#Delta"+ var
    plottingdict["xmin"] = -1
    plottingdict["xmax"] = 1
    plottingdict["xvar"] = plotdict["xvar"] #change this I dont need it

    finaldict = {"histdictslist" : plotdictlist, "plottingdict" : plottingdict}
    pprint( finaldict)
    p.create_plot(finaldict)
    p.save_plot_1pdf()
p.c.Print(plottingdict["output_dir"]+plottingdict["filename"]+".pdf]")
