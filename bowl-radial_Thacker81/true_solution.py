"""
The true solution to the radially symmetric parabolic bowl problem
from Thacker 1981.

The parameters defining the problem are imported from here into
maketopo.py
setrun.py
setplot.py

"""

from pylab import *


# set parameters defining problem

# depth at center of parabolic bowl:
D0 = 10.

# radius of B=0 contour:
L = 200.

# initial surface elevation at center of bowl:
eta0 = 2.

# gravitational force:
grav = 9.81

print(f'Parameters: D0 = {D0}, L = {L}, eta0 = {eta0}')

omega = sqrt(8.*grav*D0 / L**2)
Tperiod = 2*np.pi/omega
A = ((D0 + eta0)**2 - D0**2) / ((D0 + eta0)**2 + D0**2)
print(f'omega = {omega:3f}, Tperiod = {Tperiod:.3f} sec, A = {A:.3f}')

# parabolic bowl with depth D0 at center, B=0 at radius L:
Bfcn = lambda x,y: -D0 * (1 - (x**2 + y**2)/L**2)

def qtrue(x,y,t):
    denom = 1 - A*cos(omega*t)
    B = Bfcn(x,y)
    eta = D0 * (sqrt(1-A**2)/denom - 1 \
          - (x**2 + y**2)/L**2 * ((1-A**2)/(1-A*cos(omega*t))**2 - 1))
    eta = maximum(B, eta)
    u = 1/denom * (0.5*omega*x*A*sin(omega*t))
    v = 1/denom * (0.5*omega*y*A*sin(omega*t))
    h = eta - B
    return h,u,v,eta


def plot_eta(t):

    x = linspace(-1.2*L, 1.2*L, 201)
    y = linspace(-1.2*L, 1.2*L, 201)
    X,Y = meshgrid(x,y,indexing='ij')
    B = Bfcn(X,Y)
    h,u,v,eta = qtrue(X,Y,t)
    #fig,axs = subplots(1,2,figsize=(10,6))
    figure(301)
    #clf()
    plot(x, eta[:,100], 'b')
    plot(x, B[:,100], 'g')
    grid(True)
    #axis('scaled')
    xlabel('x (m)')
    ylabel('elevation (m)')
    title(f'Surface eta at time {t:.2f} seconds')

    figure(302)
    #clf()
    plot(x, u[:,100], 'b')
    #plot(x, B[:,100], 'g')
    grid(True)
    #axis('scaled')
    xlabel('x (m)')
    ylabel('speed (m/s)')
    title(f'Radial speed at time {t:.2f} seconds')
