# swantools

This repository gathers some useful functions and tools to be used alongside SWAN wave model.

For downloading, installing  and using SWAN, please see: http://swanmodel.sourceforge.net/

To easily install the module just do:

```bash
sudo pip install swantools
```

alternatively, download the source code and install with:

```bash
sudo setup.py install
```

Nowadays, there is a I/O class which can handle TABLE, SPECOUT and BLOCK outputs. In the future, it will be possible to write spectral boundary conditions, TPAR files and initial conditions.

For example, to use the I/O structure for reading a TABLE with HEAD option do:

```python

import swantools

rw = swantools.SwanIO()

table = rw.read_swantable('file.txt')
```
This will return a pandas DataFrame with the model data.

Reading spectral (.spc) files become very easy:

```python

lon,lat,nfreqs,freqs,ndirs,dirs,spectra = rw.read_swanspc('file.txt','19990101.00000')
```

Some useful functions are also provided, for example:

```python

lat    = np.arange(-40,-10,0.25)
lon    = np.arange(-60,-40,0.25)
plats  = np.array([-15.65,-25.25,-12.45])
plons  = np.array([-35.20,-55.27,-30.10])

indx,dists = nearest_point(lon,lat,plons,plats)
```

Much more will be added in the future.

Enjoy !
