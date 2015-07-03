# swantools

This repository gathers some useful functions and tools to be used alongside SWAN wave model.

For downloading, installing  and using SWAN, please see: http://swanmodel.sourceforge.net/

To install the module, fork or download the source code and run:

```bash
sudo setup.py install
```

There are several dependencies that have to be met in order to use all funcions. The major ones are

 - Numpy
 - Pandas
 - NetCDF4
 - Matplotlib
 - Scipy.io

Nowadays, there is a I/O class which can handle TABLE, SPECOUT and BLOCK outputs and write SPECOUT and TPAR files.

For example, to use the I/O structure for reading a TABLE made HEAD option do:

```python

import swantools.io

R   = swantools.io.SwanIO()
df  = R.read_swantable('file.txt')
```
This will return a pandas DataFrame with the model data.

For quickly plotting the results, just do:

```python
import swantools.plot
import seaborn as sns

P = swantools.plot.SwanPlot()

y = df["Hsig"]
x = df.index.values

P.timeseries(x,y,"Significant Wave Heights")
```

Reading spectral files (.spc) wrote with "SPECOUT SPEC2D" become very easy:

```python
import swantools.io

R = swantools.io.SwanIO()

lon,lat,freqs,dirs,times,factors,spec = R.read_swanspc('file.spc')
```

Plotting this data is also easy:

```python
import swantools.plot

P = swantools.plot.SwanPlot()

P.spcplot(freqs,dirs,spectra)
```

Block (.mat) files can be handled in both stationay and non-stationary versions. For extracting variables from this files, one can do:

```python
import swantools.io

R = swantools.io.SwanIO()
lon,lat,times,hs = R.read_swanblock('block.mat','Hsig')
```

Plotting field data can be done whith swantools.plot or creating a netCDF file and using ncview:


```python
import swantools.plot
P    = swantools.plot.SwanPlot()
P.blockplot(lon,lat,hs[0,:,:],"Non-stationary Results")
```

or,

```python
W = swantools.io.Converters()
W.np2nc("Hsig.nc",lat,lon,times,hs,"Significant Wave Height")
subprocess.call(ncview Hsig.nc,shell=True)
```

Non-stationary two-dimensional spectral files (SPEC2D) can be saved as netCDF:

```python
R = swantools.io.SwanIO()
W = swantools.io.Converters()
lon,lat,freqs,dirs,times,factors,spectrum = R.read_swanspc('spectrum.spc')
W.spc2nc("spectrum.nc",lat,lon,freqs,dirs,times,factors,spectrum)
```

Non-stationary two-dimensional spectral files (SPEC2D) can be written as well:

```python
# Getting some data to play with
R = swantools.io.SwanIO()
lat,lon,freqs,dirs,times,factors,spectrum = R.read_swanspc('spectrum.spc')
# Re-writing the data
R.write_spectrum("spcout.spc",lat,lon,times,freqs,dirs,factors,spectrum)
```



Much more will be added in the future.

Enjoy !
