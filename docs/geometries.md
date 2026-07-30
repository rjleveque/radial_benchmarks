(geometries)=
# Coordinate Systems and Geometries for 2D Test Problems Based on 1D Solutions

The idea of using a 1D depth-averaged problem and its solution to design
a nontrivial test problem in 2D 
can take several forms, depending on the coordinate systems used.

Here "nontrivial" means a test of the 2D equations and
software that does not simply reduce to the 1D equation in one direction with
constant values in the other direction.

The 1D "solution" might be an exact analytic solution for a simple problem,
or for more interesting problems with no exact solution, it could be
a reference solution that is 
computed using a very fine grid in 1D with a trusted code
(ideally with several different codes, and with convergence tests to confirm
that the accuracy of the reference solution is high relative to the
expected errors in the 2D solution).


## Planar coordinates

If the 2D code to be tested in in planar x-y coordinates (in units of meters,
for example) then there are at least two ways one could use a 1D solution to
design a nontrivial 2D test:

### Rotated grid

Choose a direction in the 2D plane that is not aligned with either of the
coordinate directions and set up the domain, topography, initial and boundary
conditions so that the solution should agree with the 1D solution in this
direction.  For example, the original benchmark workshop problem BP01
"Solitary Wave on a Simple Beach" (based on Synolakis) had a specified
initial condition $\hat\eta(x,0)$ and piecewise linear topography $\hat B(x)$
consisting of a flat section and a constant slope beach (hats denoting 1D).
The exact solution $\hat\eta(x,t)$ for runup on the beach is known.

In the 2D plane we could choose an angle $\alpha$ and place this 1D problem
on a 2D computational grid at this angle by defining the initial 2D surface
elevation as
$$\eta(x,y,0) = \hat\eta(\cos(\alpha)x + \sin(\alpha)y,\, 0)$$
on the topography
$$B(x,y) = \hat B (\cos(\alpha)x + \sin(\alpha)y).$$
The exact solution is then
$$\eta(x,y,t) = \hat\eta(\cos(\alpha)x + \sin(\alpha)y,\, t)$$.


If this problem in this rectangular domain with a 2D numerical method, then
garbage will probably be generated near the boundaries. But if the domain is
large enough that the waves from the boundaries do not reach the central part
of the domain over the time where the solution is tested, then the solution
along the transect through the origin shown in the figure above should agree
well with the 1D solution.  Since the wave is coming up the beach at an angle
to the computational grid, this is a nontrivial test of the 2D code, and it
could be interesting to test how well runup and drawdown are modeled at
different angles $\alpha$.  

To minimize boundary effects, the 2D topography could be modified so that it
looks more like a wave tank of some finite width $W$
placed on the grid at an angle,
e.g. by choosing some large value $B_{big}$ and setting
$B(x,y) = B_{big}$ wherever $|\cos(\alpha)y - \sin(\alpha)x| > W/2$.

The figure below shows how the piecewise linear topography (flat bottom and
linear beach)  and initial solitary wave would look
on a 2D computational grid in Cartesian coordinates for $\alpha = 0.2$
and $W = 50$.

:::{figure} figs/wavetank_initial.png
:width: 400pt
:::

The solution on a transect down the center of the channel (or on parallel
lines) can be compared with the exact solution.

I haven't done this comparison yet, but below is an animation of the solution
on 3 parallel transects at 0, 0.3, and 0.5 m from the center of the channel.
(Note the initial velocity was set to 0, so the initial hump splits into 2
waves. Also this was solved using the nonlinear shallow water equations, so
it won't agree exactly with the analytic solution.)


:::{dropdown} Animation of 1D transects of the 2D solution
:close:
```{figure} figs/wavetank_solitary_transects.mp4
:width: 600px
:align: center
```
:::


This same idea could be used to rotate a physical wave tank problem such
as the Matsuyuma problem to generate a nontrivial 2D test problem in which
the wave tank observations from the one-dimensional physical wave tank are
used as comparison data. (Although that might be more challenging since the
wave tank ends at a vertical wall rather than a sloping beach.)



### Polar coordinates

Another possibility is to select a problem where the data and solution are
one-dimensional in polar coordinates $(r,\theta)$, varying only with radius $r$.
Then solve the problem numerically in 2D using x-y coordinates, so that the
solution is nontrivial in these coordinates.

There are few exact solutions known of this type, although there is one in
https://doi.org/10.1017/S0022112081001882
that might be a good test.  In this problem the topography is a parabolic
bowl and the initial condition is a parabolic surface chosen so that there
is an exact oscillatory solution with the shoreline moving up and down in
the bowl. 

:::{dropdown} Animation of 2D solution in parbolic bowl
:close:
```{figure} figs/bowl-radial_Thacker81_2D.mp4
:width: 600px
:align: center
```
:::

:::{dropdown} Animation of 1D transects of the 2D solution
:close:
```{figure} figs/bowl-radial_Thacker81_transects.mp4
:width: 600px
:align: center
```
:::

A fine grid 1D numerical solution can be computed as a reference solution to
any problem where the topography and initial conditions are radially symmetric,
by solving the 1D depth-averaged equations with the addition of a suitable
source term in the momentum equation.  

One possible way to extend this parabolic bowl problem would
be to add friction and insure the radial solution agrees with a fine 1D
solution for various values of the Manning coefficient.

One radial example is provided in GeoClaw, see
[bowl-radial example](https://www.clawpack.org/gallery/_static/geoclaw/examples/tsunami/bowl-radial/README.html).

## 2D on the sphere

For testing real-world tsunami modeling codes, we need to devise test problems
that can be solved in longitude-latitude coordinates with spherical geometry,
since those are the equations that are generally solved even for nearfield
tsunami runup problems where the spherical geometry terms are relatively
unimportant.

If we define topography and initial conditions that are
a function of latitude alone, then the solution should remain axisymmetric
on the sphere.  However, this would be a "trivial" 2D problem in the sense
that the solution would be constant at each longitude and hence along each
row of the computational grid.

To create a nontrivial test problem, we can choose a different axis of
revolution for the purposes of defining the topography and initial data, one
that cuts through the earth at some specified
physical (longitude, latitude) denoted by $(x_0, y_0)$ and the antipode
$(360 - x_0, -y_0)$.  Relative to this axis,
we can define an "axial latitude" $\hat y_0$ that varies from $90$ degrees
at the "axial north pole" $(x_0, y_0)$ to $-90$ degrees at the antipode.

The axisymmetric solution can then be computed as a function of $\hat y$
by solving a 1D equation with the addition of source terms,
as described e.g. in [these
notes](https://faculty.washington.edu/rjl/misc/spherical_swe_2023-10-27.pdf).

This solution can then be mapped back to the sphere representing the earth
with standard longitude-latitude coordinates to produce a reference
solution.

This is described in more detail with an example in [](#test1).


(circular_ocean)=
## A circular ocean

The circular ocean presented in [](#spherical_nearfield)
was used in the context of modeling nearfield runup,  and
the computational domain was chosen along one stretch of the coast, so there
was no propagation through the singularity at the axial pole.

But this circular ocean on the sphere is not really suitable for
modeling trans-oceanic tsunami propagation, since there is a singularity at
the angular pole in the center of the ocean that is not realistic.
Moreover, an axisymmetric solution in the circular ocean can't realistically
model the case of a subduction zone earthquake near one shore causing
runup on the opposite shore, since the data and solution must be the same
everywhere around the shore in the axisymmetric case.

(annular_ocean)=
## An annular ocean

To design a test problem for farfield tsunamis it is better to start
with an annular ocean that extends from axial latitude $\hat y_1$ to
$\hat y_2$ where both of these values are well away from $\pm 90$ degrees
(the axial poles). Then a subduction zone earthquake can be placed near one
coastline, e.g. at $\hat y_1$, and the runup and inundation studied at the
other coast, at $\hat y_2$. The transoceanic distance is then roughly
$(\hat y_2 - \hat y_1) * R_{earth} * \pi/180$.  To generate a nontrivial 2D
problem, the axial north pole can again be put at any location on "earth",
and a computational domain in longitude, latitude $(x,y)$ chosen that is
large enough to cover part of both shores, along with an axial meridian
connecting them, along which the solution should agree with the 1D
axisymmetric solution. 

The figure below shows an annular ocean in blue,
extending from axial latitude 50 to 70, i.e., $50 < \hat y < 70$, 
placed on the earth with the axial pole at latitude $y_0 = 30$.
The black arrow shows the axis of symmetry.

:::{figure} figs/annular_ocean.jpg
:width: 300px
:align: center
:::

A test problem illustrating this is still under construction.
