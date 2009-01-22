from lib import lib, PyFile_AsFile

def export_wisdom_to_file(filename):
    """Export accumulated wisdom to file given by the filename"""
    fp = open(filename, 'a')
    c_fp = PyFile_AsFile(fp)
    lib.$libname$_export_wisdom_to_file(c_fp)
    fp.close()

def export_wisdom_to_string():
    """Returns a string with the accumulated wisdom"""
    return lib.$libname$_export_wisdom_to_string()

def import_wisdom_from_file(filename):
    """Imports wisdom from the file given by the filename"""
    fp = open(filename,'r')
    c_fp = PyFile_AsFile(fp)
    if lib.$libname$_import_wisdom_from_file(c_fp):
        pass
    else:
        raise IOError, "Could not read wisdom from file %s" % filename

def import_wisdom_from_string(wisdom):
    """Import wisdom from the given string"""
    if lib.$libname$_import_wisdom_from_string(wisdom):
        pass
    else:
        raise Exception, "Could not read wisdom from string: %s" % wisdom

def import_system_wisdom():
    """Import the system wisdom, this lives under /etc/fftw/wisdom on
    Unix/Linux systems"""
    if lib.$libname$_import_system_wisdom():
        pass
    else:
        raise IOError, "Could not read system wisdom. On GNU/Linux and Unix "\
                "system wisdom is located in /etc/fftw/wisdom"

def forget_wisdom():
    """Clear all wisdom"""
    lib.$libname$_forget_wisdom()


