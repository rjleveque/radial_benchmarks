from pylab import *
from clawpack.pyclaw.solution import Solution

frameno = 35

ce1 = loadtxt('celledges_1m.txt', skiprows=1)
fr1 = Solution()
fr1.read(frame=frameno,path='_output_1m',file_format='ascii')
q1 = fr1.states[0].get_q_global()

ce5 = loadtxt('celledges_5m.txt', skiprows=1)
fr5 = Solution()
fr5.read(frame=frameno,path='_output_5m',file_format='ascii')
q5 = fr5.states[0].get_q_global()

figure()

plot(ce1[:-1,0], q1[-1,:], 'r')
plot(ce5[:-1,0], q5[-1,:], 'b')
