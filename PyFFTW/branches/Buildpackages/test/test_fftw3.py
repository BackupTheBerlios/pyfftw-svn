import sys
sys.path.append('../build/lib')
import unittest
import fftw3
import fftw3f
import fftw3l
from numpy import fft,ifft,fftshift
import numpy as np
from scipy.fftpack import fft as sfft, ifft as sifft
import propagation
import os

h = 0.01
beta = 1
N = 512
libs = [fftw3, fftw3f, fftw3l]


def fftw_propagation_aligned(N,repeats, lib, dtype):
    t = np.linspace(-5,5,N)
    dt = t[1]-t[0]
    f = np.linspace(-1/dt/2.,1/dt/2.,N)
    f = fftshift(f)
    t = fftshift(t)
    farray = lib.AlignedArray(f.shape,dtype=dtype)
    tarray = lib.fftw_array(t.shape,dtype=dtype)
    fftplan = lib.Plan(tarray,farray,'forward')
    ifftplan = lib.Plan(farray,tarray,'backward')
    farray[:] = 0
    tarray[:] = 0
    tarray += np.exp(-t**2/0.5)
    dispersion = np.exp(-1.j*h*beta*f)
    ti = time.time()
    for i in xrange(repeats):
        fftplan()
        farray *= dispersion/N
        ifftplan()
    to = time.time()-ti
    return fftshift(t),fftshift(tarray),fftshift(f),fftshift(farray), to

def fftw_propagation(N,repeats,lib, dtype):
    t = np.linspace(-5,5,N)
    dt = t[1]-t[0]
    f = np.linspace(-1/dt/2.,1/dt/2.,N)
    f = fftshift(f)
    t = fftshift(t)
    farray = zeros(f.shape,dtype=dtype)
    tarray = zeros(t.shape,dtype=dtype)
    fftplan = lib.Plan(tarray,farray,'forward')
    ifftplan = lib.Plan(farray,tarray,'backward')
    farray[:] = 0
    tarray[:] = 0
    tarray += np.exp(-t**2/0.5)
    dispersion = np.exp(-1.j*h*beta*f)
    ti = time.time()
    for i in xrange(repeats):
        fftplan()
        farray *= dispersion/N
        ifftplan()
    to = time.time()-ti
    return fftshift(t),fftshift(tarray),fftshift(f),fftshift(farray), to


def np_propagation(N,repeats,dtype):
    t = np.linspace(-5,5,N)
    dt = t[1]-t[0]
    f = np.linspace(-1/dt/2.,1/dt/2.,N)
    f = fftshift(f)
    t = fftshift(t)
    tarray = np.zeros(tarray.shape,dtype)
    tarray += np.exp(-t**2/0.5)
    farray = np.zeros(tarray.shape,dtype)
    dispersion = np.zeros(tarray.shape,dtype)
    dispersion += np.exp(-1.j*h*beta*f)
    ti = time.time()
    for i in xrange(repeats):
        farray = fft(tarray)
        farray *= dispersion
        tarray = ifft(farray)
    to = time.time()-ti
    return fftshift(t),fftshift(tarray),fftshift(f),fftshift(farray),to


def scipy_propagation(N,repeats, dtype):
    t = np.linspace(-5,5,N)
    dt = t[1]-t[0]
    f = np.linspace(-1/dt/2.,1/dt/2.,N)
    f = fftshift(f)
    t = fftshift(t)
    tarray = np.zeros(tarray.shape,dtype)
    tarray += np.exp(-t**2/0.5)
    farray = np.zeros(tarray.shape,dtype)
    dispersion = np.zeros(tarray.shape,dtype)
    dispersion += np.exp(-1.j*h*beta*f)
    ti = time.time()
    for i in xrange(repeats):
        farray = sfft(tarray)
        farray *= dispersion
        tarray = sifft(tarray)
    to = time.time()-ti
    return fftshift(t),fftshift(tarray),fftshift(f),fftshift(farray),to


class ProductTestCase(unittest.TestCase):

    def testSelect(self):
        for lib in libs:
            for plan in lib.lib._typelist:
                if len(plan[1])>2:
                    plantype,(intype, outtype,length) = plan
                    shape = np.random.randint(2,5,length)
                    inputa = np.zeros(shape=shape, dtype=intype)
                    outputa = np.zeros(shape=shape, dtype=outtype)
                else:
                    plantype, (intype,outtype) = plan
                    shape = np.random.randint(2,5,np.random.randint(4,8))
                    length = len(shape)
                    inputa = np.zeros(shape=shape, dtype=intype)
                    outputa = np.zeros(shape=shape, dtype=outtype)
                func, name, types = fftw3.select(inputa,outputa)
                self.failUnless(name == plantype, "%s: select returned a wrong type for input array type=%s, output array type=%s, and dimension = %d" %(lib, inputa.dtype, outputa.dtype, length))
                self.failUnless(func is getattr(lib.lib, plantype), "%s: wrong library function for type %s" %(lib,plantype))

  #  def testWisdom(self):
        ##for lib in libs
        #fftw3.forget_wisdom()
        #inputa = fftw3.fftw_array(1024,complex)
        #outputa = fftw3.fftw_array(1024,complex)
        #plan = fftw3.Plan(inputa,outputa,flags=['patient'])
        #soriginal = fftw3.export_wisdom_to_string()
        #fftw3.import_wisdom_from_string(soriginal)
        #fftw3.export_wisdom_to_file('test.wisdom')
        #fftw3.forget_wisdom()
        #fftw3.import_wisdom_from_file('test.wisdom')
        #os.remove('test.wisdom')
        #del inputa
        #del outputa
        
    #def testPropagation(self):
        #Ns = [2**i for i in range(10,15)]
        #repeats = 2000
        #epsilon = 1e-3
        #times = []
        #for Nn in Ns:
            #t,A,f,B, ti = fftw_propagation_aligned(Nn,repeats)
            #ft,fA,ff,fB, fti = fftw_propagation_aligned(Nn,repeats)
            #nt,nA, nf, nB, nti = np_propagation(Nn,repeats)
            #st,sA, sf, sB, sti = scipy_propagation(Nn,repeats)
            #times.append((fti, ti,nti, sti))
            #self.failUnless(sum(abs(A)**2-abs(nA)**2)< epsilon, "Propagation of fftw3 and numpy gives different results")
        #print "Benchmark:"
        #print "   N   fftw3 fftw3_aligned   numpy   scipy"
        #for i in range(len(Ns)):
            #print "%5d  %5.2f  %5.2f  %5.2f   %5.2f" %(Ns[i],times[i][0], times[i][1], times[i][2], times[i][3])


if __name__ == '__main__': unittest.main()
