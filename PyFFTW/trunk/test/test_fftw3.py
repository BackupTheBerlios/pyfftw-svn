import unittest
import fftw3
import numpy

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


if __name__ == '__main__': unittest.main()


