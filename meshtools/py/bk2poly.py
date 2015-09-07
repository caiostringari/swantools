import subprocess,sys
import shapefile
import numpy as np
import matplotlib.pyplot as plt

fc='../lines/Coastline_SP_500.i2s'
fs='../lines/Oceanline_South.i2s'
fe='../lines/Oceanline_East.i2s'
fn='../lines/Oceanline_North.i2s'

coastline = np.genfromtxt(fc,skip_header=18,delimiter=" ")
southline = np.genfromtxt(fs,skip_header=18,delimiter=" ")
eastline  = np.genfromtxt(fe,skip_header=18,delimiter=" ")
northline = np.genfromtxt(fn,skip_header=18,delimiter=" ")


print "Processing Shorelines ..."
# Coastline points
xc = coastline[1:,0]         # longitude
yc = coastline[1:,1]         # latitide
fc = np.ones(len(xc))*1      # flag

# Ocean
xn = northline[:,0]          # longitude
yn = northline[:,1]          # latitude
fn = np.ones(len(xn))*2      # flag

xe = eastline[:,0]           # longitude
ye = eastline[:,1]           # latitude
fe = np.ones(len(xe))*2      # flag

xs = southline[:,0]          # longitude
ys = southline[:,1]          # latitude
fs = np.ones(len(xs))*2      # flag

# Reversing
# xc = xc[::-1]
# yc = yc[::-1]
# xn = xn[::-1]
# yn = yn[::-1]
# xe = xe[::-1]
# ye = ye[::-1]
# xs = xs[::-1]
# ys = ys[::-1]


# plt.figure(1)
# plt.plot(xc[0:],yc[0:],"-k",label="2 (Land)")
# plt.plot(xn[0:],yn[0:],"-b",label="1 (Ocean - North)")
# plt.plot(xe[0:],ye[0:],"-g",label="1 (Ocean - East)")
# plt.plot(xs[0:],ys[0:],"-y",label="1 (Ocean - South)")
# plt.grid()
# plt.axis('equal')
# plt.legend(loc="best")
# plt.show()

# .poly file

# Order : South -> East -> North -> Coastline

p = open("mesh.poly","w")

# Total number of points
pt = len(xc)+len(xs)+len(xe)+len(xn)

p.write("{} {} {} {} \n".format(pt,2,0,0))

k=1

X = []
Y = []
F = []

# South
for x,y in zip(xs,ys):
    p.write("{} {} {} \n".format(k,x,y))
    X.append(x)
    Y.append(y)
    F.append(1)
    k+=1

# East
for x,y in zip(xe,ye):
    p.write("{} {} {} \n".format(k,x,y))
    X.append(x)
    Y.append(y)
    F.append(1)
    k+=1

# North
for x,y in zip(xn,yn):
    p.write("{} {} {} \n".format(k,x,y))
    X.append(x)
    Y.append(y)
    F.append(1)
    k+=1

# Coastline
for x,y in zip(xc,yc):
    p.write("{} {} {} \n".format(k,x,y))
    X.append(x)
    Y.append(y)
    F.append(2)
    k+=1


p.write("{} {} \n".format(pt,1))

k=1
for f in F:
    p.write("{} {} {} {} \n".format(k,k,k+1,int(f)))
    k+=1
    if k == len(F):
        p.write("{} {} {} {} \n".format(len(F),len(F),1,2))
        break


print "Processing Isles ..."
# Islands
# nisles = 0
# p.write("{} \n".format(nisles))
#
sf     = shapefile.Reader("../lines/Islands_SP_200.shp")
shapes = sf.shapes()

xi = []                      # longitude
yi = []                      # latitude
fi = []                      # flag

nisles = 0
for shape in shapes:
    nisles+=1
p.write("{} \n".format(nisles))

isle = 1
for shape in shapes:
    # print "  Isle {}".format(isle)
    coordinates = shape.points
    xt=[]
    yt=[]
    for x,y in coordinates:
        p.write("{} {} {} \n".format(isle,x,y))
        xt.append(x)
        yt.append(y)
    xi.append(xt)
    yi.append(yt)
    isle+=1

# # Checking
subprocess.call("triangle -cupa0.02 mesh.poly",shell="True")
subprocess.call("./showme mesh.1",shell="True")
#
# Plot
# print "Plotting ..."
# plt.figure(1)
# plt.plot(xc,yc,"-k",label="2 (Land)")
# plt.plot(xo,yo,"-b",label="1 (Ocean)")
# for I in zip(xi,yi):
#     plt.plot(I[0],I[1],"-k")
# plt.grid()
# plt.axis('equal')
# plt.legend(loc="best")
# plt.show()
#
