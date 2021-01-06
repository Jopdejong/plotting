#!/usr/bin/env python
# -*- coding: utf-8 -*-


import ROOT

import plotter

#from Artus.HarryPlotter.utility.roottools import RootTools
name="hist1"

def f(i,j,tree, var, cuts="1",hname="h1"):
	t = ROOT.TChain("tree", "tree")
	t.Add(tree)
	h=ROOT.TH1F(hname,name,bins,xmin,xmax)
	t.Project(hname,var,cuts)
	h.SetLineColor(i)
	#h.SetMarkerStyle(j)
	
	norm = 1
	norm = h.GetEntries();
	h.Scale(1/norm);
	h.SetAxisRange(ymin, ymax,"Y")
	return h




rootfile = "/data/atlas/users/jdegens/analysis/TOP/Analysis/sm.root"
rootfile2 = "/data/atlas/users/jdegens/analysis/TOP/Analysis/ctw_EFT2_topdecayed.root"

Dir = "Event;1"
tree = ""

treepath = (rootfile+"/"+Dir+"/" if Dir!="default" else "")+tree
treepath2 = (rootfile2+"/"+Dir+"/" if Dir!="default" else "")+tree

trees = [treepath,treepath2]
#t.Add(treepath)

c=ROOT.TCanvas("c","test",600,600)

ratio=True


bins =10
xmin = 0
xmax = 1


var = 8
cuts= "(Event.TopBeta>0.9)"

appendix= "beta09"

for var in xrange(3,9):

	if var==3:
		filename="costheta_xl"
		vard="Event.CosTheta_xl"
		xmin=-1
		xmax=1
		ymin=0.1
		ymax=0.2
		bins =6
	elif var==4:
		filename="costheta_ql"
		vard="Event.CosTheta_ql"
		xmin=-1
		xmax=1
		ymin=0
		ymax=0.3
		bins =6
	elif var==5:
		filename="xl_pol"
		vard="Event.xl_pol"
		xmin=0
		xmax=5
		ymin=0
		ymax=0.4
		bins =6
	elif var==6:
		filename="xl_pol_tcm"
		vard="Event.xl_pol_tcm"
		xmin=0
		xmax=1
		ymin=0
		ymax=0.4
		bins =6
	elif var==7:
		filename="u_pol"
		vard="Event.u_pol"
		xmin=0
		xmax=1
		ymin=0
		ymax=0.4
		bins =6
	elif var==8:
		filename="z_pol"
		vard="Event.z_pol"
		xmin=0
		xmax=1
		ymin=0
		ymax=0.4
		bins =6

	filename+=appendix







	c=ROOT.TCanvas("c"+str(var),"test",600,600)



	w = f(1,1,treepath, vard, cuts,hname="h1")

	x = f(2,1,treepath2, vard, cuts,hname="h2")
	"""
	z=w.Clone('h3')
	z.Divide(x)

	if ratio:
		#pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
		#pad1.SetBottomMargin(0.)  # joins upper and lower plot
		#pad1.SetGridx()
		#pad1.Draw()
		w.Draw()
		x.Draw("same")
		# Lower ratio plot is pad2
		#c.cd()  # returns to main canvas before defining pad2
		#pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.25)
		#pad2.SetTopMargin(0.2)  # joins upper and lower plot
		#pad2.SetBottomMargin(0.)
		#pad2.SetGridx()
		#pad2.Draw()
		#pad2.cd()
		#z.SetMinimum(0.8)
	    	#z.SetMaximum(1.35)
		#z.Draw()
		z=ROOT.TRatioPlot(x, w)
		z.Draw()
		z.GetLowerRefGraph().SetMinimum(0.5)
		z.GetLowerRefGraph().SetMaximum(1.5)
		c.Update()
	else:"""
	w.Draw()
	x.Draw("same")
	c.Update()



	c.SaveAs("/user/jdegens/analysis/plots/2019-09-12/EFT2/"+filename+".png")

	c.Close()





#rootname = "test"

#g=ROOT.TFile(rootname,"update")
#RootTools.write_object(g,h,path)
#g.Close()
