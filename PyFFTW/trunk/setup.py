#!/usr/bin/env python

from distutils.core import setup
from distutils.log import warn
from distutils.command.build_py import build_py
import ctypes
from ctypes import util
import os
import sys

package_data = {}
if os.name=='nt':
    # Assuming that the dll content of 
    #  ftp://ftp.fftw.org/pub/fftw/fftw-3.2.2.pl1-dll32.zip
    # is copied to the current working directory.
    # FFTW_PATH should be either the final installation directory
    # of the dll files or empty.
    FFTW_PATH = r''
    packages_library_names = {'fftw3': 'libfftw3-3.dll', 
                              'fftw3f' : 'libfftw3f-3.dll',
                              'fftw3l': 'libfftw3l-3.dll'}
    for l, dll in packages_library_names.items():
        s = os.path.join (FFTW_PATH, dll)
        package_data[l] = [s]
else:
    FFTW_PATH = r'/usr/lib/'
    packages_library_names = {'fftw3': 'libfftw3.so', 'fftw3f' : 'libfftw3f.so',
                              'fftw3l': 'libfftw3l.so'}

_complex_typedict = {'fftw3':'complex', 'fftw3f': 'singlecomplex', 'fftw3l': 'longcomplex'}
_float_typedict = {'fftw3': 'double', 'fftw3f': 'single', 'fftw3l': 'longdouble'}
packages_0 = ['fftw3','fftw3f', 'fftw3l']

# To used threads, p+'_threads' library must exist in the system where p in packages_0.

def create_source_from_template(tmplfile, outfile, lib, libname, _complex,
                                _float, location):
    fp = open(tmplfile, 'r')
    tmpl = fp.read()
    fp.close()
    mod = tmpl.replace('$libname$',libname).replace('$complex$',_complex).\
            replace('$library$',lib).replace('$float$',_float).\
            replace('$libraryfullpath$', location)
    fp = open(outfile, 'w')
    fp.write(mod)
    fp.close()
    print "build %s from template %s" %(outfile, tmplfile)

def check_libs(packages):
    libs = {}
    for name in packages[:]:
        try:
            libpath = os.path.join(FFTW_PATH, packages_library_names[name])
            if libpath == None:
                raise OSError
            lib = ctypes.cdll.LoadLibrary(libpath)
            print "found %s at %s" %(name, libpath)
        except OSError, e:
            warn("%s is not located at %s, trying util.find_library(%s)"
                 %(name, libpath, name))
            try:
                libpath = util.find_library(name)
                if libpath == None:
                    raise OSError
                lib = ctypes.cdll.LoadLibrary(libpath)
                print "found %s at %s" %(name, libpath)
            except (TypeError,OSError), e:
                warn("Not installing bindings for %s, because could not load\
                     the library: %s\n if you know the library is installed\
                     you can specify the absolute path in setup.py" % (name, e))
                packages.remove(name)
        libs[name] = libpath
    return packages, libs

packages, liblocation = check_libs(packages_0)

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
            return create_source_from_template(module_file, outfile, package,
                                               package.replace('3',''),
                                               _complex_typedict[package],
                                               _float_typedict[package],
                                               liblocation[package])

setup(name='PyFFTW3',
      version='0.2-svn',
      description='Python bindings to the FFTW3 C-library',
      long_description='PyFFTW provide bindings to access the FFTW3 C-library (http://www.fftw.org) from Python',
      author='Jochen Schroeder',
      author_email='jschrod@berlios.de',
      url = 'pyfftw.berlios.de',
      packages=packages,
      package_dir = dict ([(n, 'src/templates') for n in packages]),
      package_data = package_data,
      cmdclass = {"build_py": build_from_templates},
      license ='GPL v3'
     )
