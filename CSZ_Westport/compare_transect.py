from pylab import *
from clawpack.pyclaw import Solution

from clawpack.visclaw import gridtools, legend_tools
from clawpack.geoclaw.util import haversine, gctransect
from clawpack.geoclaw.data import Rearth
import mapper

from clawpack.clawutil.util import fullpath_import
setplot_module = fullpath_import('1d_radial/setplot.py')

outdir = '2d_test1/_output_6levels'
format = 'binary'

if 0:
    frameno = 10
    frameno1d = 47
if 1:
    frameno = 8
    frameno1d = 45

tmin = 45
frameno1d = tmin
frameno = tmin - 37

#frameno = 13
#frameno1d = 37+frameno

framesoln = Solution(frameno, path=outdir, file_format=format)
print('Frame %i at time %g' % (frameno, framesoln.t))

figure(301,figsize=(8,5))
clf()

x0 = 50.
y0 = 40.
d1 = 2500e3
d2 = 2525e3
theta0 = 210.
dtheta = 0.02

#for theta in linspace(theta0-dtheta, theta0+dtheta, 9):
for theta in [theta0]:
    xhat1, yhat1 = mapper.latlong(d1,theta,y0,Rearth)
    xhat1 += x0
    xhat2, yhat2 = mapper.latlong(d2,theta,y0,Rearth)
    xhat2 += x0

    xtrans, ytrans = gctransect(xhat1,yhat1, xhat2, yhat2, 1000, coords='E')
    d = haversine(xtrans, ytrans, x0, y0)
    h = gridtools.grid_output_2d(framesoln, 0, xtrans, ytrans)
    eta = gridtools.grid_output_2d(framesoln, 3, xtrans, ytrans)
    B = eta - h

    plot(d/1e3,eta,'b')
    plot(d/1e3,B,'g')

xlim(2517,2521)
ylim(-20,20)
grid(True)

outdir1d = '1d_radial/_output_5mG_10m/'
#framesoln = Solution(47, path=outdir1d, file_format='ascii')

plotdata = setplot_module.setplot()
plotdata.outdir = outdir1d
plotdata.printfigs = False
plotdata.print_fignos = [1]
plotdata.plotframe(frameno1d)

#subplot(211)
theta = 210.
xhat1, yhat1 = mapper.latlong(d1,theta,y0,Rearth)
xhat1 += x0
xhat2, yhat2 = mapper.latlong(d2,theta,y0,Rearth)
xhat2 += x0

xtrans, ytrans = gctransect(xhat1,yhat1, xhat2, yhat2, 1000, coords='E')
if 0:
    transdata = vstack((xtrans,ytrans)).T
    fname ='xy_transect.txt' 
    savetxt(fname, transdata)
    print('Created ',fname)
d = haversine(xtrans, ytrans, x0, y0)
method = 'linear'
h = gridtools.grid_output_2d(framesoln, 0, xtrans, ytrans, method=method)
eta = gridtools.grid_output_2d(framesoln, 3, xtrans, ytrans, method=method)
B = eta - h

plot(d/1e3,eta,'r')
plot(d/1e3,B,'c')

if 0:
    hu = gridtools.grid_output_2d(framesoln, 1, xtrans, ytrans)
    hv = gridtools.grid_output_2d(framesoln, 2, xtrans, ytrans)
    u = divide(hu, h, where=h>0.001, out=zeros(h.shape))
    v = divide(hv, h, where=h>0.001, out=zeros(h.shape))
    s = sqrt(u**2 + v**2)
    subplot(212)
    plot(d/1e3,u,'r')

labels = ['1D with 10 m resolution',
          '2D with 1/3" resolution',
          '1D topography',
          '2D topography on transect']

legend_tools.add_legend(labels, colors=['b','r','g','c'],
                        loc='upper left', framealpha=1)

fname = f'2Dtransect_{tmin}min.png'
savefig(fname, bbox_inches='tight')
print('Created ',fname)
