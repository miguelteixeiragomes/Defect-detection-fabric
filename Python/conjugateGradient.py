import numpy as np


def f(*x):
    return 100.*np.exp(-np.sum(np.array(x)**2)/100.**2)


def grad(function, x, dx):
    return np.array( [ (.5/dx[i])*(function(x + np.array([0.]*i + [dx[i]] + (len(x) - i - 1)*[0.])) - function(x - np.array([0.]*i + [dx[i]] + (len(x) - i - 1)*[0.]))) for i in range(len(x)) ] )

def norm(v):
    return np.sqrt(np.sum(np.array(v)**2))


def conjGradMax(function, x0, dx = [.5, .5, .05], maxStep = .1, threshold = 1.):
    x = np.array(list(x0))
    lst = [np.array(list(x))]
    for i in range(9):
        print 'x =', x, function(x)
        g = grad(function, x, dx)
        n = norm(g)
        #x += (maxStep/n) * g
        x += g * ((1 - np.exp(-n/maxStep))*maxStep/n)
        lst.append(np.array(list(x)))
    
    while True:
    #while np.sqrt(np.sum((lst[-10] - lst[-1])**2)) > threshold:
        print 'x =', x, function(x)
        g = grad(function, x, dx)
        n = norm(g)
        #x += (maxStep/n) * g
        x += g * ((1 - np.exp(-n/maxStep))*maxStep/n)
        lst.append(np.array(list(x)))
    
    return x


if __name__ == '__main__':
    test = ['grad', 'maxFinder'][1]
    
    if test == 'grad':
        print grad(f, [-100., -100.], 1.)
    
    if test == 'maxFinder':
        print conjGradMax(f, [-1000., -1000.])