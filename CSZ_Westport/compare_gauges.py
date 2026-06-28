"""
Gauge comparison plots

"""

from pylab import *
from clawpack.pyclaw.gauges import GaugeSolution



gaugeno1 = 1
gaugeno2 = gaugeno1
gaugeno3 = gaugeno1

save_fig = True

if 0:
    outdir1 = '1d_radial/_output_5mG_10m'
    label1 = '1D with 10 m resolution'
    outdir2 = '1d_radial/_output_5mG_5m'
    label2 = '1D with 5 m resolution'
    #outdir3 = '1d_radial/_output_5mG_1m'
    #label3 = '1D with 1 m resolution'
    outdir3 = None
    fname = f'gauge{gaugeno1}_1D.png'


if 1:
    outdir1 = '1d_radial/_output_5mG_10m'
    label1 = '1D with 10 m resolution'
    outdir2 = '2d_test1/_output_6levels'
    label2 = '2D with 1/3" resolution'
    #outdir3 = '2d_test1/_output_5levels'
    #label3 = '2D with 1" resolution'
    outdir3 = None
    fname = f'gauge{gaugeno1}_2D.png'





dm = -400 + (gaugeno1-1)*200

gauge1 = GaugeSolution(gauge_id=gaugeno1, path=outdir1)
gauge2 = GaugeSolution(gauge_id=gaugeno2, path=outdir2)
if outdir3:
    gauge3 = GaugeSolution(gauge_id=gaugeno3, path=outdir3)

linecolors = ['r','b','r']

figure(500,figsize=(10,6))
clf()

subplot(211)
#text(40.5, 2.5, 'Water depth', fontsize=15, backgroundcolor='w')
text(0.02,0.93, 'Water depth', fontsize=15, backgroundcolor='w',
     ha='left', va='top',  transform=gca().transAxes)
plot(gauge1.t/60., gauge1.q[0,:], linecolors[0], label=label1)
plot(gauge2.t/60., gauge2.q[0,:], linecolors[1], label=label2)
if outdir3:
    plot(gauge3.t/60., gauge3.q[0,:], linecolors[2], label=label3)
legend(loc='upper right', framealpha=1)
xlim(40,60)
grid(True)
ylabel('meters')
title(f'Gauge {gaugeno1}  (${dm:.0f}$ meters from shore)', fontsize=15)


if 0:
    subplot(312)
    #text(40.5, 6.8, 'Surface elevation', fontsize=15, backgroundcolor='w')
    text(0.02,0.93, 'Surface', fontsize=15, backgroundcolor='w',
         ha='left', va='top',  transform=gca().transAxes)
    plot(gauge1.t/60., gauge1.q[-1,:], linecolors[0], label=label1)
    plot(gauge2.t/60., gauge2.q[-1,:], linecolors[1], label=label2)
    if outdir3:
        plot(gauge3.t/60., gauge3.q[-1,:], linecolors[2], label=label3)

    #legend(loc='upper left')
    xlim(40,60)
    grid(True)
    ylabel('meters')

    subplot(313)

else:
    subplot(212)


#text(40.5, 8.5, 'Flow speed', fontsize=15, backgroundcolor='w')
text(0.02,0.93, 'Flow speed', fontsize=15, backgroundcolor='w',
     ha='left', va='top',  transform=gca().transAxes)
h = gauge1.q[0,:]
hu = gauge1.q[1,:]
u = divide(hu, h, where=h>0.01, out=zeros(h.shape))
s = abs(u)
plot(gauge1.t/60., s, linecolors[0], label=label1)

h = gauge2.q[0,:]
hu = gauge2.q[1,:]
hv = gauge2.q[2,:]
u = divide(hu, h, where=h>0.01, out=zeros(h.shape))
v = divide(hv, h, where=h>0.01, out=zeros(h.shape))
s  = sqrt(u**2 + v**2)
plot(gauge2.t/60., s, linecolors[1], label=label2)

if outdir3:
    h = gauge3.q[0,:]
    hu = gauge3.q[1,:]
    hv = gauge3.q[2,:]
    u = divide(hu, h, where=h>0.01, out=zeros(h.shape))
    v = divide(hv, h, where=h>0.01, out=zeros(h.shape))
    s  = sqrt(u**2 + v**2)
    plot(gauge3.t/60., s, linecolors[2], label=label3)

#legend(loc='upper left')
xlim(40,60)
ylim(0,10)
grid(True)
xlabel('Minutes after earthquake', fontsize=12)
ylabel('meters/second')

if save_fig:
    savefig(fname, bbox_inches='tight')
    print('Saved ',fname)
