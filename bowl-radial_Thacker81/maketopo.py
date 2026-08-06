
"""
Module to create topo and qinit data files for this example.
"""

from numpy import *
from clawpack.geoclaw.topotools import Topography

from true_solution import D0, L


def maketopo():
    """
    Output topography file for the entire domain
    """
    nx = 200
    ny = 200
    xlower = -240.0
    xupper = 240.0
    ylower = -240.0
    yupper = 240.0
    outfile= "bowl.asc"

    topography = Topography(topo_func=topo)
    topography.x = linspace(xlower,xupper,(nx+1))
    topography.y = linspace(ylower,yupper,(ny+1))
    topography.write(outfile, topo_type=3, header_style='asc',
                     Z_format="%10.3f")
    print('Created ',outfile)


def topo(x,y):
    """
    Parabolic bowl
    """
    z = -D0 * (1 - (x**2 + y**2)/L**2)
    return z


if __name__=='__main__':
    maketopo()
