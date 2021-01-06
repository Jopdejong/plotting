#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import argparse
import webplot
import hist, hist2d, default_style_atlas
from pprint import pprint



import os, re, sys, json, copy



#Thinking about moving some of the more advanced stuff into a new file inhereting from this
class Plotter(object): #object makes sure that inhereting from this is possible
	#set some initial variables, such as normalize and create ratio
	def __init__(self):
		self.plotnumber = 0

		self.df_style = default_style_atlas.DefaulStyleAtlas()

		self.ratio = False
		self.show_legend = True
		self.legend_lowerx, self.legend_lowery,self.legend_upperx,self.legend_uppery = [0.7,0.75,0.77,0.9]
		self.bsub=False
		self.Hist1DClass = hist.Hist()
		self.Hist2DClass = hist2d.Hist2D()

		self.canvas_size_x = 600
		self.canvas_size_y = 600
		self.saved_files = []

	#def __del__(self):
	#	for file in self.saved_files:
	#		print file
	#		print self.c
	#		self.c.Print(file+ "]")
	#		#close files


	#set some plotdefaults which is needed for each THIST like xmin/max bins.TODO ADD/MOVE some variables
	def set_plotdefaults(self):
		if self.plottingdict.get("dim", 1) ==1:
			dimension =1
		elif self.plottingdict.get("dim", 1) ==2:
			dimension = 2
		self.df_style.set_atlas_style(dimension)

		self.Hist1DClass.set_plotdefaults(self.plottingdict) #this is input to TH1F
		self.Hist2DClass.set_plotdefaults(self.plottingdict)

		if "canvas_size_x" in self.plottingdict.keys():
			self.canvas_size_x =  self.plottingdict["canvas_size_x"]
		if "canvas_size_y" in self.plottingdict.keys():
			self.canvas_size_y =  self.plottingdict["canvas_size_y"]
		#these are not input to TH1F
		self.outputfile = self.plottingdict["output_dir"] + self.plottingdict["filename"] +"."+ self.plottingdict["filetype"]
		self.make_output_dir(self.outputfile)
		self.json_name = self.plottingdict["output_dir"] + self.plottingdict["filename"] +".json"

	@staticmethod
	def make_output_dir(_dir):
		_dir_splitted = _dir.split("/")
		#_dir_splitted = _dir_splitted[:]
		i=2
		while (i!=len(_dir_splitted) ):
			if os.path.isdir("/".join(_dir_splitted[:i])):
				pass
			else:
				print "making directory: {}".format("/".join(_dir_splitted[:i]))
				os.mkdir("/".join(_dir_splitted[:i]))
			i+=1

	def update_histdictslist(self,histdictslist): #why do i do this again?
		if  len(histdictslist) ==None:
			pass
		elif len(histdictslist) == len(self.outdictlist):
			for q, plotdict in enumerate(histdictslist):
				self.outdictlist[q].update(plotdict)

		else:
			print "warning not the same size, may cause problems"
			for q, plotdict in enumerate(histdictslist):
				self.outdictlist[q].update(plotdict)


		######### TODO:  make this a seperate function
	def create_histlist(self,q, histdict):
		self.q = q

		if "yvar" in histdict.keys():
			print "making 2d hist"
			self.HistClass = self.Hist2DClass
			self.show_legend = False
			x=self.HistClass.make_histogram(histdict)
		else:
			self.HistClass = self.Hist1DClass
			x=self.HistClass.make_histogram(histdict) #x is a TH1F
			if self.HistClass.maxy > self.maximaly:
				self.maximaly = self.HistClass.maxy

		histdict["markerstyle"] = self.HistClass.markerstyle #not very elegant to go from one to the other

		## TODO: make a fuction that will reprocess the histogram and do something with it
		## for example calculate an Assymetry, or calculate difference between histogramms.

		##maybe a second loop which draws them such that I can to something inbetween?
		##For example make a Ratio with one of the histograms

		#make sure the histograms are assigned to the correct stack, if None just draw it outside a stack
		print "entries:\t", x.GetEntries()
		if "stack" in histdict.keys():
			if histdict["stack"] in self.stacks.keys():
				self.stacks[histdict["stack"]].Add(copy.deepcopy(x))
			else:
				self.stacks[histdict["stack"]] = ROOT.THStack(histdict["stack"] ,"stack {}".format(histdict["stack"]))
				self.stacks[histdict["stack"]].Add(copy.deepcopy(x))
		else:
			if self.HistClass.nick in self.plotted_histograms.keys():
				print "nick already in histogramdict, making key:\t", str(self.nick)+str(self.q)
				histkey = str(self.HistClass.nick)+str(self.q)
				histdict["nick"] = histkey
				self.plotted_histograms[histkey] =copy.deepcopy( x)
			else:
				histkey = self.HistClass.nick
				histdict["nick"] = histkey
				self.plotted_histograms[histkey] = copy.deepcopy( x)

			#self.PaveText.AddText("%s #mu = %.2f"%(histdict["name"], x.GetMean()))
			#self.PaveText.AddText("%s #sigma = %.2f"%( histdict["name"], x.GetRMS()))

			self.histogramm_dicts[histkey] =copy.deepcopy( histdict)

	#THE Idea is that you have two inputs for the plot,
	#the first histdictslist is a list of dictionaries for each of histogram, these are set for each hist separate and contain things as the name and the linestyle
	#The second plottingdict is a dictionary which is the same for each histogramm in the plot, think of things like xbins, xmin and xmax and the variable, TODO cut
	def create_plot(self,dictionary):
		self.plotnumber += 1
		self.histdictslist = dictionary["histdictslist"]
		self.plottingdict = dictionary["plottingdict"]
		self.drawPaveText = False




		#self.update_histdictslist(histdictslist) #updates the dicts in outdictlist, maybe rename but ok for now
		self.set_plotdefaults()
		self.first=True

		#if hasattr(self, "c") == False:
		print "making new canvas"
		if not self.outputfile in self.saved_files: # this doesnt work correct
			self.c=ROOT.TCanvas("c{}".format(self.plotnumber),"test{}".format(self.plotnumber),self.canvas_size_x,self.canvas_size_y)

		### TODO: do something with pads?

		#create a dict where the histograms are stored

		if "legend" in self.plottingdict.keys():
			self.set_legend(self.plottingdict["legend"])
		self.create_legend()

		self.maximaly = 0

		self.stacks = {}
		self.histogramm_dicts = {}
		self.plotted_histograms={}
		self.plotted_functions = {}
		#self.PaveText = self.df_style.CreatePavetext()


		for q, histdict in enumerate(self.histdictslist):
			self.create_histlist(q, histdict)

			if histdict.get("fit", None) !=None:
				## TODO: more functions can be added
				if histdict["fit"]["type"] == "double_gaussian":
					func, func1, func2 = self.HistClass.fit_double_gaussian(self.plotted_histograms[histdict["nick"]])
					self.plot_double_gaussians(func,func1,func2)
				elif histdict["fit"]["type"]=="gaussian":
					func = self.HistClass.fit_gaussian(self.plotted_histograms[histdict["nick"]], self.HistClass.xmin, self.HistClass.xmax)
					self.plot_gaussians(func)


					#plotdict["plotted_functions"] = copy.deepcopy(self.plotted_functions)




			##################################
			#TODO preprocess function for a
			#self.calculate_assymetrie(x,self.args.xmid)

		#self.c.SetLogy()

		#make a plotting order?
		if len(self.stacks.keys())>0:
			self.draw_stacks()
		if len(self.plotted_histograms.keys())>0:
			self.draw_histograms()
		if len(self.plotted_functions.keys())>0:
			self.draw_functions()

		self.c.Update()
		if self.show_legend:
			self.legend.Draw()
		if self.drawPaveText:
			self.PaveText.Draw()

		self.c.Update()

	def save_plot(self, dictionary):
		self.c.SaveAs(self.outputfile)
		self.c.Close()
		self.dump_json(dictionary)

	def save_plot_1pdf(self):
		print "saved files:\n\t", self.saved_files
		print "file name: \t", self.outputfile
		if self.outputfile not in self.saved_files:
			print "opening file", self.outputfile
			self.c.Print(self.outputfile+"[")
			self.saved_files.append(self.outputfile)

		print "TITLE:\t", "plot"+str(self.plotnumber)
		self.c.Print(self.outputfile, "Title:plot"+str(self.plotnumber))#, "Title:"+str(self.plotnumber)


	def create_saved_plot(self,dictionary):
		self.create_plot(dictionary)
		self.save_plot(dictionary)


	def plot_double_gaussians(self, func, func1,func2):
		func1.SetLineColor(2)
		func2.SetLineColor(3)

		self.plotted_functions["fit"] = func
		self.plotted_functions["fit1"] = func1
		self.plotted_functions["fit2"] = func2

		self.PaveText = self.df_style.CreatePavetext()

		self.PaveText.AddText("#mu_{1} = %.2f"%( func.GetParameter(0)))
		(self.PaveText.GetListOfLines().Last()).SetTextColor(2)
		self.PaveText.AddText("#sigma_{1} = %.2f"%( func.GetParameter(1)))
		(self.PaveText.GetListOfLines().Last()).SetTextColor(2)

		self.PaveText.AddText("N_{1} = %.2f"%( func.GetParameter(2)))
		(self.PaveText.GetListOfLines().Last()).SetTextColor(2)

		self.PaveText.AddText("#mu_{2} = %.2f"%( func.GetParameter(3)))
		(self.PaveText.GetListOfLines().Last()).SetTextColor(3)

		self.PaveText.AddText("#sigma_{2} = %.2f"%( func.GetParameter(4)))
		(self.PaveText.GetListOfLines().Last()).SetTextColor(3)

		self.PaveText.AddText("N_{2} = %.2f"%( func.GetParameter(5)))
		(self.PaveText.GetListOfLines().Last()).SetTextColor(3)
		self.drawPaveText = True

	def plot_gaussians(self, func):
		print "plotting gaussians"
		self.plotted_functions["fit"] = func

		self.PaveText = self.df_style.CreatePavetext()

		self.PaveText.AddText("#mu = %.2f"%( func.GetParameter(1)))
		self.PaveText.AddText("#sigma = %.2f"%( func.GetParameter(2)))
		self.PaveText.AddText("N = %.2f"%( func.GetParameter(0)))

		self.drawPaveText = True

	def draw_stacks(self):
		for key in self.stacks.keys():
			if self.first:
				self.stacks[key].Draw("HIST") #make this not hardcode
				self.self.first = False
			else:
				self.stacks[key].Draw("HIST same") #make this not hardcoded

	def draw_histograms(self):
		for key in self.plotted_histograms.keys():
			print "markerstyle", self.histogramm_dicts[key]["markerstyle"]

			if self.plottingdict["ymax"]==None:
				self.plotted_histograms[key].SetAxisRange(self.plottingdict["ymin"], (1.1*self.maximaly),"Y");

			if self.first:
				self.first= False
				self.plotted_histograms[key].Draw(self.histogramm_dicts[key]["markerstyle"])
			else:
				self.plotted_histograms[key].Draw(self.histogramm_dicts[key]["markerstyle"]+"same")

			if self.show_legend:
				self.add_legend_entry(self.histogramm_dicts[key])

	def draw_functions(self):
		for key in self.plotted_functions.keys():
			if self.first:
				self.first= False
				self.plotted_functions[key].Draw()
			else:
				self.plotted_functions[key].Draw("same")

			#self.add_legend_entry("fit")




	def create_legend(self):
		self.legend = ROOT.TLegend(self.legend_lowerx, self.legend_lowery,self.legend_upperx,self.legend_uppery)
		self.legend.SetTextSize(0.03)
		self.legend.SetFillColor(0)
		self.legend.SetLineColor(0)
		self.legend.SetBorderSize(0);

	def set_legend(self,_legend):
		self.show_legend = True
		self.legend_lowerx = _legend[0]
		self.legend_lowery = _legend[1]
		self.legend_upperx = _legend[2]
		self.legend_uppery = _legend[3]


	def add_legend_entry(self, plotdict=None):
		if plotdict !=None:

			if "legend_names" in plotdict.keys():
				print "adding legend"

				legendname = plotdict["legend_name"]
			#elif len(self.args.legend_names)>0:
			#	legendname =  self.args.legend_names.pop(0) #give back the first element and removes it from the list
			else:
				print "adding legend names"
				legendname = plotdict["name"]
				print legendname
			self.legend.AddEntry(plotdict["nick"], legendname , "l")

	def create_multiplots(self, plotlist):
		#self.create_histdict()
		for dicts in plotlist:
			#create an option to multithread with multiprocessing
			if self.bsub:
				pass
			else:
				self.create_saved_plot(dicts)

			#create an option to bsub, this would be cool to have ;)
			#idea is to save a json file and do bsub python -j json_file queue short

	def dump_json(self, _dict): #dumps the dictionary used for the plot
		with open(self.json_name, 'w') as _jfile:
			json.dump(_dict , _jfile, indent=4) #

	def read_json(self, _json_name):
			with open(_json_name) as _jfile:
				_dict = json.load(_jfile)
				return _dict

	def calculate_assymetrie(self, hist, xmid):
		bin_xmid  = hist.GetXaxis().FindBin(xmid)
		integral1 = hist.Integral(1,bin_xmid)
		integral2 = hist.Integral(bin_xmid, self.xbins)

		Assymetrie = (integral1-integral2)/(integral1+integral2)
		print "Assymetry for ", self.nick, ":\t", Assymetrie


	#TODO proper implementation of argparser

	#TODO need to think on how to implement it.
	#def get_input_files(self):
	#	for input_file in self.args.files:


	#def prepare_list_args(self, keys_of_list_args, n_items=None, help=""):
	#	"""
	#	Prepare list-type entries in plotData. All values for given keys are casted into lists
	#	and then the lists are filled up by repeating existing items until all lists have the same size.
	#	"""
	#	# prepare lists
	#	for key in keys_of_list_args:
	#		if not isinstance(self.histdict[key], list) or isinstance(self.histdict, basestring):
	#			self.histdict[key] = [self.histdict[key]]

	#	# change "None" in input to None
	#	for key in keys_of_list_args:
	#		for index, item in enumerate(self.histdict[key]):
	#			if(item == "None"):
	#				self.histdict[key][index] = None

	#	max_n_inputs = n_items if n_items != None else max([len(self.histdict[key]) for key in keys_of_list_args])
	#	print max_n_inputs

	#	# expand/cut lists that are too short/long
	#	for key, plot_list in [(key, self.histdict[key]) for key in keys_of_list_args]:
	#		self.histdict[key] = (plot_list * max_n_inputs)[:max_n_inputs]

	@staticmethod
	def prepare_list_args(dictionary,keys_of_list_args, n_items=None, help=""):
		"""
		Prepare list-type entries in plotData. All values for given keys are casted into lists
		and then the lists are filled up by repeating existing items until all lists have the same size.
		"""
		# prepare lists
		for key in keys_of_list_args:
			if not isinstance(dictionary[key], list) or isinstance(dictionary, basestring):
				dictionary[key] = [dictionary[key]]

		# change "None" in input to None
		for key in keys_of_list_args:
			for index, item in enumerate(dictionary[key]):
				if(item == "None"):
					dictionary[key][index] = None

		max_n_inputs = n_items if n_items != None else max([len(dictionary[key]) for key in keys_of_list_args])

		# expand/cut lists that are too short/long
		for key, plot_list in [(key, dictionary[key]) for key in keys_of_list_args]:
			dictionary[key] = (plot_list * max_n_inputs)[:max_n_inputs]

		return dictionary

	@staticmethod
	def create_histdict(_args): #Lets find out why I did this again, I think it is to have a standard parsing of arguments
		histdict = {}
		histdict["input_files"] = _args.input_files

		histdict["folders"] = _args.folders

		#TODO can be simplified by function?
		if len(_args.markers)>0: #check if not empty
			histdict["markers"] = _args.markers
		else:
			histdict["markers"] = ["HIST"]

		if len(_args.colors)>0:
			histdict["colors"] = _args.colors
		else:
			histdict["colors"] = range(len(histdict["input_files"]))

		if len(_args.nicks)>0:
			histdict["nicks"] = _args.nicks
		else:
			histdict["nicks"] = ["nick_" + str(p) for p in range(len(histdict["input_files"]))]

		return histdict


		#self.prepare_list_args(["colors","markers","input_files", "folders"])

		#pprint(histdict)


		#self.outdictlist = [] #TODO rename
		#for nick in histdict["nicks"]:
		#	self.outdictlist.append({})

		#for key in histdict.keys():
		#	for k,l in enumerate(histdict[key]):
		#		self.outdictlist[k][key[:-1]] = l


	@staticmethod
	def argparser():
		parser = argparse.ArgumentParser(add_help=False)
		#parser.add_argument("-h", "--help", default=False, action="store_true",
		#                help="Show this help message and exit.")
		parser.add_argument("-x", "--x-expressions",default=[], nargs="+",
		                help="X variables")
		parser.add_argument("-y", "--y-expressions",default=[], nargs="+",
		                help="Y variables")
		parser.add_argument("-i", "--input-files",default=[], nargs="+",
		                help="input files")
		parser.add_argument("--folders",default="Event;1", type=str,
		                help="input folder")
		parser.add_argument("--legend" , default=[], nargs='+', type=float,
						help="the borders of the legend")
		parser.add_argument("--legend-names" , default=[], nargs='+', type=str,
						help="the name of the legend entries")
		parser.add_argument("-m", "--markers" , default=[], nargs='+', type=str,
						help="the marker style for each of the histogramms")
		parser.add_argument("-w", "--weights", default=["(1)"], nargs='+', type =str,
						help= "weights of the plotted histogram")
		parser.add_argument("-c", "--colors" , default=[], nargs='+', type=str,
						help="the linecolors for each of the histogramm")
		parser.add_argument("--nicks" , default=[], nargs='+', type=str,
						help="the nicks for each of the histogramm")
		parser.add_argument("--names" , default=[], nargs='+', type=str,
						help="the names for each of the histogramm")
		parser.add_argument("--x-bins", default=None, type=str,
						help="the binning in x, \'nbins,bin_min,bin_max\'")
		parser.add_argument("-j", "--json", default = "None", type=str,
						help= "input json that can be used to make a plot")
		parser.add_argument("--filename", default = "None", type=str,
						help= "filename of the output file")
		return parser

	#@staticmethod
	#def create_args(self, parser):
	#	self.args = vars(parser.parse_args())
