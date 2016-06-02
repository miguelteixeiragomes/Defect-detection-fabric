import numpy as np


def f(*x):
    return np.exp(-np.sum(np.array(x)**2))


def grad(function, x, dx):
    return np.array( [ (.5/dx)*(f(x + np.array([0.]*i + [dx] + (len(x) - i - 1)*[0.])) - f(x - np.array([0.]*i + [dx] + (len(x) - i - 1)*[0.]))) for i in range(len(x)) ] )

def norm(v):
    return np.sqrt(np.sum(np.array(v)**2))


def conjGradMax(function, x0, dx = 1., maxStep = 1.):
    x = np.array(list(x0))
    g = grad(function, x, dx)
    n = norm(g)
     = g * (np.exp(-n/maxStep)/n)


if __name__ == '__main__':
    test = ['grad'][0]
    
    if test == 'grad':
        print grad(f, [0, 0, 0], [.001]*3)