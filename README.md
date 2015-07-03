# swantools

This repository gathers some useful functions and tools to be used alongside SWAN wave model.

For downloading, installing  and using SWAN, please see: http://swanmodel.sourceforge.net/

To install the module, fork or download the source code and run:

```bash
sudo setup.py install
```

Nowadays, there is a I/O class which can handle TABLE, SPECOUT and BLOCK outputs and write TPAR files.

For example, to use the I/O structure for reading a TABLE with HEAD option do:

```python

import swantools.io

R   = swantools.io.SwanIO()
df  = R.read_swantable('file.txt')
```
This will return a pandas DataFrame with the model data.

For quickly plotting the results, just do:

Using pandas:

```python
df.plot()
```

Using swantools.plot:

```python

import swantools.plot

P = swantools.plot.SwanPlot()

y = df["Hsig"]
x = df.index.values
P.timeseries(x,y,"Significant Wave Heights")
```

Reading spectral (.spc) files become very easy:

```python
import swantools.io

R = swantools.io.SwanIO()

lon,lat,freqs,dirs,spectra = R.read_swanspc('file.txt','19990101.00000')
```

Plotting this data is also very easy:

```python
import swantools.plot

P = swantools.plot.SwanPlot()

P.spcplot(freqs,dirs,spectra)
```

Block (.mat) files can be handled in both stationay and non-stationary versions:

```python
import swantools.io

R = swantools.io.SwanIO()

t    = '19980105.0000'
lon  = R.read_swanblock('data/nonstat_block.mat','Xp')
lat  = R.read_swanblock('data/nonstat_block.mat','Yp')
hs   = R.read_swanblock('data/nonstat_block.mat','Hsig',time=t)
```

```python
import swantools.io

R    = swantools.io.SwanIO()
lon  = R.read_swanblock('data/nonstat_block.mat','Xp')
lat  = R.read_swanblock('data/nonstat_block.mat','Yp')
hs   = R.read_swanblock('data/stat_block.mat','Hsig',stat=True)
```

Much more will be added in the future.

Enjoy !
