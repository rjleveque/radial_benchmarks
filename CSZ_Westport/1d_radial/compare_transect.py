from pylab import *
from clawpack.pyclaw import Solution

from clawpack.visclaw import gridtools, legend_tools
from clawpack.geoclaw.util import haversine, gctransect
from clawpack.geoclaw.data import Rearth
import mapper

from clawpack.clawutil.util import fullpath_import
setplot_module = fullpath_import('setplot.py')

outdir = '_output_5mG_10m/'
#outdir0 = '_output_5mG_1m/'  # reference soln, need to set in setplot.py

#framesoln = Solution(47, path=outdir1d, file_format='ascii')
tmin = 45
frameno = tmin

plotdata = setplot_module.setplot()
plotdata.outdir = outdir
plotdata.printfigs = False
plotdata.print_fignos = [1]
plotdata.plotframe(frameno)

plotdata.outdir = outdir
plotdata.printfigs = False
plotdata.print_fignos = [1]
plotdata.plotframe(frameno)


labels = ['1D with 10 m resolution',
          '1D with 5 m resolution',
          '1D topography']

legend_tools.add_legend(labels, colors=['b','k','g'],
                        loc='upper left', framealpha=1)

fname = f'1Dtransect_{tmin}min.png'
savefig(fname, bbox_inches='tight')
print('Created ',fname)
