
"""
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.

"""

from numpy import *

from params import grav, D0, L, eta0

from true_solution import omega, A, Bfcn, qtrue

if 0:
    from clawpack.clawutil.data import ClawData
    probdata = ClawData()
    probdata.read('setprob.data', force=True)
    D0 = probdata.D0
    L = probdata.L
    eta0 = probdata.eta0
    print(f'Parameters: D0 = {D0}, L = {L}, eta0 = {eta0}')

    omega = sqrt(8.*grav*D0 / L**2)
    grav = 9.81

    A = ((D0 + eta0)**2 - D0**2) / ((D0 + eta0)**2 + D0**2)

    # parabolic bowl with depth D0 at center, B=0 at radius L:
    B = lambda x,y: -D0 * (1 - (x**2 + y**2)/L**2)

    def qtrue(x,y,t):
        denom = 1 - A*cos(omega*t)
        eta = D0 * (sqrt(1-A**2)/denom - 1 \
              - (x**2 + y**2)/L**2 * ((1-A**2)/(1-A*cos(omega*t)**2 - 1)))
        u = 1/denom * (0.5*omega*x*A*sin(omega*t))
        v = 1/denom * (0.5*omega*y*A*sin(omega*t))
        h = eta - B(x,y)
        return h,u,v,eta


    a = 1.
    sigma = 0.5
    h0 = 0.1

#--------------------------
def setplot(plotdata=None):
#--------------------------

    """
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of pyclaw.plotters.data.ClawPlotData.
    Output: a modified version of plotdata.

    """


    from clawpack.visclaw import colormaps, geoplot

    if plotdata is None:
        from clawpack.visclaw.data import ClawPlotData
        plotdata = ClawPlotData()


    plotdata.clearfigures()  # clear any old figures,axes,items data

    def set_drytol(current_data):
        # The drytol parameter is used in masking land and water and
        # affects what color map is used for cells with small water depth h.
        # The cell will be plotted as dry if h < drytol.
        # The best value to use often depends on the application and can
        # be set here (measured in meters):
        current_data.user["drytol"] = 1.e-3

    plotdata.beforeframe = set_drytol

    qref_dir = None

    def addgauges(current_data):
        from clawpack.visclaw import gaugetools
        gaugenos = 'all'
        gaugetools.plot_gauge_locations(current_data.plotdata, \
             gaugenos=gaugenos, format_string='ko', add_labels=True)


    land_cmap = colormaps.make_colormap({ 0.0:[0.1,0.4,0.0],
                                         0.25:[0.0,1.0,0.0],
                                          0.5:[0.8,1.0,0.5],
                                          1.0:[0.8,0.5,0.2]})

    #-----------------------------------------
    # Figure for pcolor plot
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='pcolor', figno=0)

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('pcolor')
    plotaxes.title = 'Surface'
    plotaxes.scaled = True

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.surface_or_depth
    plotitem.pcolor_cmap = geoplot.tsunami_colormap
    plotitem.pcolor_cmin = -1
    plotitem.pcolor_cmax = 1
    plotitem.add_colorbar = True
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [0]

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.land
    plotitem.pcolor_cmap = geoplot.land_colors
    plotitem.pcolor_cmin = -1.0
    plotitem.pcolor_cmax = 3.0
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [0]

    def plot_shore(current_data):
        from pylab import linspace, where, cos, sin, plot, legend
        t = current_data.t
        rout = linspace(0, 2*L, 1000)
        h_true, u_true, v_true, eta_true = qtrue(rout, zeros(rout.shape), t)
        jshore = where(h_true > 0)[0].max()
        rshore = rout[jshore]
        theta = linspace(0, 2*pi, 1000)
        xshore = rshore * cos(theta)
        yshore = rshore * sin(theta)
        plot(xshore, yshore, 'k', linewidth=0.6, label='true shoreline')
        legend(loc='upper left', fontsize=9)

    plotaxes.afteraxes = plot_shore

    # Add contour lines of bathymetry:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    plotitem.show = False
    plotitem.plot_var = geoplot.topo
    from numpy import arange, linspace
    plotitem.contour_levels = linspace(-.1, 0.5, 20)
    plotitem.amr_contour_colors = ['k']  # color on each level
    plotitem.kwargs = {'linestyles':'solid'}
    plotitem.amr_contour_show = [1]
    plotitem.celledges_show = 0
    plotitem.patchedges_show = 0

    #-----------------------------------------
    # Figure for transect plots
    #-----------------------------------------

    plotfigure = plotdata.new_plotfigure(name='transect', figno=9)
    plotfigure.figsize = (10,6)
    plotaxes = plotfigure.new_plotaxes('pcolor')

    def plot_xsec(current_data):
        from pylab import plot,legend,xlabel,sqrt,grid,xlim,ylim, \
                    xticks,ylabel,where,nan
        from numpy import cos,pi,linspace,zeros,ones,hstack,sin
        from clawpack.pyclaw import Solution
        from clawpack.visclaw import gridtools
        pd = current_data.plotdata
        frameno = current_data.frameno
        framesoln = Solution(frameno, path=pd.outdir, file_format=pd.format)
        method = 'linear'
        rout = linspace(0, 2*L, 1000)

        t = current_data.t
        h_true, u_true, v_true, eta_true = qtrue(rout, zeros(rout.shape), t)
        plot(rout, eta_true, 'k', label='analytic solution')
        plot(-rout, eta_true, 'k')
        B_true = Bfcn(rout, zeros(rout.shape))
        plot(rout, B_true,'g',label='topography')
        plot(-rout, B_true,'g')
        c = ['b','c','r','m']
        for k,alpha in enumerate([0,10,30,45]):
            xout = rout * cos(alpha*pi/180)
            yout = rout * sin(alpha*pi/180)
            h_out = gridtools.grid_output_2d(framesoln, 0, xout, yout,
                                             method=method)
            eta_out = gridtools.grid_output_2d(framesoln, -1, xout, yout,
                                               method=method)
            B_out = eta_out - h_out
            eta_out = where(h_out > 1e-3, eta_out, nan)
            #plot(rout, B_out, 'g')
            plot(rout, eta_out, color=c[k], label=f'for alpha={alpha:.1f} degrees')
            plot(-rout, eta_out, color=c[k])

        legend(loc='upper left', framealpha=1, fontsize=9)
        #xticks(rotation=20)
        xlabel('x (meters)')
        ylabel('elevation (meters)')
        xlim(-4,4)
        ylim(-2.5,2.5)
        grid(True)

    plotaxes.afteraxes = plot_xsec
    plotaxes.title = 'radial transects at angles alpha to x-axis,'


    #-----------------------------------------
    # Figure for scatter plots
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='scatter', figno=10)
    plotfigure.show = False

    # needs fixing

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = [-2,2]
    plotaxes.ylimits = [-0.15,0.3]
    plotaxes.title = 'Cross section at y=0'
    def plot_topo_xsec(current_data):
        from pylab import plot, cos,sin,where,legend,nan
        t = current_data.t

        x = linspace(-2,2,201)
        y = 0.
        B = h0*(x**2 + y**2)/a**2 - h0
        eta1 = sigma*h0/a**2 * (2.*x*cos(omega*t) + 2.*y*sin(omega*t) -sigma)
        etatrue = where(eta1>B, eta1, nan)
        plot(x, etatrue, 'r', label="true solution", linewidth=2)
        plot(x, B, 'g', label="bathymetry")
        ## plot([0],[-1],'kx',label="Level 1")  # shouldn't show up in plots,
        ## plot([0],[-1],'bo',label="Level 2")  # but will produced desired legend
        plot([0],[-1],'bo',label="Computed")  ## need to fix plotstyle
        legend()
    plotaxes.afteraxes = plot_topo_xsec

    plotitem = plotaxes.new_plotitem(plot_type='1d_from_2d_data')

    def xsec(current_data):
        # Return x value and surface eta at this point, along y=0
        from pylab import where,ravel
        x = current_data.x
        y = ravel(current_data.y)
        dy = current_data.dy
        q = current_data.q

        ij = where((y <= dy/2.) & (y > -dy/2.))
        x_slice = ravel(x)[ij]
        eta_slice = ravel(q[3,:,:])[ij]
        return x_slice, eta_slice

    plotitem.map_2d_to_1d = xsec
    plotitem.plotstyle = 'kx'     ## need to be able to set amr_plotstyle
    plotitem.kwargs = {'markersize':3}
    plotitem.amr_show = [1]  # plot on all levels

    # Figures for gauges
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Surface & topo', figno=300, \
                    type='each_gauge')

    plotfigure.clf_each_gauge = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = 'auto'
    plotaxes.ylimits = [-0.05, 0.05]
    plotaxes.title = 'Surface'
    plotaxes.grid = True

    # Plot surface as blue curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = -1
    plotitem.plotstyle = 'b-'


    #-----------------------------------------

    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    plotdata.print_gaugenos = []             # list of gauges to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?
    plotdata.parallel = True                 # make multiple frame png's at once

    return plotdata
