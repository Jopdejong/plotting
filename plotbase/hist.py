#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ROOT
from pprint import pprint
from functions import *
import os, re, sys, json


#make this baseclass, and a hist1d/hist2d?
class Hist(object):  #i dont know if this works

    def __init__(self):
        print "initialize Hist"
        self.normalize = False
        self.i = 0
        self.weights = "1"
        self.markerstyle = "HIST"
        self.linecolor = 1

    @staticmethod
    def find_ymax(h):
        ymax = h.GetMaximum() #set it to maximum
        return ymax



    def set_plotdefaults(self, plottingdict):
        if plottingdict.get("normalize", False):
             self.normalize = True
        else:
            self.normalize = False

        self.xmin = plottingdict["xmin"]
        self.xmax = plottingdict["xmax"]
        self.xbins = plottingdict["xbins"]
        self.ymin = plottingdict["ymin"]
        print plottingdict["ymax"]
        try:
            self.ymax = plottingdict["ymax"]
        except:
            self.ymax=None

        try:
            self.xlabel=plottingdict["xlabel"]
        except:
            self.xlabel = None

        try:
            self.ylabel=plottingdict["ylabel"]
        except:
            self.ylabel = ""

    def set_nick(self):
        if "nick" in self.histdict.keys():
            self.nick = str(self.histdict["nick"])
        else:
            self.nick = "nick"+str(self.i)


    def make_histogram(self, histdict):
        #returns a histogramm but not yet on the canvas
        #These depend on the histogramm which will be plotted TODO make special function for them
        self.histdict = histdict
        self.set_nick()
        if "name" in self.histdict.keys():
            self.name = str(self.histdict["name"])
        else:
            self.name = self.nick


        if "linecolor" in self.histdict.keys():
            self.linecolor = int(self.histdict["linecolor"]) #what if I want to use html colors?
        else: self.linecolor = self.i +1

        try:
            self.weights = self.histdict["weights"] #could have different weights for each plot
        except:
            pass
        try:
            self.xvar = self.histdict["xvar"] #could have different weights for each plot
        except:
            pass
        try:
            self.markerstyle = self.histdict["marker"]
        except:
            pass

        if self.xlabel == None:
            self.xlabel = self.xvar

        for file in histdict["input_files"]:
            self.tree = file +"/"+ self.histdict["folder"]
            t = ROOT.TChain("tree", "tree")
            t.Add(self.tree)

        h=ROOT.TH1F(self.nick,self.name,self.xbins,self.xmin,self.xmax)
        t.Project(self.nick,self.xvar,self.weights)

        if self.normalize:
            self.normalize_hist(h)

        h.SetLineColor(self.linecolor)
        #h.SetFillColor(self.linecolor)
        h.SetOption(self.markerstyle)


        self.maxy = self.find_ymax(h)
        if self.ymax==None:
            self.ymax = self.maxy
        h.SetAxisRange(self.ymin, self.ymax,"Y");
        h.SetStats(False)
        h.GetXaxis().SetTitle(self.xlabel)
        h.GetYaxis().SetTitle(self.ylabel)
        #h.GetXaxis().SetNdivisions(504)

        #make h self??
        self.i+=1
        return h

    def normalize_hist(self, h, normfactor=1.): #if one wants to scale it to an arbitrary number, usualy norm to 1
    	norm = h.Integral()
        if norm >0:
    	       h.Scale(normfactor/norm)

    @staticmethod
    def fit_double_gaussian(h):
        func = ROOT.TF1("func", double_gaussian(), -1,1,6)
        func.SetParameters( 0, h.GetRMS(), h.GetMaximum(), 0.1, 0.5, 1.)
        func.SetParLimits(0,-1,1)
        func.SetParLimits(3,-1,1)
        func.SetParLimits(1,0.04,2)
        func.SetParLimits(4,0.04,2)

        func.SetParLimits(2,0,10*h.GetMaximum())
        func.SetParLimits(5,0,10*h.GetMaximum())

        func.SetParNames("Mean_value1","Sigma1", "Constant1", "Mean_value2","Sigma2", "Constant2");
        h.Fit(func)

        func1 = ROOT.TF1("func1", gaussian(), -1,1,3)
        func1.SetParameters( func.GetParameter(0), func.GetParameter(1),func.GetParameter(2))

        func2 = ROOT.TF1("func2", gaussian(), -1,1,3)
        func2.SetParameters( func.GetParameter(3), func.GetParameter(4),func.GetParameter(5))

        return func, func1, func2

    @staticmethod
    def fit_gaussian(h, xmin, xmax):
        print "bla"
        func = ROOT.TF1("func", "gaus", xmin, xmax)
        func.SetParameters( h.GetMaximum(), 0, h.GetRMS())

        func.SetParNames( "Constant1", "Mean_value1","Sigma1");
        h.Fit(func)

        return func



    ##TODO add more functions which take a hist as input and do something with it
