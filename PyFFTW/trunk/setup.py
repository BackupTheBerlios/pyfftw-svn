#!/usr/bin/env python

from distutils.core import setup
from distutils.log import warn
from distutils.command.build_py import build_py
import ctypes
from ctypes import util
import os

_complex_typedict = {'fftw3':'complex', 'fftw3f': 'singlecomplex', 'fftw3l': 'longcomplex'}
_float_typedict = {'fftw3': 'double', 'fftw3f': 'single', 'fftw3l': 'longdouble'}
packages_0 = ['fftw3','fftw3f', 'fftw3l']

def create_source_from_template(tmplfile, outfile, lib, libname, _complex, _float):
    fp = open(tmplfile, 'r')
    tmpl = fp.read()
    fp.close()
    mod = tmpl.replace('$libname$',libname).replace('$complex$',_complex).replace('$library$',lib).replace('$float$',_float)
    fp = open(outfile, 'w')
    fp.write(mod)
    fp.close()
    print "build %s from template %s" %(outfile, tmplfile)

def check_libs(packages):
    for name in packages:
        try:
            lib = util.find_library(name)
            lib = ctypes.cdll.LoadLibrary(lib)
        except OSError, e:
            if name == 'fftw3':
                raise Exception, "Ctypes could not load fftw3"
            else:
                warn("Not installing bindings for %s, because I could not load the library")
                packages.remove(name)
    return packages

class build_from_templates(build_py):
    def build_module(self, module, module_file, package):
        module, ext = os.path.splitext(module)
        if not ext == '.tmpl':
            outfile = self.get_module_outfile(self.build_lib, [package], module)
            dir = os.path.dirname(outfile)
            self.mkpath(dir)
            return self.copy_file(module_file, outfile, preserve_mode=0)
        else:
            outfile = self.get_module_outfile(self.build_lib, [package], module)
            dir = os.path.dirname(outfile)
            self.mkpath(dir)
            return create_source_from_template(module_file, outfile, package, package.replace('3',''), _complex_typedict[package], _float_typedict[package])

setup(name='PyFFTW3',
      version='0.1',
      description='Python bindings to the FFTW3 C-library',
      author='Jochen Schroeder',
      email='cycomanic@gmail.com',
      url = 'pyfftw.berlios.de',
      packages=check_libs(packages_0),
      package_dir={'fftw3':'src/templates/','fftw3f':'src/templates/','fftw3l':'src/templates/'},
      cmdclass = {"build_py": build_from_templates}
     )
