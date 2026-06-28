

import os, sys
import numpy
from clawpack.visclaw import geoplot
from clawpack.geoclaw.nonuniform_grid_tools import make_mapc2p
from clawpack.geoclaw.data import Rearth, LAT2METER

fname_celledges = os.path.abspath('celledges_10m.txt')

# reference solution:
res0 = '5m'
outdir0 = f'_output_5mG_{res0}'
#outdir0 = None
#outdir0 = 'xxxx'


if outdir0 is not None:
    path_celledges0 = os.path.abspath(f'celledges_{res0}.txt')
    mapc2p0_pa, mx_edge, xp_edge = make_mapc2p(path_celledges0)

    def mapc2p0(xc):
        polarangle = mapc2p0_pa(xc)
        xp = polarangle * LAT2METER / 1e3  # convert to km
        return xp

if 0:
    fname = '_output/fgmax.txt'
    try:
        d = numpy.loadtxt(fname)
        xmax = d[:,0]
        Bmax = d[:,1]
        hmax = d[:,2]
        etamax = numpy.where(hmax>1e-3, hmax+Bmax, numpy.nan)
        jmax = numpy.where(hmax>1e-3)[0].max()
        print("run-in = %8.2f m,  run-up = %8.2f m" % (xmax[jmax],etamax[jmax]))
        print('Loaded hmax from ',fname)
    except:
        xmax = None
        print('Failed to load ',fname)
else:
    xmax = None

#xmax = None # to suppress plotting max elevation as red curve

xlimits = [20, 22.68]

def setplot(plotdata=None):

    if plotdata is None:
        from clawpack.visclaw.data import ClawPlotData
        plotdata = ClawPlotData()

    plotdata.clearfigures()

    fname1 = os.path.join(plotdata.outdir, fname_celledges)
    mapc2p1_pa, mx_edge, xp_edge = make_mapc2p(fname1)

    def mapc2p1(xc):
        polarangle = mapc2p1_pa(xc)
        xp = polarangle * LAT2METER / 1e3  # convert to km
        return xp


    def fix_layout(current_data):
        from pylab import tight_layout
        tight_layout()

    def add_etamax(current_data):
        from pylab import plot
        from clawpack.visclaw.legend_tools import add_legend
        if xmax is not None:
            plot(xmax, etamax, 'r')
            add_legend(['max eta over simulation','surface elevation eta'],
                   ['r','b'], framealpha=1)

    plotfigure = plotdata.new_plotfigure(name='domain', figno=0)
    plotfigure.figsize = (8,6)
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(211)'
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = [-5,10]
    plotaxes.title = 'Surface displacement at time h:m:s'
    plotaxes.grid = True

    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = geoplot.surface
    plotitem.color = 'b'
    plotitem.MappedGrid = True
    plotitem.mapc2p = mapc2p1

    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    #plotitem.show = False
    plotitem.plot_var = geoplot.topo
    plotitem.color = 'g'
    plotitem.MappedGrid = True
    plotitem.mapc2p = mapc2p1

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(212)'
    plotaxes.xlimits = xlimits
    plotaxes.title = 'Full depth at time h:m:s'
    plotaxes.grid = True
    plotaxes.afteraxes = fix_layout

    plotitem = plotaxes.new_plotitem(plot_type='1d_fill_between')
    #plotitem.show = False
    plotitem.plot_var = geoplot.surface
    plotitem.plot_var2 = geoplot.topo
    plotitem.color = [0.4,0.4,1] # lighter blue
    plotitem.MappedGrid = True
    plotitem.mapc2p = mapc2p1

    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    #plotitem.show = False
    plotitem.plot_var = geoplot.topo
    plotitem.color = 'g'
    plotitem.MappedGrid = True
    plotitem.mapc2p = mapc2p1

    #-------------

    plotfigure = plotdata.new_plotfigure(name='shore', figno=1)
    plotfigure.figsize = (10,5)
    #plotfigure.show = False


    plotaxes = plotfigure.new_plotaxes()
    #plotaxes.xlimits = [22.66, 22.685]  # degrees
    plotaxes.xlimits = [2518, 2521]  # km
    plotaxes.ylimits = [-5,15]
    plotaxes.ylabel = 'meters'
    plotaxes.title = 'Zoom near shore at time h:m:s'
    plotaxes.grid = True
    #plotaxes.afteraxes = add_etamax
    plotaxes.xlabel = 'km from axial pole'

    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = geoplot.surface
    plotitem.color = 'b'
    plotitem.MappedGrid = True
    plotitem.mapc2p = mapc2p1

    # reference solution:
    if outdir0 is not None:
        plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
        #plotitem.show = False
        print('+++ using ', outdir0)
        plotitem.outdir = outdir0
        plotitem.plot_var = geoplot.surface
        plotitem.color = 'k'
        #plotitem.kwargs = {'linewidth':0.9}
        plotitem.MappedGrid = True
        plotitem.mapc2p = mapc2p0

    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = geoplot.topo
    plotitem.color = 'g'
    plotitem.MappedGrid = True
    plotitem.mapc2p = mapc2p1

    #----------

    plotfigure = plotdata.new_plotfigure(name='shore eta,s', figno=2)
    plotfigure.figsize = (8,6)
    plotfigure.show = False


    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(211)'
    #plotaxes.xlimits = [22.66, 22.685]  # degrees
    plotaxes.xlimits = [2518, 2521]  # km
    plotaxes.ylimits = [-5,15]
    plotaxes.ylabel = 'meters'
    plotaxes.title = 'Zoom near shore at time h:m:s'
    plotaxes.grid = True
    plotaxes.afteraxes = add_etamax

    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = geoplot.surface
    plotitem.color = 'b'
    plotitem.MappedGrid = True
    plotitem.mapc2p = mapc2p1

    # reference solution:
    if outdir0 is not None:
        plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
        #plotitem.show = False
        plotitem.outdir = outdir0
        plotitem.plot_var = geoplot.surface
        plotitem.color = 'k'
        #plotitem.kwargs = {'linewidth':0.9}
        plotitem.MappedGrid = True
        plotitem.mapc2p = mapc2p0

    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = geoplot.topo
    plotitem.color = 'g'
    plotitem.MappedGrid = True
    plotitem.mapc2p = mapc2p1

    def speed1d(current_data):
        q = current_data.q
        h = q[0,:]
        hu = q[1,:]
        u = numpy.divide(hu, h, where=h>0.01, out=numpy.zeros(h.shape))
        speed = abs(u)
        return speed

    plotaxes = plotfigure.new_plotaxes()
    #plotaxes.show = False
    plotaxes.axescmd = 'subplot(212)'
    #plotaxes.xlimits = [22.66, 22.685]  # degrees
    plotaxes.xlimits = [2518, 2521]  # km
    plotaxes.ylimits = [0,14]
    plotaxes.ylabel = 'meters / sec'
    plotaxes.title = 'Speed around shore at time h:m:s'
    plotaxes.grid = True
    plotaxes.afteraxes = fix_layout

    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = speed1d
    plotitem.color = 'b'
    plotitem.MappedGrid = True
    plotitem.mapc2p = mapc2p1

    # reference solution:
    if outdir0 is not None:
        plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
        #plotitem.show = False
        plotitem.outdir = outdir0
        plotitem.plot_var = speed1d
        plotitem.color = 'k'
        #plotitem.kwargs = {'linewidth':0.9}
        plotitem.MappedGrid = True
        plotitem.mapc2p = mapc2p0



    #-------------

    plotfigure = plotdata.new_plotfigure(name='3 plots', figno=10)
    plotfigure.figsize = (11,8)
    #plotfigure.show = False

    # ------------------------------
    # top plot: surface on whole domain
    plotaxes = plotfigure.new_plotaxes()
    #plotaxes.axescmd = 'axes([.1,.3,.8,.25])'
    plotaxes.axescmd = 'axes([.1,.65,.7,.25])'
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = [-10,15]
    print('+++ ylimits = ', plotaxes.ylimits)
    #plotaxes.title = 'Surface at time h:m:s'
    plotaxes.title = 'Surface'
    plotaxes.grid = True

    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    #plotitem.show = False
    plotitem.plot_var = geoplot.surface
    #plotitem.color = 'purple'
    plotitem.color = 'b'
    plotitem.MappedGrid = True
    plotitem.mapc2p = mapc2p1

    plotitem = plotaxes.new_plotitem(plot_type='1d_fill_between')
    plotitem.show = False
    plotitem.plot_var = geoplot.surface
    plotitem.plot_var2 = geoplot.topo
    plotitem.color = [.5,.5,1]
    plotitem.MappedGrid = True
    plotitem.mapc2p = mapc2p1

    # reference solution:
    if outdir0 is not None:
        plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
        #plotitem.show = False
        plotitem.outdir = outdir0
        plotitem.plot_var = geoplot.surface
        plotitem.color = 'k'
        plotitem.kwargs = {'linewidth':0.9}
        plotitem.MappedGrid = True
        plotitem.mapc2p = mapc2p0

    # ------------------------------
    # middle plot, topo alone:
    plotaxes = plotfigure.new_plotaxes()
    #plotaxes.axescmd = 'axes([.1,.05,.8,.15])'
    plotaxes.axescmd = 'axes([.1,.4,.7,.15])'
    plotaxes.xlimits = xlimits
    #plotaxes.ylimits = [-1.1*h0, 0.1*h0]
    plotaxes.title = 'Topography at time h:m:s'
    plotaxes.grid = True

    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = geoplot.topo
    plotitem.color = 'g'
    plotitem.MappedGrid = True
    plotitem.mapc2p = mapc2p1

    # ------------------------------
    # bottom plot: zoom around shore:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'axes([.1,.05,.7,.25])'
    plotaxes.xlimits = [22.65, 22.685]
    plotaxes.ylimits = [-20,20]
    print('+++ ylimits = ', plotaxes.ylimits)
    plotaxes.title = 'Zoom around shore at time h:m:s'
    plotaxes.grid = True
    #plotaxes.afteraxes = add_hmax


    # reference solution
    if outdir0 is not None:
        plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
        #plotitem.show = False
        plotitem.outdir = outdir0
        plotitem.plot_var = geoplot.surface
        plotitem.color = 'k'
        plotitem.kwargs = {'linewidth':0.9}
        plotitem.MappedGrid = True
        plotitem.mapc2p = mapc2p0
        #plotitem.afterpatch = afterpatch


    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    #plotitem.show = False
    plotitem.plot_var = geoplot.surface
    #plotitem.color = 'purple'  # 1D at t
    plotitem.color = 'm'  # 1D at t
    plotitem.kwargs = {'linewidth':0.9}
    plotitem.MappedGrid = True
    plotitem.mapc2p = mapc2p1


    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = geoplot.topo
    plotitem.color = 'g'
    plotitem.MappedGrid = True
    plotitem.mapc2p = mapc2p1


    #-----------------------------------------
    # Figures for gauges
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='depth', figno=300, \
                    type='each_gauge')

    plotfigure.clf_each_gauge = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.time_scale = 1/3600.  # convert seconds to hours
    plotaxes.time_label = 'time (hours) post-quake'
    plotaxes.xlimits = 'auto'
    #plotaxes.ylimits = [-2.0, 2.0]
    plotaxes.title = 'Water depth'
    plotaxes.grid = True

    # Plot depth as blue curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 0
    plotitem.plotstyle = 'b-'



    #-----------------------------------------

    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    plotdata.print_gaugenos = 'all'          # list of gauges to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?
    plotdata.parallel = True                 # make multiple frame png's at once
    plotdata.mp4_movie = True

    return plotdata
