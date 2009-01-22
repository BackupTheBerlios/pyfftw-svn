from numpy.fft import fft,ifft,fftshift
import numpy
import pylab
import fftw3
from scipy.fftpack import fft as sfft, ifft as sifft
import time

h = 0.01
beta =1

def fftw_propagation(N,repeats):
    t = numpy.linspace(-5,5,N)
    dt = t[1]-t[0]
    f = numpy.linspace(-1/dt/2.,1/dt/2.,N)
    f = fftshift(f)
    t = fftshift(t)
    farray = fftw3.fftw_array(len(f),dtype=complex)
    tarray = fftw3.fftw_array(len(t),dtype=complex)
    fftplan = fftw3.Plan(tarray,farray,'forward')
    ifftplan = fftw3.Plan(farray,tarray,'backward')
    farray[:] = 0
    tarray[:] = 0
    tarray += numpy.exp(-t**2/0.5)
    dispersion = numpy.exp(-1.j*h*beta*f)
    ti = time.time()
    for i in xrange(repeats):
        fftplan()
        farray *= dispersion/N
        ifftplan()
    to = time.time()-ti
    return fftshift(t),fftshift(tarray),fftshift(f),fftshift(farray), to


def numpy_propagation(N,repeats):
    t = numpy.linspace(-5,5,N)
    dt = t[1]-t[0]
    f = numpy.linspace(-1/dt/2.,1/dt/2.,N)
    f = fftshift(f)
    t = fftshift(t)
    tarray = numpy.exp(-t**2/0.5)
    farray = numpy.zeros(tarray.shape,complex)
    dispersion = numpy.exp(-1.j*h*beta*f)
    ti = time.time()
    for i in xrange(repeats):
        farray = fft(tarray)
        farray *= dispersion
        tarray = ifft(farray)
    to = time.time()-ti
    return fftshift(t),fftshift(tarray),fftshift(f),fftshift(farray),to


def scipy_propagation(N,repeats):
    t = numpy.linspace(-5,5,N)
    dt = t[1]-t[0]
    f = numpy.linspace(-1/dt/2.,1/dt/2.,N)
    f = fftshift(f)
    t = fftshift(t)
    tarray = numpy.exp(-t**2/0.5)
    farray = numpy.zeros(tarray.shape,complex)
    dispersion = numpy.exp(-1.j*h*beta*f)
    ti = time.time()
    for i in xrange(repeats):
        farray = sfft(tarray)
        farray *= dispersion
        tarray = sifft(tarray)
    to = time.time()-ti
    return fftshift(t),fftshift(tarray),fftshift(f),fftshift(farray),to




