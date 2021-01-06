#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import ROOT

import os, json

from plotbase import plotclass
from plotbase import plotdefaults

from pprint import pprint

import argparse

from array import array

from math import log, exp, sqrt, factorial, pi

import random
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



plotdict["input_files"] = ["/dcache/atlas/top/jdegens/output/test3_truth//410658_PhPy8EG_tch_BW50_l_t/mu.root"]
plotdict["folder"] =  "ResultsDataTree"

plottingdict["output_dir"] = os.getcwd()+"/plots/2020-09-24/transferfunction/"

plottingdict["filetype"]="png"
plottingdict["xbins"]= 50

plottingdict["ymin"] = 0
plottingdict["ymax"] = None

plottingdict["xmin"] = -1
plottingdict["xmax"] = 1

plottingdict["xlabel"] = "(E_{R}-E_{T})/E_{T}"

plottingdict["normalize"] = False


Energies = [30, 250]
for x in xrange(300,1000,50):
    Energies.append(x)

for x in xrange(1000,2100,100):
    Energies.append(x)
print "Energy", Energies




weights0 = "(nGoodLightJets==1)*(nGoodBJets==1)*(MET>30)*(MTW>60)*(DeltaR_truth_reco_spectatorjet<0.3)*(truth_spectquark_E_tag>0)*(reco_spectquark_E_tag>0)*(reco_spectquark_pt_tag>30) *(abs(reco_spectquark_eta_tag)>2.5) *(eventSelectionBitSet==15)" #*(abs(reco_spectquark_eta_tag)>2.5)

plottingdict["xvar"] = "(reco_spectquark_E_tag-truth_spectquark_E_tag)/truth_spectquark_E_tag"
plotdict["xvar"] = "(reco_spectquark_E_tag-truth_spectquark_E_tag)/truth_spectquark_E_tag" ## FIXME:  this is stupid fix this
plotdict["linecolor"] = 1

plotdict["fit"] = {}
plotdict["fit"]["type"] = "double_gaussian"

plotted_functions ={}
plotted_histograms = {}
dicts = {}

m1 = []
s1 = []
N1 = []
m2 = []
s2 = []
N2 = []
p0 = []

err_m1 = []
err_s1 = []
err_N1 = []
err_m2 = []
err_s2 = []
err_N2 = []
err_p0 = []

x = []
err_x =[]





for i in range(len(Energies)):
    emin = Energies[i]
    if i >= len(Energies)-1:
        weights = weights0 + "*(truth_spectquark_E_tag>{})".format(emin)
        plottingdict["filename"] = "transferfunction_Emin{:d}".format(emin)
        plotdict["name"] = "E: >{:d} GeV".format(emin,emax)

    else:
        emax = Energies[i+1]
        weights = weights0 + "*(truth_spectquark_E_tag>{}) *(truth_spectquark_E_tag<{})".format(emin,emax)
        plottingdict["filename"] = "transferfunction_Emin{:d}_Emax{:d}".format(emin,emax)

        plotdict["name"] = "E: {:d} - {:d} GeV".format(emin,emax)



    plotdict["weights"] = weights
    finaldict = {"histdictslist" : [plotdict], "plottingdict" : plottingdict}
    p.create_saved_plot(finaldict)


    ### this should be some sort of function
    k ="Emin{:d}_Emax{:d}".format(emin,emax)

    if i < len(Energies)-1:
        x.append((emin+emax)/2.)
        err_x.append((emin-emax)/12**0.5)

    else:
        x.append(emin+100.)
        err_x.append(50.)

    dicts[(emin+emax)/2.] = copy.deepcopy(finaldict)

    plotted_functions[(emin+emax)/2.] = p.plotted_functions
    plotted_histograms[(emin+emax)/2.] = p.plotted_histograms

    #if gauss 2 smaller than gauss 1 swap them, 2 always larger
    if p.plotted_functions["fit"].GetParameter(2) < p.plotted_functions["fit"].GetParameter(5):
        m1.append(p.plotted_functions["fit"].GetParameter(0))
        err_m1.append((p.plotted_functions["fit"].GetParError(0)**2+0.04**2)**(0.5))

        s1.append(p.plotted_functions["fit"].GetParameter(1))
        err_s1.append((p.plotted_functions["fit"].GetParError(1)**2+0.04**2)**(0.5))



        N1.append(p.plotted_functions["fit"].GetParameter(2))
        err_N1.append(p.plotted_functions["fit"].GetParError(2))

        m2.append(p.plotted_functions["fit"].GetParameter(3))
        err_m2.append((p.plotted_functions["fit"].GetParError(3)**2+0.04**2)**(0.5))

        s2.append(p.plotted_functions["fit"].GetParameter(4))
        err_s2.append((p.plotted_functions["fit"].GetParError(4)**2+0.04**2)**(0.5))

        N2.append(p.plotted_functions["fit"].GetParameter(5))
        err_N2.append(p.plotted_functions["fit"].GetParError(5))

        p0.append(p.plotted_functions["fit"].GetParameter(2)/p.plotted_functions["fit"].GetParameter(5))
        err_part1 = (p.plotted_functions["fit"].GetParError(2)/p.plotted_functions["fit"].GetParameter(5))**2
        err_part2 = ((p.plotted_functions["fit"].GetParameter(2)/(p.plotted_functions["fit"].GetParameter(5)**2)) *p.plotted_functions["fit"].GetParError(5))**2

        err_p0.append((err_part1+err_part2+0.04**2)**0.5)


    else:
        m1.append(p.plotted_functions["fit"].GetParameter(3))
        err_m1.append((p.plotted_functions["fit"].GetParError(3)**2+0.04**2)**(0.5))

        s1.append(p.plotted_functions["fit"].GetParameter(4))
        err_s1.append((p.plotted_functions["fit"].GetParError(4)**2+0.04**2)**(0.5))

        N1.append(p.plotted_functions["fit"].GetParameter(5))
        err_N1.append(p.plotted_functions["fit"].GetParError(5))

        m2.append(p.plotted_functions["fit"].GetParameter(0))
        err_m2.append((p.plotted_functions["fit"].GetParError(0)**2+0.04**2)**(0.5))

        s2.append(p.plotted_functions["fit"].GetParameter(1))
        err_s2.append((p.plotted_functions["fit"].GetParError(1)**2+0.04**2)**(0.5))

        N2.append(p.plotted_functions["fit"].GetParameter(2))
        err_N2.append(p.plotted_functions["fit"].GetParError(2))

        p0.append(p.plotted_functions["fit"].GetParameter(5)/p.plotted_functions["fit"].GetParameter(2))
        err_part1 = (p.plotted_functions["fit"].GetParError(5)/p.plotted_functions["fit"].GetParameter(2))**2
        err_part2 = ((p.plotted_functions["fit"].GetParameter(5)/(p.plotted_functions["fit"].GetParameter(2)**2)) *p.plotted_functions["fit"].GetParError(2))**2

        err_p0.append((err_part1+err_part2+0.04**2)**0.5)

    #if err_s1[i]<=0.04:
    #    err_s1[0] +=0.04

#plotted_histograms_items = (plotted_histograms.iteritems())
plotted_histograms_order = sorted(plotted_histograms)
pprint(plotted_histograms)

arr_x = array("f", x[1:])
arr_x_m1 = array("f", x[1:-1])

arr_m1 = array("f", m1[1:-1])
arr_s1 = array("f", s1[1:])
arr_N1 = array("f", N1[1:])
arr_m2 = array("f", m2[1:])
arr_s2 = array("f", s2[1:])
arr_N2 = array("f", N2[1:])
arr_p0 = array("f", p0[1:])

arr_err_x = array("f", err_x[1:])
arr_err_x_m1 = array("f", err_x[1:-1])

arr_err_m1 = array("f", err_m1[1:-1])
arr_err_s1 = array("f", err_s1[1:])
arr_err_N1 = array("f", err_N1[1:])
arr_err_m2 = array("f", err_m2[1:])
arr_err_s2 = array("f", err_s2[1:])
arr_err_N2 = array("f", err_N2[1:])
arr_err_p0 = array("f", err_p0[1:])


Graph_m1 = ROOT.TGraphErrors(len(x)-2, arr_x_m1, arr_m1, arr_err_x_m1, arr_err_m1)
canvas2 = ROOT.TCanvas( "canvas2", "canvas2", 100, 100, 1200, 600 )
Graph_m1.GetXaxis().SetTitle("E_{truth} [GeV]")

Graph_m1.Draw("AP")

fit_m1 = ROOT.TF1("fit_m1", "[0] + [1]*(x)",  0, 2200)
Graph_m1.Fit("fit_m1")
Graph_m1.Draw("same")
canvas2.Update()

canvas2.SaveAs(plottingdict["output_dir"]+"/mu1.png")
canvas2.Close()


Graph_s1 = ROOT.TGraphErrors(len(x)-1, arr_x, arr_s1, arr_err_x, arr_err_s1)
Graph_s1.GetXaxis().SetTitle("E_{truth} [GeV]")

canvas3 = ROOT.TCanvas( "canvas3", "canvas3", 100, 100, 1200, 600 )
Graph_s1.Draw("AP")

fit_s1 = ROOT.TF1("fit_s1", "[0] + [1] * (x)",  0, 2200)
fit_s1.SetParameters(0.5, -10)
Graph_s1.Draw("same")

Graph_s1.Fit("fit_s1")
Graph_s1.GetYaxis().SetRangeUser(0,1)

Graph_s1.Draw("same")
canvas3.Update()

canvas3.SaveAs(plottingdict["output_dir"]+"/sigma1.png")
canvas3.Close()


Graph_m2 = ROOT.TGraphErrors(len(x)-1, arr_x, arr_m2, arr_err_x, arr_err_m2)
Graph_m2.GetXaxis().SetTitle("E_{truth} [GeV]")

canvas4 = ROOT.TCanvas( "canvas4", "canvas4", 100, 100, 1200, 600 )
Graph_m2.Draw("AP")

fit_m2 = ROOT.TF1("fit_m2", "[0] + [1]/sqrt(x)", 0, 2200)
Graph_m2.Fit("fit_m2")
Graph_m2.Draw("same")
canvas4.Update()

canvas4.SaveAs(plottingdict["output_dir"]+"/mu2.png")
canvas4.Close()


Graph_s2 = ROOT.TGraphErrors(len(x)-1, arr_x, arr_s2, arr_err_x, arr_err_s2)
canvas5 = ROOT.TCanvas( "canvas5", "canvas5", 100, 100, 1200, 600 )
Graph_s2.GetXaxis().SetTitle("E_{truth} [GeV]")

Graph_s2.Draw("AP")
Graph_s2.GetYaxis().SetRangeUser(0,0.25)

Graph_s2.Draw("AP")


fit_s2 = ROOT.TF1("fit_s2", "[0] + [1]*x",  0, 2200)
fit_s2.SetParameters(0.1, 0.01)

Graph_s2.Fit("fit_s2")
Graph_s2.Draw("same")
canvas5.Update()

canvas5.SaveAs(plottingdict["output_dir"]+"/sigma2.png")
canvas5.Close()


Graph_p0 = ROOT.TGraphErrors(len(x)-1, arr_x, arr_p0, arr_err_x, arr_err_p0)
Graph_p0.GetYaxis().SetRangeUser(-1,1)
canvas6 = ROOT.TCanvas( "canvas6", "canvas6", 100, 100, 1200, 600 )
Graph_p0.GetXaxis().SetTitle("E_{truth} [GeV]")


Graph_p0.Draw("AP")
Graph_p0.GetYaxis().SetRangeUser(-1,1)
Graph_p0.Draw("AP")

fit_p0 = ROOT.TF1("fit_p0", "[0] + [1]/x",  0, 2200)
fit_p0.SetParameters(0.1,100)
Graph_p0.Fit("fit_p0")
Graph_p0.Draw("same")
canvas6.Update()

canvas6.SaveAs(plottingdict["output_dir"]+"p0.png")
canvas6.Close()



def setparameters(mu1_a, mu1_b, s1_a, s1_b, mu_2_a, mu2_b, s2_a, s2_b, p0_a, p0_b, k= 0.1):
    mu1_a_gf = random.uniform(mu1_a-k*fit_m1.GetParError(0), mu1_a+k*fit_m1.GetParError(0))
    mu1_b_gf = random.uniform(mu1_b-k*fit_m1.GetParError(1), mu1_b+k*fit_m1.GetParError(1))

    s1_a_gf = random.uniform(s1_a-3*k*fit_s1.GetParError(0), s1_a+3*k*fit_s1.GetParError(0))
    s1_b_gf = random.uniform(s1_b-3*k*fit_s1.GetParError(1), s1_b+3*k*fit_s1.GetParError(1))

    mu2_a_gf = random.uniform(mu2_a-k*fit_m2.GetParError(0), mu2_a+k*fit_m2.GetParError(0))
    mu2_b_gf = random.uniform(mu2_b-k*fit_m2.GetParError(1), mu2_b+k*fit_m2.GetParError(1))

    s2_a_gf = random.uniform(s2_a-3*k*fit_s2.GetParError(0), s2_a+3*k*fit_s2.GetParError(0))
    s2_b_gf = random.uniform(s2_b-3*k*fit_s2.GetParError(1), s2_b+3*k*fit_s2.GetParError(1))

    p0_a_gf = random.uniform(p0_a-k*fit_p0.GetParError(0), p0_a+k*fit_p0.GetParError(0))
    p0_b_gf = random.uniform(p0_b-k*fit_p0.GetParError(1), p0_b+k*fit_p0.GetParError(1))

    return mu1_a_gf, mu1_b_gf, s1_a_gf, s1_b_gf, mu2_a_gf, mu2_b_gf, s2_a_gf, s2_b_gf, p0_a_gf, p0_b_gf

def set_mu1(a ,b, E):
    return a + b * (E)

def set_s1(a, b, E):
    return max(0.01,a+b*E)

def set_mu2(a, b, E):
    return a + b/sqrt(E)

def set_s2(a, b, E):
    return max(0.01,a+b*E)

def set_p0(a,b,E):
    return max(0.001,a + b/E)


def set_doublegaussian(N, mu1, s1, mu2, s2, p0, dE):
    return N/(sqrt(2*pi)*(s2+s1*p0)) *( exp(-(dE-mu2)**2/(2*s2**2)) + p0 *exp(-(dE-mu1)**2/(2*s1**2)))

mu1_a_init = fit_m1.GetParameter(0)
mu1_b_init = fit_m1.GetParameter(1)

s1_a_init = fit_s1.GetParameter(0)
s1_b_init = fit_s1.GetParameter(1)

mu2_a_init = fit_m2.GetParameter(0)
mu2_b_init = fit_m2.GetParameter(1)

s2_a_init = fit_s2.GetParameter(0)
s2_b_init = fit_s2.GetParameter(1)

p0_a_init = fit_p0.GetParameter(0)
p0_b_init = fit_p0.GetParameter(1)




lnL_final = 0
n_iters = 1000
_k =0.1



for iteration in range(n_iters):
    _k*=0.999
    print "============================"
    print "iteration: \t", iteration
    print "============================"

    lnL_new = 0

    if iteration >0:
        mu1_a, mu1_b, s1_a, s1_b, mu2_a, mu2_b, s2_a, s2_b, p0_a, p0_b = setparameters(mu1_a_final, mu1_b_final, s1_a_final, s1_b_final, mu2_a_final, mu2_b_final, s2_a_final, s2_b_final, p0_a_final, p0_b_final, k=_k)
    else:
        mu1_a = mu1_a_init
        mu1_b = mu1_b_init
        s1_a  = s1_a_init
        s1_b  = s1_b_init
        mu2_a = mu2_a_init
        mu2_b = mu2_b_init
        s2_a  = s2_a_init
        s2_b  = s2_b_init
        p0_a  = p0_a_init
        p0_b  = p0_b_init


    print "Energy: \t\t mu1: \t s1: \t mu2:\t s2: \t p0"


    for Energy in plotted_histograms_order:
        #print "Energy: \t", Energy
        nick = plotted_histograms[Energy].keys()[0]
        hist =  plotted_histograms[Energy][nick]

        mu1 = set_mu1(mu1_a, mu1_b, Energy)
        s1 = set_s1(s1_a, s1_b, Energy)
        mu2 = set_mu2(mu2_a, mu2_b, Energy)
        s2 = set_s2(s2_a, s2_b, Energy)
        p0 = set_p0(p0_a, p0_b, Energy)


        print "{:f} \t\t {:0.2f} \t {:0.2f} \t {:0.2f} \t {:0.2f} \t {:0.2f}".format(Energy, mu1, s1, mu2, s2, p0)

        integral = hist.Integral("width")
        N = integral
        #print "Integral hist:\t", N

        #N = N / (sqrt(2*pi)*(s2+p0*s1))
        #print "N:\t", N
        n_preds = []
        n_preds_e = []
        xs = []

        if iteration == 0:
            if Energy == 1150:
                mu1_e = 0.17
                s1_e = 0.42
                mu2_e = 0.04
                s2_e = 0.13
                p0_e = 8.1/94.51
                N_e = (94.51) *(sqrt(2*pi)*(s2_e+p0_e*s1_e))

        for bin in range(hist.GetNbinsX()):
            dE = hist.GetBinCenter(bin+1)
            n_data = hist.GetBinContent(bin+1)
            n_pred = set_doublegaussian(N, mu1, s1, mu2, s2, p0, dE)
            #if n_data <= 0:
            #    print "n_data: \t", n_data
            if n_pred <= 0:
                print "n_pred:\t", n_pred
            if iteration ==0:
                n_preds.append(n_pred)
                xs.append(dE)
                if Energy == 1150:
                    n_pred_e = set_doublegaussian(N_e, mu1_e, s1_e, mu2_e, s2_e, p0_e, dE)
                    n_preds_e.append(n_pred_e)

            ##print "delta E: \t", dE
            ##print "N Predicted:\t", n_pred
            ##print "N Data:\t", n_data



            if Energy>0:
                lnL_new +=  log(n_pred)*(n_data) - log(factorial(int(n_data))) - n_pred
        #print "lnL_new:\t", lnL_new

        if iteration == 0:
            dicts[Energy]["plottingdict"]["filename"] = "test_" +str(int(Energy))
            dicts[Energy]["plottingdict"]["filetype"] = "pdf"
            #dicts[Energy]["histdictslist"][0]["fit"]["type"] = ""

            #pprint( dicts[Energy])
            p.create_plot(dicts[Energy])


            arr_xs = array("f", xs)
            arr_npreds = array("f", n_preds)
            arr_npreds_e = array("f", n_preds_e)

            Graph_m2 = ROOT.TGraph(len(xs), arr_xs, arr_npreds)
            Graph_m2.Draw("psame")

            if Energy == 1150:

                Graph_m2_e = ROOT.TGraph(len(xs), arr_xs, arr_npreds_e)
                Graph_m2_e.Draw("*same")
                #print "integral function: \t", p.plotted_functions["fit"].Integral(-2,2)

            p.save_plot(dicts[Energy])




    if iteration == 0:
        #p.c.Print(plottingdict["output_dir"] + "test.pdf]")
        pass
        #print "____________________________________________"

    print lnL_new
    try:
        print lnL_final
    except:
        pass
    P_new = exp(lnL_new)
    if iteration == 0:
        lnL_init = lnL_new
        P_init = P_new

        lnL_final = lnL_new
        P_final = P_new

        mu1_a_final = mu1_a
        mu1_b_final = mu1_b
        s1_a_final  = s1_a
        s1_b_final  = s1_b
        mu2_a_final = mu2_a
        mu2_b_final = mu2_b
        s2_a_final  = s2_a
        s2_b_final  = s2_b
        p0_a_final  = p0_a
        p0_b_final  = p0_b




    else:
        if lnL_new>lnL_final:
            _k *=1.1
            P_final = P_new
            lnL_final=lnL_new


            mu1_a_final = mu1_a
            mu1_b_final = mu1_b
            s1_a_final  = s1_a
            s1_b_final  = s1_b
            mu2_a_final = mu2_a
            mu2_b_final = mu2_b
            s2_a_final  = s2_a
            s2_b_final  = s2_b
            p0_a_final  = p0_a
            p0_b_final  = p0_b
        else:
            rn = random.uniform(0,1)

            if (lnL_new-lnL_final)/20 > log(rn):
                #_k *=1.5

                P_final=P_new
                lnL_final=lnL_new

                mu1_a_final = mu1_a
                mu1_b_final = mu1_b
                s1_a_final  = s1_a
                s1_b_final  = s1_b
                mu2_a_final = mu2_a
                mu2_b_final = mu2_b
                s2_a_final  = s2_a
                s2_b_final  = s2_b
                p0_a_final  = p0_a
                p0_b_final  = p0_b



print "lnL_final:\t", lnL_final
print "lnL_init:\t", lnL_init
print "Energy: \t\t mu1: \t s1: \t mu2:\t s2: \t p0"



for Energy in plotted_histograms_order:

    n_preds_final = []
    x_f =[]

    nick = plotted_histograms[Energy].keys()[0]
    hist =  plotted_histograms[Energy][nick]

    N_final = hist.Integral("width")

    mu1_final = set_mu1(mu1_a_final, mu1_b_final, Energy)
    s1_final = set_s1(s1_a_final, s1_b_final, Energy)
    mu2_final = set_mu2(mu2_a_final, mu2_b_final, Energy)
    s2_final = set_s2(s2_a_final, s2_b_final, Energy)
    p0_final = set_p0(p0_a_final, p0_b_final, Energy)

    mu1_init = set_mu1(mu1_a_init, mu1_b_init, Energy)
    s1_init = set_s1(s1_a_init, s1_b_init, Energy)
    mu2_init = set_mu2(mu2_a_init, mu2_b_init, Energy)
    s2_init = set_s2(s2_a_init, s2_b_init, Energy)
    p0_init = set_p0(p0_a_init, p0_b_init, Energy)


    print "{:f} \t\t {:0.2f} \t {:0.2f} \t {:0.2f} \t {:0.2f} \t {:0.2f}".format(Energy, mu1_final, s1_final, mu2_final, s2_final, p0_final)
    print "{:f} \t\t {:0.2f} \t {:0.2f} \t {:0.2f} \t {:0.2f} \t {:0.2f}".format(Energy, mu1_init, s1_init, mu2_init, s2_init, p0_init)
    print("\n")

    for bin in range(hist.GetNbinsX()):
        dE = hist.GetBinCenter(bin+1)
        x_f.append(dE)
        n_pred_final = set_doublegaussian(N_final, mu1_final, s1_final, mu2_final, s2_final, p0_final, dE)
        n_preds_final.append(n_pred_final)


    dicts[Energy]["plottingdict"]["filename"] = "final_"+str(int(Energy))
    dicts[Energy]["plottingdict"]["filetype"] = "pdf"
    dicts[Energy]["histdictslist"][0]["fit"]["type"] = ""

    p.create_plot(dicts[Energy])


    arr_npreds_final = array("f", n_preds_final)
    arr_x_f = array("f", x_f)


    Graph_m2_final = ROOT.TGraph(len(x_f), arr_x_f, arr_npreds_final)
    Graph_m2_final.Draw("psame")
    p.save_plot(dicts[Energy])
#p.c.Print(plottingdict["output_dir"] + "final.pdf]")

dict_pars={}
dict_pars["mu1_a"] = mu1_a_final
dict_pars["mu1_b"] = mu1_b_final

dict_pars["s1_a"] = s1_a_final
dict_pars["s1_b"] = s1_b_final

dict_pars["mu2_a"] = mu2_a_final
dict_pars["mu2_b"] = mu2_b_final

dict_pars["s2_a"] = s2_a_final
dict_pars["s2_b"] = s2_b_final

dict_pars["p0_a"] = p0_a_final
dict_pars["p0_b"] = p0_b_final

with open(plottingdict["output_dir"] + "final.json", 'w') as _jfile:
    json.dump(dict_pars , _jfile, indent=4) #
