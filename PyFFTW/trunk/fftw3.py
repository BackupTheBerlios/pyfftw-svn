import numpy
import ctypes
import os
from ctypes import pythonapi

#__path = os.path.dirname('__file__')
__librarypath = '/usr/lib/'
fftw_flags = {'measure':0, 'destroy input': 1, 'unaligned': 2,
               'conserve memory':4, 'exhaustive':8, 'preserve input': 16,
               'patient': 32, 'estimate': 64}
realfft_type = {'halfcomplex r2c':0, 'halfcomplex c2r':1, 'discrete hartley':2,
              'realeven 00':3, 'realeven 01':4, 'realeven 10':5,
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
                       ('fftw_plan_r2r_1d', (float, float, 1)),
                       ('fftw_plan_r2r_2d', (float, float, 2)),
                       ('fftw_plan_r2r_3d', (float, float, 3)),
                       ('fftw_plan_r2r', (float, float))]


for name, types in __typedict_plans:
    val = getattr(lib, name)
    val.restype = ctypes.c_void_p
    if types[0] == complex or types[1] == complex:
        if len(types) >2:
            val.argtypes = [ctypes.c_int for i in range(types[2])] + \
                           [numpy.ctypeslib.ndpointer(dtype=types[0],\
                                ndim=types[2], flags='contiguous, writeable'),\
                            numpy.ctypeslib.ndpointer(dtype=types[1],\
                                ndim=types[2], flags='contiguous,writeable'),\
                            ctypes.c_int, ctypes.c_uint]
        else:
            val.argtypes = [ctypes.c_int, numpy.ctypeslib.ndpointer(dtype=int,\
                                ndim=1,flags='contiguous'),\
                             numpy.ctypeslib.ndpointer(dtype=types[0],\
                                flags='contiguous, writeable'), \
                             numpy.ctypeslib.ndpointer(dtype=types[1], \
                                flags='contiguous,writeable'),\
                             ctypes.c_int, ctypes.c_uint]
    else:
        if len(types) > 2:
            val.argtypes = [ctypes.c_int for i in range(types[2])] + \
                            [numpy.ctypeslib.ndpointer(dtype=types[0],\
                                ndim=types[2], flags='contiguous, writeable'),\
                            numpy.ctypeslib.ndpointer(dtype=types[1],\
                                ndim=types[2], flags='contiguous,writeable')]+\
                            [ctypes.c_int for i in range(types[2])] +\
                            [ctypes.c_uint]
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


lib.fftw_malloc.restype = ctypes.c_void_p
lib.fftw_malloc.argtypes = [ctypes.c_int]
lib.fftw_free.restype = None
lib.fftw_free.argtypes = [ctypes.c_void_p]

_PyFile_AsFile = ctypes.pythonapi.PyFile_AsFile
_PyFile_AsFile.argtypes = [ctypes.py_object]
_PyFile_AsFile.restype = ctypes.c_void_p

lib.fftw_export_wisdom_to_file.argtypes = [ctypes.c_void_p]
lib.fftw_export_wisdom_to_file.restype = None

def export_wisdom_to_file(filename):
    fp = open(filename, 'a')
    c_fp = _PyFile_AsFile(fp)
    lib.fftw_export_wisdom_to_file(c_fp)
    fp.close()

lib.fftw_export_wisdom_to_string.argtypes = None
lib.fftw_export_wisdom_to_string.restype = ctypes.c_char_p
def export_wisdom_to_string():
    return lib.fftw_export_wisdom_to_string()

lib.fftw_import_wisdom_from_file.argtypes = [ctypes.c_void_p]
lib.fftw_import_wisdom_from_file.restype = ctypes.c_int
def import_wisdom_from_file(filename):
    fp = open(filename,'r')
    c_fp = _PyFile_AsFile(fp)
    if lib.fftw_import_wisdom_from_file(c_fp):
        pass
    else:
        raise IOError, "Could not read wisdom from file %s" %filename


lib.fftw_import_wisdom_from_string.argtypes = [ctypes.c_char_p]
lib.fftw_import_wisdom_from_string.restype = ctypes.c_int
def import_wisdom_from_string(wisdom):
    if lib.fftw_import_wisdom_from_string(wisdom):
        pass
    else:
        raise "Could not read wisdom from string: %s" %wisdom

lib.fftw_import_system_wisdom.restype = ctypes.c_int
lib.fftw_import_system_wisdom.argtypes = None
def import_system_wisdom():
    if lib.fftw_import_system_wisdom():
        pass
    else:
        raise IOError, "Could not read system wisdom. On GNU/Linux and Unix system wisdom is located in /etc/fftw/wisdom"

forget_wisdom = lib.fftw_forget_wisdom
forget_wisdom.restype = None
forget_wisdom.argtype = None

#def create_aligned_array(size, dtype='complex'):
#    tmp = numpy.zeros(1,dtype=dtype)
#    nbytes = tmp.nbytes
#    p = lib.fftw_malloc(size*nbytes)
#    return simdalignedarray(shape=size,buffer=(ctypes.c_byte*nbytes*size).from_address(p),dtype=dtype)

execute = lib.fftw_execute
execute.restype = None
execute.argtypes = [ctypes.c_void_p]

execute_dft = lib.fftw_execute_dft
execute_dft.restype = None
execute_dft.argtypes = [ctypes.c_void_p,\
                        numpy.ctypeslib.ndpointer(flags='contiguous, writeable'),\
                        numpy.ctypeslib.ndpointer(flags='contiguous,writeable')]

destroy_plan = lib.fftw_destroy_plan


def select(inarray,outarray):
    """From a given input and output numpy array select the appropriate fftw3 plan to create.""" 
    if inarray.shape != outarray.shape:
        raise TypeError, 'Input array and output array must have the same shape'
    elif inarray.dtype != float and inarray.dtype != complex:
        raise TypeError, "Input array has to be either floating point or complex"
    elif outarray.dtype != float and outarray.dtype != complex:
        raise TypeError, "Output array has to be either floating point or complex"
    i = 0
    while(i < len(__typedict_plans)):
        name, types = __typedict_plans[i]
        if inarray.dtype != types[0]:
            i += 8
            continue
        elif outarray.dtype != types[1]:
            i += 4
            continue
        elif i in [3,7,11,15]:
            return getattr(lib, name), name, types
        elif len(inarray.shape) != types[2]:
            i += 1
            continue
        else:
            return getattr(lib, name), name, types

def __create_complex_plan(inarray,outarray,direction,flags):
    """Internal function to create complex fft plan given an input and output 
    numpy array and the direction and flags integers"""
    func, name, types = select(inarray,outarray)

    if len(types) < 3:
        return func(len(inarray.shape), numpy.asarray(inarray.shape,dtype=int),\
             inarray, outarray, direction, flags), name
    elif types[2] == 1:
        return func(inarray.shape[0], inarray, outarray, direction, flags),name
    elif types[2] == 2:
        return func(inarray.shape[0], inarray.shape[1], inarray, outarray,\
                    direction, flags), name
    elif types[2] == 3:
        return func(inarray.shape[0], inarray.shape[1], inarray.shape[2],\
                    inarray, outarray, direction, flags), name
    else:
        raise ValueError, 'the dimensions are not correct'

def __create_real_plan(inarray,outarray,realtype,flags):
    """Internal function to create real fft plan given an input and output 
    numpy array and the realtype and flags integers"""
    func, name, types = select(inarray,outarray)
    print name

    if len(types) < 3:
        return func(len(inarray.shape), numpy.asarray(inarray.shape,dtype=int),\
             inarray, outarray, numpy.asarray(realtype), flags), name
    elif types[2] == 1:
        return func(inarray.shape[0], inarray, outarray, realtype[0], flags), name
    elif types[2] == 2:
        return func(inarray.shape[0], inarray.shape[1], inarray, outarray,\
                    realtype[0], realtype[1], flags), name
    elif types[2] == 3:
        return func(inarray.shape[0], inarray.shape[1],inarray.shape[2], inarray, outarray,\
                    realtype[0], realtype[1], realtype[2], flags), name
    else:
        raise ValueError, 'the dimensions are not correct'

def _create_plan(inarray, outarray, direction='forward', flags=['estimate'],
                realtypes=None):
    if realtypes != None:
        return __create_real_plan(inarray,outarray,\
                [realfft_type[r] for r in realtypes], __cal_flag_value(flags))
    else:
        return __create_complex_plan(inarray,outarray,\
                fft_direction[direction], __cal_flag_value(flags))


def __cal_flag_value(flags):
    ret = 0
    for f in flags:
        ret += fftw_flags[f]
    return ret

class Plan(object):
    def __init__(self, inarray=None, outarray=None, direction='forward', flags=['estimate'], realtypes=None, create_plan=True):
        self.flags = flags
        self.direction = direction
        self.realtypes = realtypes
        if create_plan:
            if inarray == None and outarray  == None:
                raise 'Need at least one array to create the plan'
            elif inarray == None:
                self.__create_plan(inarray,inarray)
            elif outarray == None:
                self.__create_plan(outarray,outarray)
            else:
                self.__create_plan(inarray,outarray)

    def __set_shape(self,shape):
        if len(shape)==1:
            self.ndim = 1
            self.N = numpy.asarray(shape, dtype=int)
        elif len(shape) > 1:
            self.ndim = len(shape)
            self.N = numpy.asarray(shape, dtype=int)
        else:
            raise ValueError, 'shape must be at least one dimensional'
    
    def __get_shape(self):
        return self.N
    shape = property(__get_shape, __set_shape)

    def __create_plan(self, inarray, outarray):
        self.plan, self.type_plan = _create_plan(inarray,outarray, direction=self.direction, flags=self.flags,realtypes=self.realtypes)
        self.shape = inarray.shape

    def _get_parameter(self):
        return self.plan
    _as_parameter_ = property(_get_parameter)

    def __call__(self):
        self.execute()

    def execute(self):
        execute(self)

    def __del__(self):
        destroy_plan(self)
    
    def execute_dft(self,inarray,outarray):
        execute_dft(self,inarray,outarray)

class simdalignedarray(numpy.ndarray):
    #plan=None
    def __new__(cls, shape, dtype=complex, plan=None):
        #try:
            #length = sum(shape)
        #except:
            #length = shape
        tmp = numpy.zeros(shape,dtype=dtype)
        #nbytes = tmp.nbytes
        p = lib.fftw_malloc(tmp.nbytes)
        b = (ctypes.c_byte*tmp.nbytes)(p)
        obj = numpy.ndarray.__new__(cls,shape=shape,buffer=b,dtype=dtype)
        #obj.plan = plan
        return obj

    def __del__(self):
        if self.base == None:
           lib.fftw_free(self)
        else:
            pass
        #if self.plan is not None:
        #    destroy_plan(self.plan)
        #lib.fftw_free(self.ctypes.data)
    
