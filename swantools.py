#!/usr/bin/python
#
#
#------------------------------------------------------------------------
#------------------------------------------------------------------------
#
#
# SMODULE  : broou.tools
# POURPOSE : Gathers functions used by other scripts
# AUTHOR   : Caio Eadi Stringari
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
import operator
import datetime
import numpy  as np
import pandas as pd

from matplotlib.dates import num2date,date2num 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#

class SwanIO:

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
		
		dates=[]
		f = open(fname,'r').readlines()
	
		if headers:
			# Handle times
			for line in f: dates.append(line.split()[0])
			times        = swantime2datetime(dates)
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
			times        = swantime2datetime(dates)
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

		# Check dates. Only one value can be used for now.

		if np.shape(swantime) >= 1:
			print "Only single date retrives can be handle"
			# sys.exit()

		f = open(fname,'r').readlines()

		
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
				print start, end
				LINES=[]
				for i,lines in enumerate(f):
					if i >= start and i <= end:
						LINE  = lines.split()
						LINES.append(LINE)
				VALUES=[]
				for block in LINES:
					for strs in block:
						VALUES.append(float(strs))
				Ssectrum=np.reshape(VALUES,(nfreqs,ndirs))*factor
				# print factor
				# print l


				# freqs  = l[line+2:line+nfreqs+1]
				# print start,end






		# pass


# Utils

def find_nearest(target,val):

	""" Given a numpy vector, this function will find the nearest given index and value
	    in the given target.
	"""
	
	difs                 = abs(target-val)
	min_idx, min_val     = min(enumerate(difs), key=operator.itemgetter(1))
	out                  = target[min_idx]
	return min_idx, out
			
def swantime2datetime(time,inverse=False):
	
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





	
if __name__ == "__main__":

	# Reading data

	reader = SwanIO()
	headers = ["TIME","HSIGN","HSWELL","PDIR","DIR","TPS","PER","WINDX","WINDY","PROPAGAT"]
	table1  = reader.read_swantable('Boia_Minuano_1998.txt',headers=headers)
	table2  = reader.read_swantable('Boia_Minuano_H_1998.txt')

	t = swantime2datetime([729390,],inverse=True)

	spc = reader.read_swanspc('Boia_Minuano_1998.spc',t)




	# Utils	
	t = np.array([1,2,3,4,5,6,7,8,9])
	v = 5.6
	idx,vt = find_nearest(t,v)
#	print idx,vt



