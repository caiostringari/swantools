import numpy as np
import pylab
import matplotlib.pyplot as plt


class SwanPlot:

	def __init__(self):
		pass

	def spcplot(self,freqs,dirs,time,spectra,**kw):
		""" Simple spectral plot """
		# Spectral space
		D,F = np.meshgrid(    np.linspace(0,360,len(dirs)),
		                      np.linspace(0,0.5,len(freqs)))
		# Or use the original
		# D,F   = np.meshgrid(dirs,freqs)
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
		fig,ax = plt.subplots(figsize=(6,6),subplot_kw=dict(projection='polar'))
		circle = plt.Circle((0,0),.03,color='gray',transform=ax.transData._b)
		# Corrects referential
		ax.set_theta_zero_location("N")
		ax.set_theta_direction(-1)
		# Draw the plot
		spc = ax.contourf(theta,F,nspectra,cmap=cmap,levels=lims)
		# Draw Grid
		ax.grid(True,color="w")
		# Draw the circle
		ax.add_artist(circle)
		# Adjust Colorbar
		# cb=plt.colorbar(spc,ax=ax,ticks=tks,orientation='horizontal',shrink=0.65,
	                            #  extend='both',norm=norm)
		# cb.set_clim(0,1)
		# cb.set_label(r'$Normalized$ $Variance$ $Density$ $(m^{-2}.s^{-1}.deg^{-1})$')
		# Mask labels to show periods instead of frequencies
		ax.set_yticklabels(map(str,[20.0,10.0,6.6,5.0]))
		# Mask xlabels
		ax.set_xticklabels(['N','NE','E','SE','S','SW','W','NW'])
		ax.tick_params(axis='y',colors='w')
		#
		plt.figtext(.1,.95,time.strftime("%Y%m%d - %H:%M"),fontsize=14, ha='left',)
		# show
		plt.show()

	def blockplot(self,x,y,z,title):
		plt.figure()
		cmap = pylab.cm.jet
		vmin = np.nanmin(z)
		vmax = np.nanmax(z)
		plt.pcolormesh(x,y,z,cmap=cmap,vmin=vmin,vmax=vmax)
		plt.colorbar()
		plt.title(title)
		plt.xlim([x.min(),x.max()])
		plt.ylim([y.min(),y.max()])
		plt.grid()
		plt.show()

	def timeseries(self,x,y,var,**kw):
	    plt.figure(figsize=(12,4))
	    plt.plot(x,y,"-r",label=var)
	    plt.legend()
	    plt.show()
