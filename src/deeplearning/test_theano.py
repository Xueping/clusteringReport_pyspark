import theano.tensor as T
import numpy

from theano import function

x = T.dscalar('x')
y = T.dscalar('y')
z = x + y
f = function([x,y],z)

print(f(2,3))

print(numpy.allclose(f(16.3,12.1), 28.4))


