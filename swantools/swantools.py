#!/usr/bin/python

__version__ = '0.1'
__author__  = 'Caio Stringari'
__mail__    = 'caio.stringari@gmail.com'
__license__ = 'GPL2'

#
#
# V 0.1    : 15/04/2015
#
#------------------------------------------------------------------------
#------------------------------------------------------------------------
#
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Global Imports
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


import sys,os
import os.path
import operator
import datetime
import pylab
import math

import scipy.io
import scipy.spatial

import numpy  as np
import pandas as pd
import matplotlib.pyplot as plt


from matplotlib.dates import num2date,date2num 

#
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#

class SwanIO:

	def __init__(self):
		pass

	def iocheck(self,fname):
		io = os.path.isfile(fname)
		if io:
			pass
		else:
			raise IOError('File {0} not found.'.format(fname)) 

	def read_swantable(self,fname,headers=[]):

		""" 
		    Use this function to read data generated with the command table.
		    Both NOHEAD and HEAD options can be read here. 

		    If using NOHEAD,
		    the user must specify with variables are being read, for example:

		    reader = SwanIO()
			headers = ["TIME","HSIGN","HSWELL","PDIR","DIR","TPS","PER","WINDX","WINDY","PROPAGAT"]
			table = reader.read_swantable('file.txt',headers=headers)

			If usind HEAD option, just do:

			reader = SwanIO()
			table  = reader.read_swantable('file_with_headers.txt')

			The function will return a pandas DataFrame.
		"""
		
		# I/O check
		self.iocheck(fname)

		f=open(fname,'r').readlines()

		dates=[]
	
		if headers:
			# Handle times
			for line in f: dates.append(line.split()[0])
			times        = SwanUtils.swantime2datetime(dates)
			# Read the table file
			rawdata      = np.genfromtxt(fname)
			rawdata[:,0] = times
			index        = np.arange(0,len(rawdata[:,0]),1)
			df           = pd.DataFrame(rawdata[:,:],index=index,columns=headers)
			return df
		else:
			# Handle times
			for i,line in enumerate(f):
				if i > 6: dates.append(line.split()[0])
			times        = SwanUtils.swantime2datetime(dates)
			# Handle headers
			headers     = [] 
			for i,h in enumerate(f[4].split()):
				if i >0: headers.append(h)
			# Read the table file
			rawdata      = np.genfromtxt(fname,skip_header=7)
			rawdata[:,0] = times
			index        = np.arange(0,len(rawdata[:,0]),1)
			df           = pd.DataFrame(rawdata[:,:],index=index,columns=headers)
			return df


	def read_swanspc(self,fname,swantime):

		""" 
		    Use this function to read data generated with the SPECOUT command.
		    
		    The sixtase MUST be :
		    'SPECOUT 'Location' SPEC2D ABS 'name.spc'

		    Read the documentation in http://swanmodel.sourceforge.net to more details on spectral output.

		    Inputs
		    fname:    the name of the file
		    swantime: a date and time string in swans's format

		    Outputs
		    lon:    longitude of the point
		    lat:    latitude of the point
		    nfreqs: number of frequencies
		    freqs:  list of frequencies
		    ndirs:  number of directions
		    dirs:   list of directions
		    spectra: array with spectral data (frequencies,directions)
		"""

		# I/O check
		self.iocheck(fname)

		f = open(fname,'r').readlines()

		# Time check
		check = False
		for line in f:
			if swantime in line:
				check = True
				break
		if check:
			pass
		else:
			raise ValueError('It seems the date requested is not present in the file.') 
		
		for l,line in enumerate(f):

			# Heading the headers
			if "TIME" in line:
				time = f[l+1].split()[0]
			elif "LONLAT" in line:
				lon = float(f[l+2].split()[0])
				lat = float(f[l+2].split()[1])
			elif "AFREQ" in line:
				nfreqs = int(f[l+1].split()[0])
				start  = l+2
				end    = l+nfreqs+1
				freqs  = []
				for i,l in enumerate(f):
					if i >= start and i <= end:
						fq = l.split()[0]
						freqs.append(float(fq))
			elif "NDIR" in line:
				ndirs = int(f[l+1].split()[0])
				start  = l+2
				end    = l+ndirs+1
				dirs  = []
				for i,l in enumerate(f):
					if i >= start and i <= end:
						ds = l.split()[0]
						dirs.append(float(ds))

			# Read the spectrum for a given date
			elif swantime in line:
				factor = float(f[l+2])
				start  = l+3
				end    = l+nfreqs+2
				LINES=[]
				for i,lines in enumerate(f):
					if i >= start and i <= end:
						LINE  = lines.split()
						LINES.append(LINE)
				VALUES=[]
				for block in LINES:
					for strs in block:
						VALUES.append(float(strs))
				spectra=np.reshape(VALUES,(nfreqs,ndirs))*factor

		return lon,lat,nfreqs,freqs,ndirs,dirs,spectra

	def read_swanblock(self,fname,basename,time=False,stat=False):

		"""
			Function to read SWAN's BLOCK output statment. Both stationary
			and non-stationary versions can be handled there. If requesting
			a non-stationary output a proper date string shoudl be given.
			In case of non-stationary data with no dates, such as XP or YP,
			just call the function as if it were stationary.
			will return a numpy array with [Xp,Yp] dimension.
		"""

		# Reading ths data causes to some useless warnigs to be printed,
		# removing it using "brute-force"
		import warnings
		warnings.filterwarnings("ignore")

		# I/O check
		self.iocheck(fname)

		block = scipy.io.loadmat(fname)
		keys  = block.keys()

		if stat:
			var = basename
			z   = scipy.io.loadmat(fname)[var]
			return z

		else:

			if time:
				
				var = basename+"_"+time.replace('.','_')+"00"

				for k in keys:
					if var in keys:
						z   = scipy.io.loadmat(fname)[var]
						return z
						break
					else:
						raise ValueError('It seems the variable requested is \
						                  not present in the file.')
			else:

				var = basename

				for k in keys:
					if var in keys:
						z   = scipy.io.loadmat(fname)[var]
						return z
						break
					else:
						raise ValueError('It seems the variable requested is \
							              not present in the file.')


class SwanPlots:

	def simple_spectralplot(self,freqs,dirs,spectra):
		""" Simple spectral plot """
		# Spectral space
		# D,F = np.meshgrid(np.linspace(360,0,ndirs),np.linspace(0,0.5,nfreqs)*0.5)
		# Or use the original
		D,F   = np.meshgrid(np.linspace(360,0,len(dirs)),freqs)
		theta = np.radians(D-90)
		#
		# Normalize data
		nspectra=spectra/spectra.max()
		#
		# Set the colormap
		cmap = pylab.cm.get_cmap('jet',20)
		lims = np.linspace(0,1,21,endpoint=True)
		tks  = np.linspace(0,1,11,endpoint=True)
		norm = pylab.mpl.colors.BoundaryNorm(lims,cmap.N)
		# Set the plot
		fig,ax = plt.subplots(subplot_kw=dict(projection='polar'))
		circle = plt.Circle((0,0),.035,color='w',transform=ax.transData._b)
		# Corrects referential
		ax.set_theta_zero_location("N")
		ax.set_theta_direction(-1)
		# Draw the plot 
		spc = ax.contourf(theta,F,nspectra,cmap=cmap,levels=lims)
		# Draw Grid
		ax.grid(True,color='w')
		# Draw the circle
		ax.add_artist(circle)
		# Adjust Colorbar
		cb=plt.colorbar(spc,ax=ax,ticks=tks,orientation='horizontal',shrink=0.65, 
	                             extend='both',norm=norm)
		cb.set_clim(0,1)
		cb.set_label(r'$Normalized$ $Variance$ $Density$ $(m^{-2}.s^{-1}.deg^{-1})$')
		# Mask labels to show periods instead of frequencies
		ax.set_yticklabels(map(str,[20.0,10.0,6.6,5.0]))
		# Mask xlabels
		ax.set_xticklabels(['N','NE','E','SE','S','SW','W','NW'])
		ax.tick_params(axis='y',colors='w')
		#
		# show
		plt.show()

	def simple_blockplot(self,x,y,z,title):
		plt.figure()
		cmap = pylab.cm.jet
		plt.pcolormesh(x,y,z,cmap=cmap,vmin=z.min(),vmax=z.max())
		plt.colorbar()
		plt.title(title)
		plt.xlim([x.min(),x.max()])
		plt.ylim([y.min(),y.max()])
		plt.grid()
		plt.show()


# Swan Utils

class SwanUtils():

	@classmethod
	def swantime2datetime(self,time,inverse=False):
		"""
			Translating Swans's time strings to datetimes and vice-versa.
			See datetime and num2date documentation for more information.
		"""
		
		fmt = "%Y%m%d.%H%M%S"

		dtime = []
		stime = []
		
		if inverse:
			for date in time:
				stime.append(datetime.datetime.strftime(num2date(date),fmt))
				return stime
		else:
			for date in time:
				dtime.append(date2num(datetime.datetime.strptime(date,fmt)))
			return dtime

	@classmethod
	def dir2cat(self,theta):
		""" Given a array of directions, will return the respective
		    categoreis (N,S,E,W, ect..). Credits to Eric Nardi.
		"""
		categories = ['N', 'NNE', 'NE', 'ENE',
		              'E', 'ESE', 'SE', 'SSE',
		              'S', 'SSW', 'SW', 'WSW',
		              'W', 'WNW', 'NW', 'NNW']
		# print theta
		interval = 360.0/len(categories)
		idx      = np.floor((theta+interval/2)%360/interval)
		cat      = []
		for i in idx: cat.append(categories[int(i)])
		return cat


# Package functions

def find_nearest(target,val):

	""" Given a numpy vector, this function will find the nearest given index and value
	    in the given target.
	"""
	
	difs                 = abs(target-val)
	min_idx, min_val     = min(enumerate(difs), key=operator.itemgetter(1))
	out                  = target[min_idx]
	return min_idx, out

def nearest_point(tx,ty,x,y):

	txy = zip(tx,ty)
	xy  = zip(x,y)

	# Using scipy.spatial.cKDTree for the search

	tree          = scipy.spatial.cKDTree(txy)
	dist, indexes = tree.query(xy)

	return dist, indexes


if __name__ == "__main__":

	### Some examples ####

	# Reading data
	from swantools import SwanUtils

	reader  = SwanIO()

	# Reading TABLE dada without headers:
	headers = ["TIME","HSIGN","HSWELL","PDIR","DIR","TPS","PER","WINDX","WINDY","PROPAGAT"]
	table1  = reader.read_swantable('../data/Boia_Minuano_1998.txt',headers=headers)
	
	# Reading TABLE with headers:
	table2  = reader.read_swantable('../data/Boia_Minuano_H_1998.txt')
	
	# Reading spectral data
	t       = SwanUtils.swantime2datetime([729390,],inverse=True)
	lon,lat,nfreqs,freqs,ndirs,dirs,spectra = reader.read_swanspc('../data/Boia_Minuano_1998.spc',t[0])
	
	# Reading a block file - Non stationary example
	hs1 = reader.read_swanblock('../data/nonstat_block.mat','Hsig',time='19980105.0000')
	# Coordinates example
	lon = reader.read_swanblock('../data/nonstat_block.mat','Xp')
	lat = reader.read_swanblock('../data/nonstat_block.mat','Yp')
	dep = reader.read_swanblock('../data/nonstat_block.mat','Botlev')
	# Stationary example
	hs2 = reader.read_swanblock('../data/stat_block.mat','Hsig',stat=True)
	

	# Ploting data
	sp = SwanPlots()
	
	# Plot spectral data
	# sp.simple_spectralplot(freqs,dirs,spectra)

	# Simple block plot
	# sp.simple_blockplot(lon,lat,hs2,'Bottom')

	# Utils
	dirs = np.arange(0, 360, 10)
	cats = SwanUtils.dir2cat(dirs)
	print cats



	lat    = np.arange(-40,-10,0.25)
	lon    = np.arange(-60,-40,0.25)
	plats  = np.array([-15.65,-25.25,-12.45])
	plons  = np.array([-35.20,-55.27,-30.10])

	indx,dists = nearest_point(lon,lat,plons,plats)


	# t = np.array([1,2,3,4,5,6,7,8,9])
	# v = 5.6
	# idx,vt = find_nearest(t,v)
#	print idx,vt



