import ctypes
from ctypes import pythonapi
from numpy import ctypeslib

__librarypath = '/usr/lib/'
lib = ctypeslib.load_library('libfftw3.so', __librarypath)

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
                           [ctypeslib.ndpointer(dtype=types[0],
                                                      ndim=types[2],
                                                      flags='contiguous, '\
                                                            'writeable, '\
                                                            'aligned'),
                            ctypeslib.ndpointer(dtype=types[1],
                                                      ndim=types[2],
                                                      flags='contiguous, '\
                                                            'writeable, '\
                                                            'aligned'),

                            ctypes.c_int, ctypes.c_uint]
        else:
            val.argtypes = [ctypes.c_int,
                            ctypeslib.ndpointer(dtype=int, ndim=1,
                                                      flags='contiguous, '\
                                                            'aligned'),
                            ctypeslib.ndpointer(dtype=types[0],
                                                      flags='contiguous, '\
                                                            'writeable, '\
                                                            'aligned'),
                            ctypeslib.ndpointer(dtype=types[1],
                                                      flags='contiguous, '\
                                                            'writeable,'\
                                                            'aligned'),
                            ctypes.c_int, ctypes.c_uint]
    else:
        if len(types) > 2:
            val.argtypes = [ctypes.c_int for i in range(types[2])] +\
                           [ctypeslib.ndpointer(dtype=types[0],
                                                      ndim=types[2],
                                                      flags='contiguous, '\
                                                            'writeable, '\
                                                            'aligned'),
                            ctypeslib.ndpointer(dtype=types[1],
                                                      ndim=types[2],
                                                      flags='contiguous,'\
                                                            'writeable, '\
                                                            'aligned')] +\
                            [ctypes.c_int for i in range(types[2])] +\
                            [ctypes.c_uint]
        else:
            val.argtypes = [ctypes.c_int,
                            ctypeslib.ndpointer(dtype=int,
                                                      ndim=1,
                                                      flags='contiguous, '\
                                                            'aligned'),
                            ctypeslib.ndpointer(dtype=types[0],
                                                      flags='contiguous, '\
                                                            'writeable, '\
                                                            'aligned'),
                            ctypeslib.ndpointer(dtype=types[1],
                                                      flags='contiguous, '\
                                                            'writeable, '\
                                                            'aligned'),
                            ctypeslib.ndpointer(dtype=int, ndim=1,
                                                      flags='contiguous, '\
                                                            'aligned'),
                            ctypes.c_uint]

#malloc and free
lib.fftw_malloc.restype = ctypes.c_void_p
lib.fftw_malloc.argtypes = [ctypes.c_int]
lib.fftw_free.restype = None
lib.fftw_free.argtypes = [ctypes.c_void_p]

#executing arrays
lib.fftw_execute.restype = None
lib.fftw_execute.argtypes = [ctypes.c_void_p]

#guru execution
lib.fftw_execute_dft.restype = None
lib.fftw_execute_dft.argtypes = [ctypes.c_void_p,
                        ctypeslib.ndpointer(flags='aligned, contiguous, '\
                                                        'writeable'),\
                        ctypeslib.ndpointer(flags='aligned, contiguous, '\
                                                        'writeable')]

#destroy plans
lib.fftw_destroy_plan.restype = None
lib.fftw_destroy_plan.argtypes = [ctypes.c_void_p]

#wisdom
_PyFile_AsFile = pythonapi.PyFile_AsFile
_PyFile_AsFile.argtypes = [ctypes.py_object]
_PyFile_AsFile.restype = ctypes.c_void_p

#export to file
lib.fftw_export_wisdom_to_file.argtypes = [ctypes.c_void_p]
lib.fftw_export_wisdom_to_file.restype = None

#export to string
lib.fftw_export_wisdom_to_string.argtypes = None
lib.fftw_export_wisdom_to_string.restype = ctypes.c_char_p

#import from file
lib.fftw_import_wisdom_from_file.argtypes = [ctypes.c_void_p]
lib.fftw_import_wisdom_from_file.restype = ctypes.c_int

#import from string
lib.fftw_import_wisdom_from_string.argtypes = [ctypes.c_char_p]
lib.fftw_import_wisdom_from_string.restype = ctypes.c_int

#import system wisdom
lib.fftw_import_system_wisdom.restype = ctypes.c_int
lib.fftw_import_system_wisdom.argtypes = None

#forget wisdom
lib.fftw_forget_wisdom.restype = None
lib.fftw_forget_wisdom.argtype = None
