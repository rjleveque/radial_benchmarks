
"""
Module to create topo and qinit data files for this example.
"""

from clawpack.geoclaw.topotools import Topography
from pylab import *

d = 1  # water depth
H = 0.019*d
#beta = acot(19.85)
slope = 1/19.85
gamma = sqrt(3*H/(4*d))
#L = arccosh(sqrt(20))/gamma
L = 30
x0 = d/slope
x1 = x0 + L
x2 = x0 + 3*L

w = 50. # width of wavetank
alpha = 0.2  # angle of wavetank to grid
sech = lambda x: 2/(exp(x)+exp(-x))

# grid for both topo and qinit files:
dx = 0.2  # target mesh spacing
xlower = -20.
xupper = x2
nx = int(round((xupper - xlower)/dx))
ylower = -35.
yupper = 40.
ny = int(round((yupper - ylower)/dx))

def maketopo():
    """
    Output topography file for the entire domain
    """
    outfile= "wavetank.asc"

    topography = Topography(topo_func=topo)
    topography.x = linspace(xlower,xupper,(nx+1))
    topography.y = linspace(ylower,yupper,(ny+1))
    topography.write(outfile, topo_type=3, header_style='asc',
                     Z_format="%10.3f")
    print('Created ',outfile)


def topo(x,y):
    """
    wave tank at angle alpha to grid
    """
    xhat = cos(alpha)*x + sin(alpha)*y
    yhat = -sin(alpha)*x + cos(alpha)*y

    # piecewise linear function of xhat:
    z = where(xhat > x0, -d, -d+slope*(x0-xhat))

    # add vertical walls along sides:
    z = where(abs(yhat) < w/2, z, 2.)

    return z


def makeqinit():
    """
    Create qinit data file
    """
    outfile= "wave.xyz"

    topography = Topography(topo_func=qinit)
    topography.x = linspace(xlower,xupper,(nx+1))
    topography.y = linspace(ylower,yupper,(ny+1))
    topography.write(outfile, topo_type=1)
    print('Created ',outfile)

def qinit(x,y):
    """
    solitary wave
    """
    xhat = cos(alpha)*x + sin(alpha)*y
    eta = H*sech(gamma*(xhat-x1)/d)**2

    return eta

def plot_init():
    from clawpack.visclaw import colormaps
    fig,ax = subplots(figsize=(12,5))
    topo = Topography('wavetank.asc', topo_type=3)
    topo.plot(axes=ax, cb_kwargs={'shrink':0.7})

    wave = Topography('wave.xyz',1)
    amp = wave.Z.max()
    print(f'amplitude of wave = {amp:.6f}')
    Z = where(wave.Z < 0.1*amp, nan, wave.Z)
    Z = where(topo.Z > 1, nan, Z)
    Z = flipud(Z)
    #contour(wave.X,wave.Y,Z,amp*arange(.1,1,.1),colors='yellow')
    cf = contourf(wave.X,wave.Y,Z,amp*arange(.2,1.01,.05),
                  cmap=colormaps.blue_yellow_red, alpha=1)
    colorbar(cf, label='wave amplitude (m)', shrink=0.7)
    title('Wave tank topography and initial data (solitary wave)')
    fname = 'wavetank_initial.png'
    savefig(fname, bbox_inches='tight')
    print('Created ',fname)

if __name__=='__main__':
    maketopo()
    makeqinit()
    plot_init()
