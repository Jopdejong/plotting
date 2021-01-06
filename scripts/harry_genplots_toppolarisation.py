#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os

import Artus.Utility.jsonTools as jsonTools

import Artus.HarryPlotter.harry as harry

import plotconfig as pc

import sys


## TODO: clean up using classes like binnings and labels
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Make polariation plots.",
		parents=[logger.loggingParser])

	parser.add_argument("-i", "--input", nargs="+", default=["ctW-c8.root",
	"ctW-c6.root", "ctW-c4.root", "ctW-c2.root",
	"SM-c0.root", "ctW-c-2.root", "ctW-c-4.root", "ctW-c-6.root",
	"ctW-c-8.root"], help="Input rootfiles.")
	parser.add_argument("-d", "--input-dir", type=str,
		help="input directory to find the rootfiles, all paths are relative to this path")
	parser.add_argument("-a", "--args", default="",
		help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
		help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--folder", type=str, default="Event",
		help="root folder. [Default: %(default)s]")
	parser.add_argument("-x", "--quantities", nargs="+", default=["z_pol","xl_pol", "xl_pol_tcm", "u_pol", "CosTheta_xl", "CosTheta_ql","CosTheta_yl", "CosTheta_zl", "CosTheta_Nl","CosTheta_Tl", "CosTheta_xl_reco", "CosTheta_ql_reco","CosTheta_yl_reco", "CosTheta_zl_reco", "CosTheta_Nl_reco","CosTheta_Tl_reco", "xl_pol_tcm_reco" ],
		help = "quantities to be plotted")
	parser.add_argument("-w", "--weights", type=str, default= "(1)",
		help="weights to be applied")
	parser.add_argument("--title", type=str, default= "",
		help="title for the plot")
	parser.add_argument("-o", "--output-dir",
		default="/user/jdegens/analysis/plots/gen_pol_plots/",
		help="Output directory. [Default: %(default)s]")
	parser.add_argument("--www", default=None,
		help="Output directory. [Default: %(default)s]")
	parser.add_argument("--ratio", default=True, action="store_false",
		help="make a ratio plot")
	parser.add_argument("--normalize-to-unity", default=True, action="store_false",
		help="normalize to unity")
	parser.add_argument("--calculate-asymmetry", default=True, action="store_false",
		help="calculate assymetries")
	parser.add_argument("--create-asymmetry-plot", default=True, action="store_false",
		help="calculate assymetries")
	parser.add_argument("--reco-comparison", default=False, action="store_true",
		help="calculate assymetries")
	parser.add_argument("--nicks", nargs="+", default=["ctw8", "ctw6","ctw4", "ctw2","sm","ctw-2","ctw-4","ctw-6","ctw-8"], help="Input rootfiles.")
	parser.add_argument("-c", "--colors", nargs="+", default=None, help="Input rootfiles.")
	parser.add_argument("-m", "--markers", nargs="+", default=["LINE"], help="Input rootfiles.")
	parser.add_argument( "--legend-markers", nargs="+", default=["LINE"], help="Input rootfiles.")

	parser.add_argument("-l", "--line-styles", type = int, nargs="+", default=[1], help="Input rootfiles.")
	parser.add_argument("--marker-styles", type = int, nargs="+", default=[], help="Input rootfiles.")

	parser.add_argument("--n-plots", type=int,
		help="Number of plots. [Default: all]")
	parser.add_argument("--legend-cols", type=int, default=3,
		help="Number of plots. [Default: %(default)]")

	args = parser.parse_args()
	logger.initLogger(args)

	original_quantities = args.quantities

	if "LHE" in args.quantities:
		args.quantities = ["CosTheta_xl", "CosTheta_ql","CosTheta_yl", "CosTheta_zl", "CosTheta_Nl", "CosTheta_Tl", "xl_pol_tcm"] #, "z_pol" , "u_pol"
	elif "reco" in args.quantities:
		args.quantities = ["CosTheta_xl_reco", "CosTheta_ql_reco","CosTheta_yl_reco", "CosTheta_zl_reco",  "xl_pol_tcm_reco", "CosTheta_Nl_reco","CosTheta_Tl_reco"] #"CosTheta_Nl_reco","CosTheta_Tl_reco",
	elif "reco_a" in args.quantities:
		args.quantities = ["CosTheta_xl_reco_a", "CosTheta_ql_reco_a","CosTheta_yl_reco_a", "CosTheta_zl_reco_a",  "xl_pol_tcm_reco_a", "CosTheta_Nl_reco_a","CosTheta_Tl_reco_a"] #"CosTheta_Nl_reco_a","CosTheta_Tl_reco_a",
	elif "reco_b" in args.quantities:
		args.quantities = ["CosTheta_xl_reco_b", "CosTheta_ql_reco_b","CosTheta_yl_reco_b", "CosTheta_zl_reco_b",  "xl_pol_tcm_reco_b"] #"CosTheta_Nl_reco_b","CosTheta_Tl_reco_b",
	elif "godbole" in args.quantities:
		args.quantities = ["z_pol", 'u_pol', "xl_pol", "xl_pol_tcm"]
	elif "godbole_reco" in args.quantities:
		args.quantities = ["z_pol_reco", 'u_pol', "xl_pol", "xl_pol_tcm_reco"]
	elif "godbole_reco_a" in args.quantities:
		args.quantities = ["z_pol_reco_a", 'u_pol', "xl_pol", "xl_pol_tcm_reco_a"]

	print args.quantities


	if args.reco_comparison:
		if len(args.quantities) >2:
			"more than two x values comparing reco and lhe not yet supported"
		if len(args.quantities) == 1:
			for i in ["_reco", "_reco_a", "_reco_b"]:
				args.quantities.append(args.quantities[0]+i)
	print args.quantities

	plot_config = {}
	config_lists = []

	plot_config["calculate_asymmetry_outputfile"] = args.output_dir+"/assymetries.txt"
	file = open(plot_config["calculate_asymmetry_outputfile"], "w")
	file.close()

	plot_config["formats"] = ["png","pdf"]
	plot_config["output_dir"] = args.output_dir
	plot_config["directories"] = [args.input_dir]
	plot_config["files"] = []
	#for file in args.input:
		#plot_config["files"].append("hepmc_"+file)
	plot_config["files"] = args.input
	plot_config["nicks"] = []
	plot_config["folders"] = args.folder
	plot_config["markers"] = args.markers
	plot_config["legend_markers"] = args.legend_markers
	plot_config["line_styles"] = map(int,args.line_styles)
	plot_config["marker_styles"] = map(int,args.marker_styles)

	plot_config["weights"] = [args.weights]

	plot_config["title"] = args.title

	for nick in args.nicks:
		print nick
		if nick != "sm":
			plot_config["nicks"].append(str(nick)) #"i"+
		else:
			plot_config["nicks"].append(str(nick))

	print plot_config["nicks"]
	#TODO move this to a class, such that it can be used in different places
	if args.www !=None:
		plot_config["www"] = args.www

	pc_class = pc.PlotConfigs()

	#labels = {}
	#labels["u_pol"] = "u"
	#labels["z_pol"] = "z"
	#labels["xl_pol"] = "x_{l}^{lab}"
	#labels["xl_pol_tcm"] = "x_{l}^{top}"
	#labels["CosTheta_xl"] = "cos(#theta_{xl})"
	#labels["CosTheta_yl"] = "cos(#theta_{yl})"
	#labels["CosTheta_zl"] = "cos(#theta_{zl})"
	#labels["CosTheta_ql"] = "cos(#theta_{ql})"
	#labels["CosTheta_Tl"] = "cos(#theta_{Tl})"
	#labels["CosTheta_Nl"] = "cos(#theta_{Nl})"

	#labels["CosTheta_xl_reco"] = "reco cos(#theta_{xl})"
	#labels["CosTheta_yl_reco"] = "reco cos(#theta_{yl})"
	#labels["CosTheta_zl_reco"] = "reco cos(#theta_{zl})"
	#labels["CosTheta_ql_reco"] = "reco cos(#theta_{ql})"
	#labels["CosTheta_Tl_reco"] = "reco cos(#theta_{Tl})"
	#labels["CosTheta_Nl_reco"] = "reco cos(#theta_{Nl})"
	#labels["xl_pol_tcm_reco"]  = "reco x_{l}^{top}"
	#labels["z_pol_reco"] = "reco z"

	#labels["CosTheta_xl_reco_a"] = "reco_a cos(#theta_{xl})"
	#labels["CosTheta_yl_reco_a"] = "reco_a cos(#theta_{yl})"
	#labels["CosTheta_zl_reco_a"] = "reco_a cos(#theta_{zl})"
	#labels["CosTheta_ql_reco_a"] = "reco_a cos(#theta_{ql})"
	#labels["CosTheta_Tl_reco_a"] = "reco_a cos(#theta_{Tl})"
	#labels["CosTheta_Nl_reco_a"] = "reco_a cos(#theta_{Nl})"
	#labels["xl_pol_tcm_reco_a"]  = "reco_a x_{l}^{top}"
	#labels["z_pol_reco_a"] = "reco_a z"

	#labels["CosTheta_xl_reco_b"] = "reco_b cos(#theta_{xl})"
	#labels["CosTheta_yl_reco_b"] = "reco_b cos(#theta_{yl})"
	#labels["CosTheta_zl_reco_b"] = "reco_b cos(#theta_{zl})"
	#labels["CosTheta_ql_reco_b"] = "reco_b cos(#theta_{ql})"
	#labels["CosTheta_Tl_reco_b"] = "reco_b cos(#theta_{Tl})"
	#labels["CosTheta_Nl_reco_b"] = "reco_b cos(#theta_{Nl})"
	#labels["xl_pol_tcm_reco_b"]  = "reco_b x_{l}^{top}"
	#labels["z_pol_reco_b"] = "reco_b z"

	#labels["TopPT"] = "p_{T}^{top}"
	#labels["BottomPT"] = "p_{T}^{b}"
	#labels["JetPT"] = "p_{T}^{jet}"

	#asymmetrypoints = {}
	#binnings = {}
	#for ext in ["", "_reco", "_reco_a", "_reco_b"]:
	#	asymmetrypoints["u_pol"+ext] = 0.5
	#	asymmetrypoints["z_pol"+ext] = 0.5
	#	asymmetrypoints["xl_pol"+ext] = 0.5
	#	asymmetrypoints["xl_pol_tcm"+ext] = 0.5
	#	asymmetrypoints["CosTheta_xl"+ext] = 0
	#	asymmetrypoints["CosTheta_yl"+ext] = 0
	#	asymmetrypoints["CosTheta_zl"+ext] = 0
	#	asymmetrypoints["CosTheta_ql"+ext] = -0.25
	#	asymmetrypoints["CosTheta_Tl"+ext] = 0
	#	asymmetrypoints["CosTheta_Nl"+ext] = 0

	#	binnings["u_pol"+ext] = ["8,0,1"]
	#	binnings["z_pol"+ext] = ["8,0,1"]
	#	binnings["xl_pol"+ext] = ["20,0,5"]
	#	binnings["xl_pol_tcm"+ext] = ["8,0,1"]
	#	binnings["CosTheta_xl"+ext] = ["8,-1,1"]
	#	binnings["CosTheta_yl"+ext] = ["8,-1,1"]
	#	binnings["CosTheta_zl"+ext] = ["8,-1,1"]
	#	binnings["CosTheta_ql"+ext] = ["8,-1,1"]
	#	binnings["CosTheta_Tl"+ext] = ["8,-1,1"]
	#	binnings["CosTheta_Nl"+ext] = ["8,-1,1"]

	#binnings["TopPT"] = ["25,0,500"]
	#binnings["JetPT"] = ["25,0,500"]
	#binnings["JetE"] = ["25,0,500"]
	#binnings["BottomPT"] = ["15,0,300"]
	#asymmetrypoints["TopPT"] = 100
	#asymmetrypoints["JetPT"] = 75
	#asymmetrypoints["JetE"] = 150




	plot_config["labels"] = copy.deepcopy(args.nicks)

	plot_config["legend"] = [0.6, 0.7, 0.9, 0.89]
	plot_config["legend_cols"] = args.legend_cols

	#plot_config["redo_cache"] = True
	plot_config["y_subplot_lims"] = [0.5,1.5]

	if args.colors != None:
		plot_config["colors"] = args.colors

	#FIXME now if you give the argument you actualy make true to false which might be confusing
	plot_config["analysis_modules"] = []
	if args.normalize_to_unity:
		plot_config["analysis_modules"].append("NormalizeToUnity")
	if args.calculate_asymmetry:
		plot_config["analysis_modules"].append("CalculateAsymmetry")
	if args.ratio:
		plot_config["analysis_modules"].append("Ratio")
		if "sm" in plot_config["nicks"]:
			plot_config["ratio_denominator_nicks"] = ["sm"]
		else:
			print "making a ratio without the sm nick, this is not yet really supported"
			sys.exit()
		plot_config["ratio_numerator_nicks"] = plot_config["nicks"]
		print args.nicks

		for i in range(len(plot_config["ratio_numerator_nicks"])):
			plot_config["labels"].append("")


	for var in args.quantities:
		print "making config for variable:", var
		plot_config["x_expressions"] = var

		plot_config["x_bins"], plot_config["x_label"] = pc_class.set_plotconfig(var)

		#try:
		#	plot_config["x_label"] = labels[var]
		#except KeyError:
		#	print "x label not specified"
		#	plot_config["x_label"] = str(var)
		#try:
		#	plot_config["x_bins"] = binnings[var]
		#except KeyError:
		#	print "binning not specified setting it to:"
		#	plot_config["x_bins"] =  '0 0.025 0.05 0.075 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.'
		#	print plot_config["x_bins"]


		if args.calculate_asymmetry:
			try:
				plot_config["calculate_asymmetry_reference"] = pc_class.asymmetry.set_assymetrypoint(var)
			except KeyError:
				print "no assymetry reference set"
				plot_config["calculate_asymmetry_reference"] = 100

		config_lists.append(copy.deepcopy(plot_config))

	harry.HarryPlotter(list_of_config_dicts=config_lists, list_of_args_strings=args.args,
		n_processes=args.n_processes, n_plots=args.n_plots
	)

	################create assymetry plots###################
	if args.create_asymmetry_plot:
		file = open(plot_config["calculate_asymmetry_outputfile"], "r")

		lines=file.readlines()

		assymetries_plotdict = {}

		assymetries_plotdict["labels"]=[]
		assymetries_plotdict["x_expressions"]=[]
		assymetries_plotdict["y_expressions"]=[]

		assymetries_plotdict["input_modules"] ="InputInteractive"
		for i in range(len(lines)/3):
			assymetries_plotdict["labels"].append( lines[3*i][:-1])
			assymetries_plotdict["x_expressions"].append([lines[3*i+1][:-1]])
			assymetries_plotdict["y_expressions"].append([lines[3*i+2][:-1]])

		labels_backup = copy.deepcopy(assymetries_plotdict["labels"])
		x_backup = copy.deepcopy(assymetries_plotdict["x_expressions"])
		y_backup = copy.deepcopy(assymetries_plotdict["y_expressions"])

		print assymetries_plotdict["labels"]
		color_dict = {}
		marker_style_dict = {}
		line_style_dict = {}

		color_dict["u"] = "#E74C3C"
		marker_style_dict["u"] = 20
		line_style_dict["u"]= 8


		color_dict["z"] = "#8E44AD"
		marker_style_dict["z"] = 21
		line_style_dict["z"]= 1
		#assymetries_plotdict["nicks"] = assymetries_plotdict["labels"]


		if args.reco_comparison:
			for j in range(len(labels_backup)):
				print labels_backup[j]
				if labels_backup[j].startswith("reco_b"):
					assymetries_plotdict["labels"][3] = labels_backup[j]
					assymetries_plotdict["x_expressions"][3] = x_backup[j]
					assymetries_plotdict["y_expressions"][3] = y_backup[j]
				elif labels_backup[j].startswith("reco_a"):
					assymetries_plotdict["labels"][2] = labels_backup[j]
					assymetries_plotdict["x_expressions"][2] = x_backup[j]
					assymetries_plotdict["y_expressions"][2] = y_backup[j]
				elif labels_backup[j].startswith("reco"):
					assymetries_plotdict["labels"][1] = labels_backup[j]
					assymetries_plotdict["x_expressions"][1] = x_backup[j]
					assymetries_plotdict["y_expressions"][1] = y_backup[j]
				else:
					assymetries_plotdict["labels"][0] = labels_backup[j]
					assymetries_plotdict["x_expressions"][0] = x_backup[j]
					assymetries_plotdict["y_expressions"][0] = y_backup[j]

			for i in ["x_{l}^{top}", "cos(#theta_{xl})", "cos(#theta_{yl})", "cos(#theta_{zl})", "cos(#theta_{ql})", "cos(#theta_{Tl})", "cos(#theta_{Nl})", "z_pol"]:
				color_dict[i] = "#3498DB"
				marker_style_dict[i] = 20
				line_style_dict[i] = 1

				color_dict["reco "+ i] = "#16A085"
				marker_style_dict["reco "+ i] = 21
				line_style_dict["reco "+ i] = 2

				color_dict["reco_a "+ i] = "#F39C12"
				marker_style_dict["reco_a "+ i] = 22
				line_style_dict["reco_a "+ i] = 3

				color_dict["reco_b "+ i] = "#E74C3C"
				marker_style_dict["reco_b "+ i] = 23
				line_style_dict["reco_b "+ i] = 4

				#if i in assymetries_plotdict["labels"][0]:
				#	assymetries_plotdict["nicks_whitelist"] = [i, "reco "+ i, "reco_a "+ i, "reco_b "+ i]

		else:
			for i in ["", "reco ", "reco_a ", "reco_b "]:
				color_dict[i+"x_{l}^{top}"] = "#3498DB"
				marker_style_dict[i+"x_{l}^{top}"] = 22
				line_style_dict[i+"x_{l}^{top}"] = 2

				color_dict[i+"cos(#theta_{xl})"] = "#16A085"
				marker_style_dict[i+"cos(#theta_{xl})"] = 23
				line_style_dict[i+"cos(#theta_{xl})"] = 3

				color_dict[i+"cos(#theta_{yl})"] = "#F39C12"
				marker_style_dict[i+"cos(#theta_{yl})"] = 24
				line_style_dict[i+"cos(#theta_{yl})"] = 4

				color_dict[i+"cos(#theta_{zl})"] = "#2C3E50"
				marker_style_dict[i+"cos(#theta_{zl})"] = 25
				line_style_dict[i+"cos(#theta_{zl})"] = 5

				color_dict[i+"cos(#theta_{ql})"] = "#D4E157"
				marker_style_dict[i+"cos(#theta_{ql})"] = 26
				line_style_dict[i+"cos(#theta_{ql})"] = 6

				color_dict[i+"z"] = "#8E44AD"
				marker_style_dict[i+"z"] = 21
				line_style_dict[i+"z"]= 1
				#color_dict["CosTheta_Tl"] = ""
				#color_dict["CosTheta_Nl"] = ""

		#print assymetries_plotdict["nicks_whitelist"]
		#print assymetries_plotdict["nicks"]

		color_dict['x_{l}^{lab}'] = "#2471A3"
		marker_style_dict['x_{l}^{lab}'] = 27
		line_style_dict['x_{l}^{lab}'] = 7


		assymetries_plotdict["x_expressions"]= assymetries_plotdict["x_expressions"][0]
		assymetries_plotdict["y_label"]= "Asymmetry"
		assymetries_plotdict["x_label"]= "Re(ctW)"

		assymetries_plotdict["formats"] = ["png","pdf"]
		assymetries_plotdict["markers"] = ["LP"]
		assymetries_plotdict["legend"] = [0.25, 0.65, 0.875, 0.92]
		assymetries_plotdict["legend_cols"] = 3
		assymetries_plotdict["filename"] = "assymetry_"+("_".join(original_quantities[0].replace("/","___"))) #TODO
		assymetries_plotdict["y_lims"] = [-1,1]
		assymetries_plotdict["www"] = "JEC_shifts"

		assymetries_plotdict["colors"] = []
		assymetries_plotdict["marker_styles"]=[]
		assymetries_plotdict["line_styles"] = []
		for i,var in enumerate(assymetries_plotdict["labels"]):
			try:
				assymetries_plotdict["colors"].append(color_dict[var])
			except KeyError:
				print "Could not find color key"
				assymetries_plotdict["colors"].append(str(i+1))
			try:
				assymetries_plotdict["marker_styles"].append(marker_style_dict[var])
			except KeyError:
				print "Could not find marker style key"
				assymetries_plotdict["marker_styles"].append(28+i)
			try:
				assymetries_plotdict["line_styles"].append(line_style_dict[var])
			except KeyError:
				print "Could not find line style key"
				assymetries_plotdict["line_styles"].append(8+i)

		harry.HarryPlotter(list_of_config_dicts=[assymetries_plotdict], list_of_args_strings=" --log-level debug",
			n_processes=1, n_plots=args.n_plots
		)
