import unittest
import fftw3
import numpy
import propagation
import os
from subprocess import Popen, PIPE

N = 512
plans = fftw3.__typedict_plans

class ProductTestCase(unittest.TestCase):

    def testSelect(self):
        for plan in plans:
            if len(plan[1])>2:
                plantype,(intype, outtype,length) = plan
                shape = numpy.random.randint(2,5,length)
                inputa = numpy.zeros(shape=shape, dtype=intype)
                outputa = numpy.zeros(shape=shape, dtype=outtype)
            else:
                plantype, (intype,outtype) = plan
                shape = numpy.random.randint(2,5,numpy.random.randint(4,8))
                length = len(shape)
                inputa = numpy.zeros(shape=shape, dtype=intype)
                outputa = numpy.zeros(shape=shape, dtype=outtype)
            func, name, types = fftw3.select(inputa,outputa)
            self.failUnless(name == plantype, "select returned a wrong type for input array type=%s, output array type=%s, and dimension = %d" %(inputa.dtype, outputa.dtype, length))
            self.failUnless(func is getattr(fftw3.lib, plantype), "wrong library function for type %s" %plantype)

    def testWisdom(self):
        fftw3.forget_wisdom()
        inputa = fftw3.fftw_array(1024,complex)
        outputa = fftw3.fftw_array(1024,complex)
        plan = fftw3.Plan(inputa,outputa,flags=['patient'])
        soriginal = fftw3.export_wisdom_to_string()
        fftw3.import_wisdom_from_string(soriginal)
        fftw3.export_wisdom_to_file('test.wisdom')
        fftw3.forget_wisdom()
        fftw3.import_wisdom_from_file('test.wisdom')
        os.remove('test.wisdom')
        del inputa
        del outputa
        
    def testPropagation(self):
        Ns = [2**i for i in range(10,15)]
        repeats = 2000
        epsilon = 1e-3
        times = []
        for Nn in Ns:
            t,A,f,B, ti = propagation.fftw_propagation(Nn,repeats)
            nt,nA, nf, nB, nti = propagation.numpy_propagation(Nn,repeats)
            st,sA, sf, sB, sti = propagation.scipy_propagation(Nn,repeats)
            times.append((ti, nti, sti))
            self.failUnless(sum(abs(A)**2-abs(nA)**2)< epsilon, "Propagation of fftw3 and numpy gives different results")
        print "Benchmark:"
        print "   N   fftw3   numpy   scipy"
        for i in range(len(Ns)):
            print "%5d  %5.2f    %5.2f   %5.2f" %(Ns[i],times[i][0], times[i][1], times[i][2])


if __name__ == '__main__': unittest.main()
