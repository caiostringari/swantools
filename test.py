
import swantools.io
import swantools.utils
import swantools.plot


import datetime
import matplotlib.pyplot as plt

import numpy as np

def readtable():
    R = swantools.io.SwanIO()
    P = swantools.plot.SwanPlot()

    # Reading TABLE dada with headers:
    df  = R.read_swantable('data/table.txt')

    y = df["Hsig"]
    x = df.index.values
    P.timeseries(x,y,"Significant Wave Heights")

def readspc():
    # Reading spectral data
    R = swantools.io.SwanIO()
    lat,lon,freqs,dirs,times,factors,spectrum = R.read_swanspc('data/spectrum.spc')
    P = swantools.plot.SwanPlot()
    P.spcplot(freqs,dirs,times[15],spectrum[15,:,:]*factors[15])
    # for t, time in enumerate(times):
    #     P.spcplot(freqs,dirs,times[t],spectrum[t,:,:])

def readblock(mode):
    R    = swantools.io.SwanIO()
    P    = swantools.plot.SwanPlot()

    if  mode == "non-stat":
        # Reading a block file - Non stationary example
        lon,lat,times,hs = R.read_swanblock('data/block.mat','Hsig')
        P.blockplot(lon,lat,hs[0,:,:],"Non-stationary Results")
        # for t, time in enumerate(times):
        #     P.blockplot(lon,lat,hs[t,:,:],time.strftime("%Y%m%d %H:%M"))
    elif mode == "stat":
        # Reading a block file - Non stationary example
        lon,lat,times,hs = R.read_swanblock('data/stat_block.mat','Hsig',stat=True)
        P.blockplot(lon,lat,hs,"Stationary Results")

def writescp():

    # Getting some data to play with
    R = swantools.io.SwanIO()
    lat,lon,freqs,dirs,times,factors,spectrum = R.read_swanspc('data/spectrum.spc')

    # Re-writing the data
    R.write_spectrum("spcout.spc",lat,lon,times,freqs,dirs,factors,spectrum)

    # Plot to confirm
    lat,lon,freqs,dirs,times,factors,spectrum = R.read_swanspc('spcout.spc')
    P = swantools.plot.SwanPlot()
    for t, time in enumerate(times):
        P.spcplot(freqs,dirs,times[t],spectrum[t,:,:])


def netcdf_output():
    R = swantools.io.SwanIO()
    W = swantools.io.Converters()

    lon,lat,times,hs = R.read_swanblock('data/block.mat','Hsig')

    W.np2nc("Hsig.nc",lat,lon,times,hs,"Significant Wave Height")



def spectral_output():
    R = swantools.io.SwanIO()
    W = swantools.io.Converters()

    lon,lat,freqs,dirs,times,factors,spectrum = R.read_swanspc('data/spectrum.spc')

    W.spc2nc("spectrum.nc",lat,lon,freqs,dirs,times,factors,spectrum)


if __name__ == "__main__":

    # # Table data
    # import seaborn as sns
    # with sns.axes_style("darkgrid"):
    #     readtable()

    # Spectral data
    readspc()

    # Field data
    readblock("non-stat")

    # Convertung block to netCDF4
    netcdf_output()

    # Converting spctral file to netCDF4
    spectral_output()

    # Wrinting spctral data
    writescp()
