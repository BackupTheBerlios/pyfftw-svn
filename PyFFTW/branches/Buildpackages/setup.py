#!/usr/bin/env python

from distutils import setup
from distutils.log import warn
import sys

def create_source_from_templates(libname, library, _complex, _float):


try:
    import numpy
    import ctypes
except ImportError, e:
    print "PyFFTW needs numpy and ctypes installed to run and install"
    sys.exit(-1)

try:
    from ctypes import util
    name = 'fftw3'
    fftw = util.find_library(name)
    lib = ctypes.cdll.LoadLibrary(fftw)
    _complex = complex
    _float = float
    create_source_from_templates(name, fftw, _complex, _float)

except, e:
    print "Ctypes could not load the fftw3 shared library"
    sys.exit()

try:
    fftwf = util.find_library('fftw3f')
    lib = ctypes.cdll.LoadLibrary(fftwf)
    
setup(name='PyFFTW3',
      version='0.1',
      description='Python bindings to the FFTW3 C-library',
      author='Jochen Schroeder',
      packages=['fftw3']
      package_dir={'fftw3':'src/fftw3'}
     )
