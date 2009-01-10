import numpy
import ctypes
import os

#__path = os.path.dirname('__file__')
__librarypath = '/usr/lib/'
fftwflags = {'measure':0, 'destroy input': 1, 'unaligned': 2,
               'conserve memory':4, 'exhaustive':8, 'preserve input': 16,
               'patient': 32, 'estimate': 64}
realffts = {'halfcomplex r2c':0, 'halfcomplex c2r':1, 'discrete hartley' :2,
              'realeven 00':3, 'realeven 01':4, 'realeven 10': 5
              'realeven 11':6, 'realodd 00':7, 'realodd 01':8,
              'realodd 10':9, 'realodd 11':10}

fft_direction = {'forward' : -1, 'backward': 1}
lib = numpy.ctypeslib.load_library('libfftw3.so',__librarypath)

__typedict_plans =    [('fftw_plan_dft_1d', (complex, complex, 1)),
                       ('fftw_plan_dft_2d', (complex, complex, 2)),
                       ('fftw_plan_dft_3d', (complex, complex, 3)),
                       ('fftw_plan_dft', (complex, complex)),
                       ('fftw_plan_dft_c2r_1d', (complex, float, 1)),
                       ('fftw_plan_dft_c2r_2d', (complex, float, 2)),
                       ('fftw_plan_dft_c2r_3d', (complex, float, 3)),
                       ('fftw_plan_dft_c2r', (complex, float)),
                       ('fftw_plan_dft_r2c_1d', (float, complex, 1)),
                       ('fftw_plan_dft_r2c_2d', (float, complex, 2)),
                       ('fftw_plan_dft_r2c_3d', (float, complex, 3)),
                       ('fftw_plan_dft_r2c', (float, complex)),
                       ('fftw_plan_dft_r2r_1d', (float, float, 1)),
                       ('fftw_plan_dft_r2r_2d', (float, float, 2)),
                       ('fftw_plan_dft_r2r_3d', (float, float, 3)),
                       ('fftw_plan_dft_r2r', (float, float))]


for name, types in __typedict_plans:
    val = getattr(lib, name)
    val.restype = ctypes.c_void_p
    if types[0] or types[1] == complex:
        if len(types) >2:
            val.argtypes = [ctypes.c_int for i in range(types[2])] + \
                           [numpy.ctypeslib.ndpointer(dtype=types[0],\
                                ndim=types[2], flags='contiguous, writeable'),\
                            numpy.ctypeslib.ndpointer(dtype=types[1],\
                                ndim=types[2], flags='contiguous,writeable'),\
                            ctypes.c_uint]
        else:
            val.argtypes = [ctypes.c_int, numpy.ctypeslib.ndpointer(dtype=int,\
                                ndim=1,flags='contiguous'),\
                             numpy.ctypeslib.ndpointer(dtype=types[0],\
                                flags='contiguous, writeable'), \
                             numpy.ctypeslib.ndpointer(dtype=types[1], \
                                flags='contiguous,writeable'),\
                             ctypes.c_uint]
    else:
        if len(types) > 2:
            val.argtypes = [ctypes.c_int for i in range(types[2])] + \
                            [numpy.ctypeslib.ndpointer(dtype=types[0],\
                                ndim=types[2], flags='contiguous, writeable'),\
                            numpy.ctypeslib.ndpointer(dtype=types[1],\
                                ndim=types[2], flags='contiguous,writeable')]+\
                            [ctypes.c_int for i in range(types[2])] +\
                            [ctypes.c_int]
        else:
            val.argtypes = [ctypes.c_int, numpy.ctypeslib.ndpointer(dtype=int,\
                                ndim=1,flags='contiguous'),\
                             numpy.ctypeslib.ndpointer(dtype=types[0],\
                                flags='contiguous, writeable'), \
                             numpy.ctypeslib.ndpointer(dtype=types[1], \
                                flags='contiguous,writeable'),\
                             numpy.ctypeslib.ndpointer(dtype=int, ndim=1,\
                                                       flags='contiguous'),\
                             ctypes.c_uint]


def select(inarray,outarray):
    if inarray.shape != outarray.shape:
        raise TypeError, 'Input array and output array must have the same shape'
    elif inarray.dtype == outarray.dtype == float:
        raise TypeError, 'At least one of the arrays has to be complex'
    i = 0
    while(i < len(__typedict_plans)):
        name, types = __typedict_plans[i]
        if inarray.dtype != types[0]:
            i += 8
            continue
        elif outarray.dtype != types[1]:
            i += 4
            continue
        elif i in [3,7,11]:
            return getattr(lib, name), name, types
        elif len(inarray.shape) != types[2]:
            i += 1
            continue
        else:
            return getattr(lib, name), name, types

#def __create_plan_multi_dim(inarray,outarray, direction='forward', flags='estimate'):
    #func, name, types = select(inarray,outarray)
    #intflags = 0
    #for flag in flags:
        #intflags +=


    #if len(types) > 3:
        #func(len(inarray.shape,


class Plan(object):
    def __init__(self, inarray=None, outarray=None, direction='forward', flags=['estimate'], create_plan=True):
        self.__flags = flags
        self.direction = __fftw_direction['direction']
        if create_plan:
            if not inarray or not outarray:
                raise 

    def __set_shape(self,shape):
        if len(shape)==1:
            self.ndim = 1
            self.N = array([shape])
        elif len(shape) > 1:
            self.ndim = len(shape)
            self.N = shape
        else:
            raise ValueError, 'shape must be at least one dimensional'
    
    def __get_shape(self):
        return self.N
    shape = property(__get_shape, __set_shape)

    def __get_flags(self):
        ret = 0
        for f in self.__flags:
            ret += __fftwflags[f]
        return ret

    def __set_flags(self):
        self.__flags = flags
    flags = property(__get_flags,__set_flags)

    def __create_plan(self, inarray, outarray):
        func, name, types = select(inarray, outarray)
        self.fftype = name
        if ,

