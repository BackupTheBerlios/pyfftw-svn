import fftw3
from pylab import *

im = imread('../test/einstein.png')
imm = im[:,:,1]

a = fftw3.fftw_array(imm.shape,dtype=float)
#a = zeros(imm.shape,dtype=float)

b = fftw3.fftw_array((imm.shape[0],imm.shape[1]/2+1),dtype=complex)
#b = zeros((imm.shape[0],imm.shape[1]/2+1),dtype=complex)
p = fftw3.Plan(a,b)
ip = fftw3.Plan(b,a,'backward')
a[:] = imm[:]
del a
for i in xrange(20):
    print i
    p()
    b = b/prod(p.shape)+0.01
    ip()
p()
ip()
imshow(p.inarray)
show()
