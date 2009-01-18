from ctypes import pythonapi
import ctypes
from fftw3 import lib

_PyFile_AsFile = pythonapi.PyFile_AsFile
_PyFile_AsFile.argtypes = [ctypes.py_object]
_PyFile_AsFile.restype = ctypes.c_void_p

lib.fftw_export_wisdom_to_file.argtypes = [ctypes.c_void_p]
lib.fftw_export_wisdom_to_file.restype = None
def export_wisdom_to_file(filename):
    """Export accumulated wisdom to file given by the filename"""
    fp = open(filename, 'a')
    c_fp = _PyFile_AsFile(fp)
    lib.fftw_export_wisdom_to_file(c_fp)
    fp.close()

lib.fftw_export_wisdom_to_string.argtypes = None
lib.fftw_export_wisdom_to_string.restype = ctypes.c_char_p
def export_wisdom_to_string():
    """Returns a string with the accumulated wisdom"""
    return lib.fftw_export_wisdom_to_string()

lib.fftw_import_wisdom_from_file.argtypes = [ctypes.c_void_p]
lib.fftw_import_wisdom_from_file.restype = ctypes.c_int
def import_wisdom_from_file(filename):
    """Imports wisdom from the file given by the filename"""
    fp = open(filename,'r')
    c_fp = _PyFile_AsFile(fp)
    if lib.fftw_import_wisdom_from_file(c_fp):
        pass
    else:
        raise IOError, "Could not read wisdom from file %s" % filename


lib.fftw_import_wisdom_from_string.argtypes = [ctypes.c_char_p]
lib.fftw_import_wisdom_from_string.restype = ctypes.c_int
def import_wisdom_from_string(wisdom):
    """Import wisdom from the given string"""
    if lib.fftw_import_wisdom_from_string(wisdom):
        pass
    else:
        raise Exception, "Could not read wisdom from string: %s" % wisdom

lib.fftw_import_system_wisdom.restype = ctypes.c_int
lib.fftw_import_system_wisdom.argtypes = None
def import_system_wisdom():
    """Import the system wisdom, this lives under /etc/fftw/wisdom on
    Unix/Linux systems"""
    if lib.fftw_import_system_wisdom():
        pass
    else:
        raise IOError, "Could not read system wisdom. On GNU/Linux and Unix "\
                "system wisdom is located in /etc/fftw/wisdom"

lib.fftw_forget_wisdom.restype = None
lib.fftw_forget_wisdom.argtype = None
def forget_wisdom():
    """Clear all wisdom"""
    lib.fftw_forget_wisdom()


