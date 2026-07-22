import pyvista as pv
import numpy as np
from clawpack.visclaw import colormaps


# 1. Create a high-resolution sphere mesh
sphere = pv.Sphere(radius=1.0, theta_resolution=200, phi_resolution=200)

# 2. Extract Cartesian coordinates of the points
x, y, z = sphere.points[:, 0], sphere.points[:, 1], sphere.points[:, 2]

# 3. Convert Cartesian to Spherical coordinates
# theta: polar/colatitude angle (0 to pi, measured from +Z axis)
theta = np.arccos(z / np.sqrt(x**2 + y**2 + z**2))

# phi: azimuthal angle (-pi to pi, measured in the XY plane)
phi = np.arctan2(y, x)

# 4. Define your mathematical function, f(theta, phi)
# Example: A spherical harmonic-like pattern
#scalars = np.sin(3 * theta) * np.cos(2 * phi)
#scalars = theta

def axial_latitude(x,y,xpole,ypole):
    """
    Given (x,y), longitude and latitude on earth in WGS84, determine
    the axial latitude of this point relative
    to an axis of rotation that passes through the sphere
    with "north" pole (ax_lat = 90) at the point (xpole,ypole) in
    WGS84 coordinates.

    x,y can be scalars or numpy arrays with the same shape.
    """
    from clawpack.geoclaw.data import Rearth
    from clawpack.geoclaw.util import haversine
    from numpy import pi
    
    # great circle distance of x,y from axial pole:
    d = haversine(x,y,xpole,ypole)

    # convert distance to angle in degrees, with 0 at axial equator:
    ax_lat = (pi/2. - d/Rearth) * 180/pi
    
    return ax_lat

if 0:
    phi0 = 50  # axial latitude of shore
    B1d = lambda phi: phi0 - phi
    B = B1d(theta)

else:
    yhat0 = 60 * np.pi/180
    B1d = lambda yhat: np.where(abs(yhat - yhat0) < 10*np.pi/180, 1, -1)

    xpole = 0
    ypole = 30
    X = phi * 180/np.pi
    Y = (np.pi/2 - theta) * 180/np.pi
    yhat = axial_latitude(X,Y,xpole,ypole) * np.pi/180
    B = B1d(yhat)

scalars = B

# 5. Attach the scalars to the mesh and plot
sphere.point_data["custom_function"] = scalars

if 1:
    plotter = pv.Plotter()
    plotter.add_mesh(sphere, scalars="custom_function", 
                     cmap=colormaps.yellow_red_blue, clim=(-1,1))
                     #cmap="viridis")
                     #show_edges=True)
    plotter.show(window_size=(1500,1500))
