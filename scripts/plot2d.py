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

parser = argparse.ArgumentParser(parents=[plotclass.Plotter.argparser()]) #can someone explain why the parser doesnt have the right help??
#change parser with additional arguments here
args = parser.parse_args()

#print args
plotdict = {}
plottingdict= {}
plotdictlist = []

if os.path.isfile(args.json):
	finaldict = p.read_json(args.json)

	plottingdict = finaldict["plottingdict"]
	plotdictlist = finaldict["histdictslist"]

#rootfile = "/dcache/atlas/top/jdegens/output/test2_mark/v1_412076/skimm.EFT_v30.v1.mu_KLFIT1_lowerpztag.root"
rootfile2 = "/dcache/atlas/top/jdegens/output/test2_truth//410658_PhPy8EG_tch_BW50_l_t/mc16_13TeV.410658.PhPy8EG_tch_BW50_l_t.mu2.root"

#rootfiles = args.input_files
rootfiles = [rootfile2]#, rootfile2]
folder=args.folders

plottingdict["output_dir"] = os.getcwd()+"/plots/2020-08-19/test_2d/"

xvar = args.x_expressions[0]
yvar = args.y_expressions[0]

print yvar




plotdict ={}
plotdict["weights"]= args.weights[0]
#plotdict["colors"]= args.colors
plotdict["name"] =args.names

plotdict["xvar"] = args.x_expressions[0]
plotdict["yvar"] = args.y_expressions[0]

print "yvar", plotdict["yvar"]





plotdict["input_files"] = rootfiles
plotdict["folder"] = "ResultsDataTree"
plotdict["nick"] = "nick"+str(1)
#plotdict["name"] = "klfit - tag"
#plotdict["stack"] = "stack_{}".format(t)
filename = plotdict["xvar"]

plotdictlist.append(copy.deepcopy(plotdict))

plotlist=[]


#for var in variables:
#d.set_var(var)

plottingdict["filename"]=args.filename if args.filename !="None" else filename
plottingdict["filetype"]="png"
plottingdict["xbins"]= 50
plottingdict["xmin"] = 0
plottingdict["xmax"] = 2500

plottingdict["ybins"]= 50
plottingdict["ymin"] = 0.
plottingdict["ymax"] = 2500.

plottingdict["canvas_size_x"] = 800

plottingdict["dim"] = 2


#lottingdict["ymin"] = 0.0

plottingdict["xlabel"] = "truth jet_E"
plottingdict["ylabel"] = "reco jet_E"


plottingdict["markerstyle"] = "COLZl"
#for pdl in plotdictlist:
#	pdl["xvar"] = d["xvar"]
finaldict = {"histdictslist" : plotdictlist, "plottingdict" : plottingdict}

plotlist.append(copy.deepcopy(finaldict))


print len(plotlist)

p.create_multiplots(plotlist)

#rootname = "test"

#g=ROOT.TFile(rootname,"update")
#RootTools.write_object(g,h,path)
#g.Close()
