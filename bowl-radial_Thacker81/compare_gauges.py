from pylab import *
from clawpack.pyclaw.gauges import GaugeSolution
import true_solution

outdir1 = './_output'
outdir2 = 'sgn2d/_output'
gaugeno1 = 100
gaugeno2 = 100

gauge1 = GaugeSolution(gauge_id=gaugeno1, path=outdir1)
gauge2 = GaugeSolution(gauge_id=gaugeno2, path=outdir2)

figure(500,figsize=(13,5))
clf()

h,u,v,eta = true_solution.qtrue(0,0,gauge1.t)

plot(gauge1.t, eta, 'k', label='SWE - Thacker')
plot(gauge1.t, gauge1.q[-1,:], 'b', label='SWE - GeoClaw')
plot(gauge2.t, gauge2.q[-1,:], 'r', label='SGN - GeoClaw')

legend(bbox_to_anchor=(1.1, 0.2), loc='upper right', framealpha=1)
#xlim(0,2)
#ylim(-2,4)
grid(True)
xlabel('Time')
ylabel('meters')

title('Gauge comparison -- surface at (0,0)')
