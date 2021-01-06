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


rootfiles = ["/dcache/atlas/top/jdegens/output/test2_truth//410658_PhPy8EG_tch_BW50_l_t/mc16_13TeV.410658.PhPy8EG_tch_BW50_l_t.mu_topwidth50.root", "/dcache/atlas/top/jdegens/output/test2_truth//410658_PhPy8EG_tch_BW50_l_t/mc16_13TeV.410658.PhPy8EG_tch_BW50_l_t.mu4.root"]

rootfiles = ["/dcache/atlas/top/jdegens/output/test3_MG5/500298_MGPy8EG_LO_Dim6TopUFO_Reweighted/mu.root"]

folder=args.folders

plottingdict["output_dir"] = os.getcwd()+"/plots/2020-09-24/kinematics/"

if len(args.x_expressions) == 0:
	variables = ["xl_pol", "z_pol", "costheta_xl","costheta_ql","xl_pol_tcm", "u_pol"]
else:
	variables = args.x_expressions

_plotdict ={}
_plotdict["weights"]= args.weights
_plotdict["colors"]= args.colors
_plotdict["names"] =args.names
_plotdict["var"] =variables


_plotdict = p.prepare_list_args(_plotdict, ["weights", "colors", "names", "var"])
pprint(_plotdict)

rfile_n = ["norm", "topwidth50"]

for k,rfile in enumerate(rootfiles[0:1]):
	for l, var in enumerate(_plotdict["var"]):
		plotdict["xvar"] = var
		plotdict["weights"]=_plotdict["weights"][l]

		plotdict["input_files"] = rootfiles
		plotdict["folder"] = "nominal"
		#plotdict["nick"] = "nick"+str(t)
		plotdict["name"] = _plotdict["names"][l]
		plotdict["linecolor"] = _plotdict["colors"][l]
		#plotdict["name"] = "klfit - tag"
		#plotdict["stack"] = "stack_%d" % t
		filename = var

		plotdictlist.append(copy.deepcopy(plotdict))

plotlist=[]


#for var in variables:
d = plotdefaults.Plotdefaults(var) ## TODO:  initialize it ones and do d.set_var in loop?
#d.set_var(var)
plottingdict.update(d) #update the dict which is input for the plot with d, which has things like xmin,xmax etc...

plottingdict["filename"]=args.filename if args.filename !="None" else filename
plottingdict["filetype"]="png"
plottingdict["xbins"]= 20
plottingdict["xmin"] = 0
plottingdict["xmax"] = 200
plottingdict["ymax"] = None
plottingdict["xlabel"] = "pt"#"cos(#theta_{x})"
plottingdict["normalize"] = True
#for pdl in plotdictlist:
#	pdl["var"] = d["var"]
finaldict = {"histdictslist" : plotdictlist, "plottingdict" : plottingdict}

plotlist.append(copy.deepcopy(finaldict))


print len(plotlist)


p.show_legend = True
p.create_multiplots(plotlist)

#rootname = "test"

#g=ROOT.TFile(rootname,"update")
#RootTools.write_object(g,h,path)
#g.Close()
