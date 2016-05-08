def maxs(x):
    return [ x[i] for i in range(1,len(x)-1) if (x[i] > x[i-1]) and (x[i] > x[i+1]) ]


def mins(x):
    return [ x[i] for i in range(1,len(x)-1) if x[i] < min(x[i-1], x[i+1]) ]