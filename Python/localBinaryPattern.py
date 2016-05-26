import numpy as np
print "Local Binary Pattern:"
try:
    from localBinaryPatternCL import directionalLBP_CL as directionalLBP_Tmp
    print "\tKicking it up openCL style!"
except:
    from localBinaryPatternPY import directionalLBP_PY as directionalLBP_Tmp
    print "\tInstall the damned openCL fool!"


def directionalLBP(img, patternList, neighborRange = 0):
    return directionalLBP_Tmp( np.float32(img) , patternList , neighborRange )


if __name__ == '__main__':
    from scipy.ndimage import imread
    import pylab as pl
    I = np.average( imread('com.png') , axis = 2 )
    pl.imshow( directionalLBP( I , 15 ) , cmap = 'Greys_r' )
    pl.show()