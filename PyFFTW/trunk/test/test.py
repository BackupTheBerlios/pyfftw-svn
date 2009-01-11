import numpy
import pylab
from numpy.fft import fftshift, fft, ifft
from scipy.fftpack import fft as sfft, ifft as sifft
import fftw3
import time

N=2**15
repeats=500
h = 0.1
beta = 1

f=numpy.linspace(-5,5,N)
df = f[1]-f[0]
t = numpy.linspace(-1./(df*2),1./(df*2),N)
ts = fftshift(t)
fs=fftshift(f)
tmp = numpy.zeros(len(f),dtype=complex)
tmp2 = numpy.zeros(len(f),dtype=complex)
gs = numpy.zeros(len(f),dtype=complex)
g = numpy.zeros(len(f),dtype=complex)
fft_plan = fftw3.Plan(g,gs,flags=['measure'])
ifft_plan = fftw3.Plan(gs,g,direction='backward',flags=['measure'])
gs[:] = numpy.exp(-fs[:]**2/0.02)+0.j
di = numpy.exp(-1.j*h*beta*fs)
ti = time.time()
for i in xrange(repeats):
    gs *= di
    ifft_plan()
    g /= N
    fft_plan()
to = time.time()
print "fftw time %f s" %(to-ti)
del fft_plan,ifft_plan

gs2 = numpy.exp(-fs**2/0.02)+0.j
g2 = numpy.zeros(len(f),dtype=complex)
ti = time.time()
for i in xrange(repeats):
    gs2 *= di
    g2 = ifft(gs2)
    gs2 = fft(g2)
to = time.time()
print "numpy time %f s" %(to-ti)

gs3 = numpy.exp(-fs**2/0.02)+0.j
g3 = numpy.zeros(len(f),dtype=complex)
ti = time.time()
for i in xrange(repeats):
    gs3 *= di
    g3 = sifft(gs3)
    gs3 = sfft(g3)
to = time.time()
print "scipy time %f s" %(to-ti)


pylab.plot(ts,abs(g)**2,label='fftw')
pylab.plot(ts,abs(g2)**2,label='numpy')
pylab.plot(ts,abs(g3)**2,label='scipy')
pylab.xlabel('time')
pylab.legend()
pylab.figure()
pylab.plot(fs,abs(gs)**2,label='fftw')
pylab.plot(fs,abs(gs2)**2,label='numpy')
pylab.plot(fs,abs(gs3)**2,label='scipy')
pylab.xlabel('frequency')
pylab.legend()
pylab.show()






