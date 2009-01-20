import fftw3
import numpy
from numpy import testing


for i in xrange(1):
    #a = fftw3.fftw_array((2**16,))
    #b = fftw3.fftw_array((2**16,))
    a = numpy.zeros((2**16,))
    b = numpy.zeros((2**16,))
    p = fftw3.Plan(a,b)
    print testing.memusage()
    del a,b,p

