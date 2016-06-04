import numpy as np
print "Local Binary Pattern:"
try:
    from localBinaryPatternCL import directionalLBP_CL as directionalLBP_Tmp
    print "\tKicking it up openCL style!"
except:
    from localBinaryPatternPY import directionalLBP_PY as directionalLBP_Tmp
    import random
    print "\tInstall the damned openCL you %s!" % (random.choice(['fool', 'oaf', 'knave', 'varlet']),)


def directionalLBP(img, patternList, neighborRange = 20):
    return directionalLBP_Tmp( np.float32(img) , patternList , neighborRange )


if __name__ == '__main__':
    from scipy.ndimage import imread
    import pylab as pl
    I = np.average( imread('com.png') , axis = 2 )
    pl.imshow( directionalLBP( I , '|' , 0 ) , cmap = 'Greys_r' )
    pl.show()