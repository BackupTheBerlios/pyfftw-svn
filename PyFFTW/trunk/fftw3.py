import numpy
import ctypes
#import os

#__path = os.path.dirname('__file__')
__librarypath = '/usr/lib/'
lib = numpy.ctypeslib.load_library('libfftw3.so', __librarypath)

from wisdom import export_wisdom_to_file, export_wisdom_to_string,\
        import_wisdom_from_string, import_wisdom_from_file, \
        import_system_wisdom, forget_wisdom

fftw_flags = {'measure':0,
              'destroy input': 1,
              'unaligned': 2,
              'conserve memory':4,
              'exhaustive':8,
              'preserve input': 16,
              'patient': 32,
              'estimate': 64}

realfft_type = {'halfcomplex r2c':0,
                'halfcomplex c2r':1,
                'discrete hartley':2,
                'realeven 00':3,
                'realeven 01':4,
                'realeven 10':5,
                'realeven 11':6,
                'realodd 00':7,
                'realodd 01':8,
                'realodd 10':9,
                'realodd 11':10}


fft_direction = {'forward' : -1, 'backward': 1}
lib = numpy.ctypeslib.load_library('libfftw3.so', __librarypath)

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

# set the return and argument types on the plan functions
for name, types in __typedict_plans:
    val = getattr(lib, name)
    val.restype = ctypes.c_void_p
    if types[0] == complex or types[1] == complex:
        if len(types) >2:
            val.argtypes = [ctypes.c_int for i in range(types[2])] +\
                           [numpy.ctypeslib.ndpointer(dtype=types[0],
                                                      ndim=types[2],
                                                      flags='contiguous, '\
                                                            'writeable, '\
                                                            'aligned'),
                            numpy.ctypeslib.ndpointer(dtype=types[1],
                                                      ndim=types[2],
                                                      flags='contiguous, '\
                                                            'writeable, '\
                                                            'aligned'),

                            ctypes.c_int, ctypes.c_uint]
        else:
            val.argtypes = [ctypes.c_int,
                            numpy.ctypeslib.ndpointer(dtype=int, ndim=1,
                                                      flags='contiguous, '\
                                                            'aligned'),
                            numpy.ctypeslib.ndpointer(dtype=types[0],
                                                      flags='contiguous, '\
                                                            'writeable, '\
                                                            'aligned'),
                            numpy.ctypeslib.ndpointer(dtype=types[1],
                                                      flags='contiguous, '\
                                                            'writeable,'\
                                                            'aligned'),
                            ctypes.c_int, ctypes.c_uint]
    else:
        if len(types) > 2:
            val.argtypes = [ctypes.c_int for i in range(types[2])] +\
                           [numpy.ctypeslib.ndpointer(dtype=types[0],
                                                      ndim=types[2],
                                                      flags='contiguous, '\
                                                            'writeable, '\
                                                            'aligned'),
                            numpy.ctypeslib.ndpointer(dtype=types[1],
                                                      ndim=types[2],
                                                      flags='contiguous,'\
                                                            'writeable, '\
                                                            'aligned')] +\
                            [ctypes.c_int for i in range(types[2])] +\
                            [ctypes.c_uint]
        else:
            val.argtypes = [ctypes.c_int,
                            numpy.ctypeslib.ndpointer(dtype=int,
                                                      ndim=1,
                                                      flags='contiguous, '\
                                                            'aligned'),
                            numpy.ctypeslib.ndpointer(dtype=types[0],
                                                      flags='contiguous, '\
                                                            'writeable, '\
                                                            'aligned'),
                            numpy.ctypeslib.ndpointer(dtype=types[1],
                                                      flags='contiguous, '\
                                                            'writeable, '\
                                                            'aligned'),
                            numpy.ctypeslib.ndpointer(dtype=int, ndim=1,
                                                      flags='contiguous, '\
                                                            'aligned'),
                            ctypes.c_uint]


#malloc and free
lib.fftw_malloc.restype = ctypes.c_void_p
lib.fftw_malloc.argtypes = [ctypes.c_int]
lib.fftw_free.restype = None
lib.fftw_free.argtypes = [ctypes.c_void_p]

def create_fftw_array(shape, dtype='complex'):
    return fftw_array(shape=shape,dtype=dtype)

lib.fftw_execute.restype = None
lib.fftw_execute.argtypes = [ctypes.c_void_p]
def execute(plan):
    """Execute fftw-plan, i.e. perform Fourier transform on the arrays given
    when the plan was created"""
    lib.fftw_execute(plan)

lib.fftw_execute_dft.restype = None
lib.fftw_execute_dft.argtypes = [ctypes.c_void_p,
                        numpy.ctypeslib.ndpointer(flags='aligned, contiguous, '\
                                                        'writeable'),\
                        numpy.ctypeslib.ndpointer(flags='aligned, contiguous, '\
                                                        'writeable')]
def guru_execute_dft(plan, inarray, outarray):
        """Guru interface: perform Fourier transform on two arrays,
        outarray=fft(inarray) using the given plan. Important: This function
        does not perform any checks on the array shape and alignment for
        performance reasons. It is therefore crucial to only provide arrays
        with the same shape, dtype and alignment as the arrays used for planning,
        failure to do so can lead to unexpected behaviour and even python
        segfaulting.
        """
        lib.fftw_execute_dft(plan, inarray, outarray)

lib.fftw_destroy_plan.restype = None
lib.fftw_destroy_plan.argtypes = [ctypes.c_void_p]
def destroy_plan(plan):
    """Delete the given plan"""
    if isinstance(plan,Plan):
        del plan
    else:
        lib.fftw_destroy_plan(plan)

def select(inarray,outarray):
    """From a given input and output numpy array select the appropriate
    fftw3 plan to create.""" 
    if inarray.shape != outarray.shape:
        if inarray.dtype = outarray.dtype:
            raise TypeError, "Input array and output array must have the same "\
                             "shape if they have the same dtype"
        elif inarray.dtype = complex and outarray.dtype = float:
            inshape = list(outarray.shape)
            inshape[-1] = inshape[-1]/2 + 1
            if not inarray.shape is tuple(inshape):
                raise TypeError, "For complex to real transforms the complex "\
                                 "array must be of shape (n1 x n2 x...x "\
                                 "(n-1)/2 +1"
         elif inarray.dtype = float and outarray.dtype = complex:
            outshape = list(inarray.shape)
            outshape[-1] = outshape[-1]/2 + 1
            if not inarray.shape is tuple(inshape):
                raise TypeError, "For real to complex transforms the complex "\
                                 "array must be of shape (n1 x n2 x...x "\
                                 "(n-1)/2 +1"
    if inarray.dtype != float and inarray.dtype != complex:
        raise TypeError, "Input array has to be either floating point or"\
                         " complex"
    elif outarray.dtype != float and outarray.dtype != complex:
        raise TypeError, "Output array has to be either floating point "\
                         "or complex"
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

def _create_complex_plan(inarray, outarray, direction, flags):
    """Internal function to create complex fft plan given an input and output
    numpy array and the direction and flags integers"""
    func, name, types = select(inarray,outarray)
    #this is necessary because the r2c and c2r transforms always use the
    #shape of the larger array (the real one)
    if numpy.prod(inarray.shape) < numpy.prod(outarray.shape):
        shape = outarray.shape
    else:
        shape = inarray.shape

    if len(types) < 3:
        plan = func(len(shape),
                    numpy.asarray(shape, dtype=int),
                    inarray, outarray, direction, flags)
        if plan == None:
            raise Exception, "Error creating fftw plan %s for the given "\
                             "parameters" %name
        else:
            return plan, name
    elif types[2] == 1:
        plan = func(shape[0], inarray, outarray, direction, flags)
        if plan == None:
            raise Exception, "Error creating fftw plan %s for the given "\
                             "parameters" %name
        else:
            return plan, name
    elif types[2] == 2:
        plan = func(shape[0], shape[1], inarray, outarray,\
                    direction, flags)
        if plan == None:
            raise Exception, "Error creating fftw plan %s for the given "\
                             "parameters" %name
        else:
            return plan, name
    elif types[2] == 3:
        plan = func(shape[0], shape[1], shape[2],\
                    inarray, outarray, direction, flags)
        if plan == None:
            raise Exception, "Error creating fftw plan %s for the given "\
                             "parameters" %name
        else:
            return plan, name
    else:
        raise ValueError, 'the dimensions are not correct'

def _create_real_plan(inarray, outarray, realtype, flags):
    """Internal function to create real fft plan given an input and output 
    numpy array and the realtype and flags integers"""
    func, name, types = select(inarray,outarray)

    if len(types) < 3:
        plan = func(len(inarray.shape), numpy.asarray(inarray.shape,dtype=int),\
             inarray, outarray, numpy.asarray(realtype), flags)
        if plan == None:
            raise Exception, "Error creating fftw plan %s for the given "\
                             "parameters" %name
        else:
            return plan, name
    elif types[2] == 1:
        plan = func(inarray.shape[0], inarray, outarray, realtype[0], flags)
        if plan == None:
            raise Exception, "Error creating fftw plan %s for the given "\
                             "parameters" %name
        else:
            return plan, name
    elif types[2] == 2:
        plan = func(inarray.shape[0], inarray.shape[1], inarray, outarray,\
                    realtype[0], realtype[1], flags)
        if plan == None:
            raise Exception, "Error creating fftw plan %s for the given "\
                             "parameters" %name
        else:
            return plan, name
    elif types[2] == 3:
        plan = func(inarray.shape[0], inarray.shape[1],inarray.shape[2], \
                    inarray, outarray, realtype[0], realtype[1], \
                    realtype[2], flags)
        if plan == None:
            raise Exception, "Error creating fftw plan %s for the given "\
                             "parameters" %name
        else:
            return plan, name
    else:
        raise ValueError, 'the dimensions are not correct'

def _create_plan(inarray, outarray, direction='forward', flags=['estimate'],
                realtypes=None):
    """Internal function to create a complex fft plan given an input and output
    numpy array and the direction and flags integers"""
    if realtypes != None:
        return _create_real_plan(inarray,outarray,\
                [realfft_type[r] for r in realtypes], _cal_flag_value(flags))
    else:
        return _create_complex_plan(inarray,outarray,\
                                     fft_direction[direction],
                                     _cal_flag_value(flags))

def _cal_flag_value(flags):
    """Calculate the integer flag value from a list of string flags"""
    ret = 0
    for f in flags:
        ret += fftw_flags[f]
    return ret

class Plan(object):
    """Object representing a fftw plan used to execute Fourier transforms in
    fftw"""
    def __init__(self, inarray=None, outarray=None, direction='forward',
                 flags=['estimate'], realtypes=None, create_plan=True):
        """Initialize the fftw plan. 
        Parameters:
            inarray     --  array to be transformed (default=None)
            outarray    --  array to contain the Fourier transform
                            (default=None)
            If one of the arrays is None, the fft is considered to be
            an inplace transform.

            direction   --  direction of the Fourier transform, forward
                            or backward (default='forward')
            flags       --  list of fftw-flags to be used in planning
                            (default=['estimate'])
            realtypes   --  list of fft-types for real-to-real ffts, this
                            needs to be given if both input and output 
                            arrays are real (default=None)
            create_plan --  weather to actually create the plan (default=True)
            """

        self.flags = flags
        self.direction = direction
        self.realtypes = realtypes
        if create_plan:
            if inarray == None and outarray  == None:
                raise 'Need at least one array to create the plan'
            elif inarray == None:
                self.create_plan(inarray,inarray)
            elif outarray == None:
                self.create_plan(outarray,outarray)
            else:
                self.create_plan(inarray,outarray)

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

    def create_plan(self, inarray, outarray):
        """Create the actual fftw-plan from inarray and outarray"""
        self.plan, self.type_plan = _create_plan(inarray,outarray,
                                                 direction=self.direction,
                                                 flags=self.flags,
                                                 realtypes=self.realtypes)
        self.shape = inarray.shape

    def _get_parameter(self):
        return self.plan
    _as_parameter_ = property(_get_parameter)

    def __call__(self):
        """Perform the Fourier transform outarray = fft(inarray) for
        the arrays given at plan creation"""
        self.execute()

    def execute(self):
        """Execute the fftw plan, i.e. perform the FFT outarray = fft(inarray)
        for the arrays given at plan creation"""
        execute(self)

    def __del__(self):
        destroy_plan(self)

    def guru_execute_dft(self,inarray,outarray):
        """Guru interface: perform Fourier transform on two given arrays,
        outarray=fft(inarray). Important: This method does not perform any
        checks on the array shape and alignment for performance reasons. It is
        therefore crucial to only provide arrays with the same shape, dtype and
        alignment as the arrays used for planning, failure to do so can lead to
        unexpected behaviour and even python segfaulting
        """
        guru_execute_dft(self,inarray,outarray)


class fftw_array(numpy.ndarray):
    #plan=None
    def __new__(cls, shape, dtype=complex, plan=None):
        tmp = numpy.zeros(shape,dtype=dtype)
        #nbytes = tmp.nbytes
        p = lib.fftw_malloc(tmp.nbytes)
        b = (ctypes.c_byte*tmp.nbytes)(p)
        obj = numpy.ndarray.__new__(cls,shape=shape,buffer=b,dtype=dtype)
        del tmp, b
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
    
