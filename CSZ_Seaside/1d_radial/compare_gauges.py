from pylab import *
from clawpack.pyclaw.gauges import GaugeSolution

res1 = 2
res2 = 5
outdir1 = f'_output_{res1}m'
outdir2 = f'_output_{res2}m'
#gaugeno = 28380
gaugeno = 24000

gauge1 = GaugeSolution(gauge_id=gaugeno, path=outdir1)
gauge2 = GaugeSolution(gauge_id=gaugeno, path=outdir2)

figure(500,figsize=(13,5))
clf()

if 1:
    plot(gauge2.t/60., gauge2.q[-1,:], 'b', label=f'onshore {res2}m')
    plot(gauge1.t/60., gauge1.q[-1,:], 'r', label=f'onshore {res1}m')
    qoi = 'surface elevation'
else:
    plot(gauge2.t/60., gauge2.q[0,:], 'b', label=f'onshore {res2}m')
    plot(gauge1.t/60., gauge1.q[0,:], 'r', label=f'onshore {res1}m')
    qoi = 'water depth'

xlim(0,60)
#ylim(0,20)
grid(True)
xlabel('Minutes after earthquake')
ylabel('meters')

title(f'Gauge {gaugeno} comparison of {qoi}')
legend(loc='upper left', framealpha=1)
