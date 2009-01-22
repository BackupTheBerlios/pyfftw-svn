import numpy as np
import ctypes
from lib import lib, _typelist


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

def create_AlignedArray(shape, dtype=complex):
    return AlignedArray(shape=shape,dtype=dtype)

def execute(plan):
    """Execute fftw-plan, i.e. perform Fourier transform on the arrays given
    when the plan was created"""
    lib.fftw_execute(plan)

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

def destroy_plan(plan):
    """Delete the given plan"""
    if isinstance(plan,Plan):
        del plan
    else:
        lib.fftw_destroy_plan(plan)

def select(inarray,outarray):
    """From a given input and output np array select the appropriate
    fftw3 plan to create.""" 
    if inarray.shape != outarray.shape:
        if inarray.dtype == outarray.dtype:
            raise TypeError, "Input array and output array must have the same "\
                             "shape if they have the same dtype"
        elif inarray.dtype == complex and outarray.dtype == float:
            inshape = list(outarray.shape)
            inshape[-1] = inshape[-1]/2 + 1
            if inarray.shape != tuple(inshape):
                raise TypeError, "For complex to real transforms the complex "\
                                 "array must be of shape (n1 x n2 x...x "\
                                 "(n-1)/2 +1"
        elif inarray.dtype == float and outarray.dtype == complex:
            outshape = list(inarray.shape)
            outshape[-1] = outshape[-1]/2 + 1
            if outarray.shape != tuple(outshape):
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
    np array and the direction and flags integers"""
    func, name, types = select(inarray,outarray)
    #this is necessary because the r2c and c2r transforms always use the
    #shape of the larger array (the real one)
    if np.prod(inarray.shape) < np.prod(outarray.shape):
        shape = outarray.shape
    else:
        shape = inarray.shape

    if len(types) < 3:
        plan = func(len(shape),
                    np.asarray(shape, dtype=int),
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
    np array and the realtype and flags integers"""
    func, name, types = select(inarray,outarray)

    if len(types) < 3:
        plan = func(len(inarray.shape), np.asarray(inarray.shape,dtype=int),\
             inarray, outarray, np.asarray(realtype), flags)
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
    np array and the direction and flags integers"""
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
            self.N = np.asarray(shape, dtype=int)

        elif len(shape) > 1:
            self.ndim = len(shape)
            self.N = np.asarray(shape, dtype=int)
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
        self.inarray = inarray
        self.outarray = outarray

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

class AlignedArray(np.ndarray):
    def __new__(cls, shape, dtype=complex):
        tmp = np.zeros(shape,dtype=dtype)
        p = lib.fftw_malloc(tmp.nbytes)
        b = (ctypes.c_byte*tmp.nbytes)(p)
        obj = np.ndarray.__new__(cls,shape=shape,buffer=b,dtype=dtype)
        del tmp,b
        obj.c_data = p
        return obj

    def __del__(self):
        if hasattr(self, 'c_data'):
            lib.fftw_free(self.c_data)
        else:
            pass