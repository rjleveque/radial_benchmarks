
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
""" 

import numpy
from clawpack.visclaw import colormaps

alpha = 0.1

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
    plotfigure.figsize=(11,6)

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('pcolor')
    plotaxes.title = 'Surface'
    plotaxes.scaled = True
    #plotaxes.xlimits = [-2,2]
    #plotaxes.ylimits = [-2,2]
    plotaxes.afteraxes = addgauges

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.surface_or_depth
    plotitem.pcolor_cmap = geoplot.tsunami_colormap
    plotitem.pcolor_cmin = -0.005
    plotitem.pcolor_cmax = 0.005
    plotitem.add_colorbar = True
    plotitem.amr_celledges_show = [1,0,0]
    plotitem.amr_patchedges_show = [0,1]

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.land
    plotitem.pcolor_cmap = land_cmap  #geoplot.land_colors
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 2.0
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [1,0,0]
    plotitem.amr_patchedges_show = [0,1]

    # Add contour lines of eta:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    #plotitem.show = False
    plotitem.plot_var = -1
    from numpy import arange, linspace
    plotitem.contour_levels = arange(0.005, 0.05, 0.005)
    plotitem.amr_contour_colors = ['yellow']  # color on each level
    plotitem.kwargs = {'linestyles':'solid', 'linewidths':0.8}
    plotitem.amr_contour_show = [0,1]  
    plotitem.celledges_show = 0
    plotitem.patchedges_show = 0
    plotitem.show = True

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
        xhat = linspace(-5, 40, 1000)
        for offset in [0,0.3,0.5]:
            yhat = offset*ones(xhat.shape)
            xout = cos(alpha)*xhat - sin(alpha)*yhat
            yout = sin(alpha)*xhat + cos(alpha)*yhat
            h_out = gridtools.grid_output_2d(framesoln, 0, xout, yout,
                                             method=method)
            eta_out = gridtools.grid_output_2d(framesoln, -1, xout, yout,
                                               method=method)
            B_out = eta_out - h_out
            eta_out = where(h_out > 1e-3, eta_out, nan)
            plot(xout, B_out, 'g')
            plot(xout, eta_out, 'b', label=f'along yhat = {offset:.3f}')

        #legend(framealpha=1)
        xticks(rotation=20)
        xlabel('x (meters)')
        ylabel('y (meters)')
        xlim(-5,10)
        ylim(-0.05, 0.05)
        grid(True)

    plotaxes.afteraxes = plot_xsec
    plotaxes.title = 'Surface on three parallel transects'


    #-----------------------------------------
    # Figure for scatter plots
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='scatter', figno=10)

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('pcolor')
    plotaxes.title = 'Scatter plot of cell values vs. xhat'
    #plotaxes.scaled = True
    plotaxes.xlimits = [-5,60]
    plotaxes.ylimits = [-0.1,0.1]
    plotaxes.grid = True

    # Set up for item on these axes: scatter of 2d data
    
    def eta_vs_xhat(current_data):
        # Return radius of each grid cell and p value in the cell
        from pylab import sqrt,sin,cos,where,nan
        x = current_data.x
        y = current_data.y
        xhat = cos(alpha)*x + sin(alpha)*y
        yhat = -sin(alpha)*x + cos(alpha)*y
        q = current_data.q
        h = q[0,:,:]
        eta = q[-1,:,:]
        eta = where(h>1e-3, eta, nan)
        eta = where(abs(yhat) < 1, eta, nan)
        return xhat, eta
    
    def B_vs_xhat(current_data):
        # Return radius of each grid cell and p value in the cell
        from pylab import sqrt,sin,cos,where,nan
        x = current_data.x
        y = current_data.y
        xhat = cos(alpha)*x + sin(alpha)*y
        yhat = -sin(alpha)*x + cos(alpha)*y
        q = current_data.q
        h = q[0,:,:]
        eta = q[-1,:,:]
        B = eta - h
        B = where(abs(yhat) < 1, B, nan)
        #import pdb; pdb.set_trace()
        return xhat, B

    plotitem = plotaxes.new_plotitem(plot_type='1d_from_2d_data')
    plotitem.map_2d_to_1d = B_vs_xhat
    plotitem.show = True       # show on plot?
    plotitem.plotstyle = '.'
    plotitem.color = 'g'
    
    plotitem = plotaxes.new_plotitem(plot_type='1d_from_2d_data')
    plotitem.map_2d_to_1d = eta_vs_xhat
    plotitem.show = True       # show on plot?
    plotitem.plotstyle = '.'
    plotitem.color = 'b'
    
    # Set up for item on these axes: 1d reference solution
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.show = (qref_dir is not None)
    plotitem.outdir = qref_dir
    plotitem.plot_var = 0
    plotitem.plotstyle = '-'
    plotitem.color = 'r'
    plotitem.kwargs = {'linewidth': 2}
    
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
    
    def add_zeroline(current_data):
        from pylab import plot, legend
        t = current_data.t
        #legend(('surface','topography'),loc='lower left')
        plot(t, 0*t, 'k')

    #plotaxes.afteraxes = add_zeroline


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

    
