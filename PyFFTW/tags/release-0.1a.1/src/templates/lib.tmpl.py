#   This file is part of PyFFTW.
#
#    Copyright (C) 2009 Jochen Schroeder
#    Email: jschrod@berlios.de
#
#    PyFFTW is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    PyFFTW is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PyFFTW.  If not, see <http://www.gnu.org/licenses/>.

import ctypes
from ctypes import pythonapi, util, py_object
from numpy import ctypeslib, typeDict


lib = ctypes.cdll.LoadLibrary(util.find_library('$library$'))

_typelist =    [('$libname$_plan_dft_1d', (typeDict['$complex$'], typeDict['$complex$'], 1)),
                       ('$libname$_plan_dft_2d', (typeDict['$complex$'], typeDict['$complex$'], 2)),
                       ('$libname$_plan_dft_3d', (typeDict['$complex$'], typeDict['$complex$'], 3)),
                       ('$libname$_plan_dft', (typeDict['$complex$'], typeDict['$complex$'])),
                       ('$libname$_plan_dft_c2r_1d', (typeDict['$complex$'], typeDict['$float$'], 1)),
                       ('$libname$_plan_dft_c2r_2d', (typeDict['$complex$'], typeDict['$float$'], 2)),
                       ('$libname$_plan_dft_c2r_3d', (typeDict['$complex$'], typeDict['$float$'], 3)),
                       ('$libname$_plan_dft_c2r', (typeDict['$complex$'], typeDict['$float$'])),
                       ('$libname$_plan_dft_r2c_1d', (typeDict['$float$'], typeDict['$complex$'], 1)),
                       ('$libname$_plan_dft_r2c_2d', (typeDict['$float$'], typeDict['$complex$'], 2)),
                       ('$libname$_plan_dft_r2c_3d', (typeDict['$float$'], typeDict['$complex$'], 3)),
                       ('$libname$_plan_dft_r2c', (typeDict['$float$'], typeDict['$complex$'])),
                       ('$libname$_plan_r2r_1d', (typeDict['$float$'], typeDict['$float$'], 1)),
                       ('$libname$_plan_r2r_2d', (typeDict['$float$'], typeDict['$float$'], 2)),
                       ('$libname$_plan_r2r_3d', (typeDict['$float$'], typeDict['$float$'], 3)),
                       ('$libname$_plan_r2r', (typeDict['$float$'], typeDict['$float$']))]


def set_argtypes(val, types):
    if types[0] == typeDict['$complex$'] and types[1] == typeDict['$complex$']:
        set_argtypes_c2c(val,types)
    elif types[0] == typeDict['$complex$'] or types[1] == typeDict['$complex$']:
        set_argtypes_c2r(val,types)
    else:
        set_argtypes_r2r(val,types)

def set_argtypes_c2c(val,types):
    if len(types) >2:
        val.argtypes = [ctypes.c_int for i in range(types[2])] +\
                       [ctypeslib.ndpointer(dtype=types[0],ndim=types[2], \
                                            flags='contiguous, writeable, '\
                                                  'aligned'),
                        ctypeslib.ndpointer(dtype=types[1], ndim=types[2],\
                                            flags='contiguous, writeable, '\
                                                  'aligned'),
                        ctypes.c_int, ctypes.c_uint]
    else:
        val.argtypes = [ctypes.c_int, ctypeslib.ndpointer(dtype=int, ndim=1,\
                                                          flags='contiguous, '\
                                                                'aligned'),
                        ctypeslib.ndpointer(dtype=types[0], flags='contiguous,'\
                                                                 ' writeable, '\
                                                                  'aligned'),
                        ctypeslib.ndpointer(dtype=types[1],flags='contiguous, '\
                                                                 'writeable,'\
                                                                 'aligned'),
                        ctypes.c_int, ctypes.c_uint]

def set_argtypes_c2r(val,types):
    if len(types) >2:
        val.argtypes = [ctypes.c_int for i in range(types[2])] +\
                       [ctypeslib.ndpointer(dtype=types[0],ndim=types[2], \
                                            flags='contiguous, writeable, '\
                                                  'aligned'),
                        ctypeslib.ndpointer(dtype=types[1], ndim=types[2],\
                                            flags='contiguous, writeable, '\
                                                  'aligned'),
                        ctypes.c_uint]
    else:
        val.argtypes = [ctypes.c_int, ctypeslib.ndpointer(dtype=int, ndim=1,\
                                                          flags='contiguous, '\
                                                                'aligned'),
                        ctypeslib.ndpointer(dtype=types[0], flags='contiguous,'\
                                                                 ' writeable, '\
                                                                  'aligned'),
                        ctypeslib.ndpointer(dtype=types[1],flags='contiguous, '\
                                                                 'writeable,'\
                                                                 'aligned'),
                        ctypes.c_uint]

def set_argtypes_r2r(val, types):
    if len(types) > 2:
        val.argtypes = [ctypes.c_int for i in range(types[2])] +\
                       [ctypeslib.ndpointer(dtype=types[0], ndim=types[2],
                                            flags='contiguous, writeable, '\
                                                  'aligned'),
                        ctypeslib.ndpointer(dtype=types[1], ndim=types[2],
                                            flags='contiguous, writeable, '\
                                                  'aligned')] +\
                        [ctypes.c_int for i in range(types[2])] +\
                        [ctypes.c_uint]
    else:
        val.argtypes = [ctypes.c_int, ctypeslib.ndpointer(dtype=int, ndim=1,
                                                          flags='contiguous, '\
                                                                'aligned'),
                        ctypeslib.ndpointer(dtype=types[0], flags='contiguous,'\
                                                                  'writeable, '\
                                                                  'aligned'),
                        ctypeslib.ndpointer(dtype=types[1], flags='contiguous,'\
                                                                  'writeable, '\
                                                                  'aligned'),
                        ctypeslib.ndpointer(dtype=int, ndim=1,
                                            flags='contiguous, aligned'),
                        ctypes.c_uint]



# set the return and argument types on the plan functions
for name, types in _typelist:
    val = getattr(lib, name)
    val.restype = ctypes.c_void_p
    set_argtypes(val,types)

#malloc and free
lib.$libname$_malloc.restype = ctypes.c_void_p
lib.$libname$_malloc.argtypes = [ctypes.c_int]
lib.$libname$_free.restype = None
lib.$libname$_free.argtypes = [ctypes.c_void_p]

#create a buffer from memory (necessary for array allocation)
PyBuffer_FromReadWriteMemory = pythonapi.PyBuffer_FromReadWriteMemory
PyBuffer_FromReadWriteMemory.restype = py_object
PyBuffer_FromReadWriteMemory.argtypes = [ctypes.c_void_p, ctypes.c_int]

#executing arrays
lib.$libname$_execute.restype = None
lib.$libname$_execute.argtypes = [ctypes.c_void_p]

#guru execution
lib.$libname$_execute_dft.restype = None
lib.$libname$_execute_dft.argtypes = [ctypes.c_void_p,
                        ctypeslib.ndpointer(flags='aligned, contiguous, '\
                                                        'writeable'),\
                        ctypeslib.ndpointer(flags='aligned, contiguous, '\
                                                        'writeable')]

#destroy plans
lib.$libname$_destroy_plan.restype = None
lib.$libname$_destroy_plan.argtypes = [ctypes.c_void_p]

#wisdom

# create c-file object from python
PyFile_AsFile = pythonapi.PyFile_AsFile
PyFile_AsFile.argtypes = [ctypes.py_object]
PyFile_AsFile.restype = ctypes.c_void_p

#export to file
lib.$libname$_export_wisdom_to_file.argtypes = [ctypes.c_void_p]
lib.$libname$_export_wisdom_to_file.restype = None

#export to string
lib.$libname$_export_wisdom_to_string.argtypes = None
lib.$libname$_export_wisdom_to_string.restype = ctypes.c_char_p

#import from file
lib.$libname$_import_wisdom_from_file.argtypes = [ctypes.c_void_p]
lib.$libname$_import_wisdom_from_file.restype = ctypes.c_int

#import from string
lib.$libname$_import_wisdom_from_string.argtypes = [ctypes.c_char_p]
lib.$libname$_import_wisdom_from_string.restype = ctypes.c_int

#import system wisdom
lib.$libname$_import_system_wisdom.restype = ctypes.c_int
lib.$libname$_import_system_wisdom.argtypes = None

#forget wisdom
lib.$libname$_forget_wisdom.restype = None
lib.$libname$_forget_wisdom.argtype = None
