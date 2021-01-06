
#!/usr/bin/env python
# -*- coding: utf-8 -*-


#Make this the default one and move special variables to another class inhereting from this.
#This file for example pt/eta/phi lepton.
#Special class top: Top pt, mass...
#Special class Higgs: Higgs pt, mass...
class Plotdefaults(dict):
	def __init__(self, var):
		self.set_var(var)

	def set_var(self, var):
		#Do this smarter?
		var =var.lower() #make it lower case such that it is case insensitive
		if var in ["costheta_xl"]: #TODO maybe add aliases something like self.costheta_xl = ["costheta_xl", "costhetaxl"]
			self.var_costheta_xl()
		elif var in ["costheta_ql"]: #TODO maybe add aliases
			self.var_costheta_ql()
		elif var in ["xl_pol"]: #TODO maybe add aliases
			self.var_xl_pol()
		elif var in ["xl_pol_tcm"]: #TODO maybe add aliases
			self.var_xl_pol_tcm()
		elif var in ["u_pol"]: #TODO maybe add aliases
			self.var_u_pol()
		elif var in ["z_pol"]: #TODO maybe add aliases
			self.var_z_pol()

		else:
			print "COULD NOT FIND VARIABLE IN STANDARD VARIABLES"
			print "setting the following variables:"
			print "self[xmin]=0, self[xmax]=1, self[ymin]=0, self[ymax]=1, self[xbins] =16"
			self.defaults(var)

	def defaults(self, var):
		self["xmin"]=0
		self["xmax"]=6
		self["ymin"]=0
		self["ymax"]=1
		self["xbins"] =16
		self["var"] = var
		self["filename"] = var

	def var_costheta_xl(self):
		self["filename"]="costheta_xl"
		self["var"]="Event.CosTheta_xl"
		self["xmin"]=-1
		self["xmax"]=1
		self["ymin"]=0.
		self["ymax"]=1
		self["xbins"] =6

	def var_costheta_ql(self):
		self["filename"]="costheta_ql"
		self["var"]="Event.CosTheta_ql"
		self["xmin"]=-1
		self["xmax"]=1
		self["ymin"]=0
		self["ymax"]=0.3
		self["xbins"] =6

	def var_xl_pol(self):
		self["filename"]="xl_pol"
		self["var"]="Event.xl_pol"
		self["xmin"]=0
		self["xmax"]=5
		self["ymin"]=0
		self["ymax"]=0.4
		self["xbins"] =6
	def var_xl_pol_tcm(self):
		self["filename"]="xl_pol_tcm"
		self["var"]="Event.xl_pol_tcm"
		self["xmin"]=0
		self["xmax"]=1
		self["ymin"]=0
		self["ymax"]=0.4
		self["xbins"] =6
	def var_u_pol(self):
		self["filename"]="u_pol"
		self["var"]="reco_u_pol_tag"
		self["xmin"]=0
		self["xmax"]=1
		self["ymin"]=0
		self["ymax"]=0.4
		self["xbins"] =6
	def var_z_pol(self):
		self["filename"]="z_pol"
		self["var"]="reco_z_pol_tag"
		self["xmin"]=0
		self["xmax"]=1
		self["ymin"]=0
		#self["ymax"]=0.4
		self["xbins"] =6
