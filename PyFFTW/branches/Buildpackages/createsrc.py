import os
import shutil
tmpl_path = 'templates/'
tmpl_files = ['lib.tmpl','planning.tmpl','wisdom.tmpl']
librarynames = ['fftw3', 'fftw3f', 'fftw3l']
_complexes = {'fftw3':'complex', 'fftw3f': 'complex64', 'fftw3l': 'complex192'}
_floats = {'fftw3': 'float', 'fftw3f': 'float32', 'fftw3l': 'float96'}
paths = {'fftw3' : 'src/fftw3', 'fftw3f': 'src/fftw3/single', 'fftw3l': 'src/fftw3/long_double'}


def create_source_from_template(tmplfile, outfile, lib, libname, _complex, _float):
    fp = open(tmplfile, 'r')
    tmpl = fp.read()
    fp.close()
    mod = tmpl.replace('$libname$',libname).replace('$complex$',_complex).replace('$library$',lib).replace('$float$',_float)
    fp = open(outfile, 'w')
    fp.write(mod)
    fp.close()

for libname in librarynames:
    os.makedirs(paths[libname])
    for f in tmpl_files:
        infile = os.path.join(tmpl_path,f)
        fn, ext = os.path.splitext(f)
        fn = fn+'.py'
        outfile = os.path.join(paths[libname],fn)
        create_source_from_template(infile, outfile, libname, libname.replace('3',''), _complexes[libname], _floats[libname])
        shutil.copyfile(os.path.join(tmpl_path,'__init__.py'),os.path.join(paths[libname],'__init__.py'))

