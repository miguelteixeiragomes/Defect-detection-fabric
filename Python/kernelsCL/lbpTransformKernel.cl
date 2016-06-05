#define i  get_global_id(0)
#define j  get_global_id(1)
#define Lx get_global_size(0)
#define Ly get_global_size(1)

inline unsigned int ravel_idx(unsigned short idx1, unsigned short idx2, unsigned short len2)
{
    return len2*idx1 + idx2;
}


__kernel void LBP(__global float* I, __global unsigned char* R)
{
    float pixel = I[ravel_idx(i + 1, j + 1, Ly + 2)];
    unsigned char s = 0;

    s +=   1*(char)( I[ravel_idx(i    , j    , Ly + 2)]  >=  pixel );
    s +=   2*(char)( I[ravel_idx(i    , j + 1, Ly + 2)]  >=  pixel );
    s +=   4*(char)( I[ravel_idx(i    , j + 2, Ly + 2)]  >=  pixel );

    s +=   8*(char)( I[ravel_idx(i + 1, j + 2, Ly + 2)]  >=  pixel );
    s +=  16*(char)( I[ravel_idx(i + 2, j + 2, Ly + 2)]  >=  pixel );

    s +=  32*(char)( I[ravel_idx(i + 2, j + 1, Ly + 2)]  >=  pixel );
    s +=  64*(char)( I[ravel_idx(i + 2, j    , Ly + 2)]  >=  pixel );

    s += 128*(char)( I[ravel_idx(i + 1, j    , Ly + 2)]  >=  pixel );

    R[ravel_idx(i, j, Ly)] = s;
}


__kernel void directionalPatterns(__global unsigned char* R, __global unsigned char* patterns, unsigned short patternsLen, __global unsigned char* nearMisses, unsigned short nearMissesLen)
{
    unsigned char pixel = R[ravel_idx(i, j, Ly)];
    unsigned char r = 0;

    for (int k = 0; k < patternsLen; k++){
        if (pixel == patterns[k]){
            r = 255;
            break;
        }
    }
    if (r == 0)
    {
        for (int k = 0; k < nearMissesLen; k++)
        {
            if (pixel == nearMisses[k])
            {
                r = 127;
                break;
            }
        }
    }
    R[ravel_idx(i, j, Ly)] = r;
}


__kernel void neighborCorrection(__global unsigned char* R)
{
    if (R[ravel_idx( i+1 , j+1 , Ly )] == 127)
    {
        R[ravel_idx( i+1 , j+1 , Ly )] += 128*((unsigned char)(( R[ravel_idx( i+2 , j+1 , Ly )]/255 + 
                                                                 R[ravel_idx( i   , j+1 , Ly )]/255 + 
                                                                 R[ravel_idx( i+1 , j+2 , Ly )]/255 + 
                                                                 R[ravel_idx( i+1 , j   , Ly )]/255 + 
                                                                 R[ravel_idx( i+2 , j+2 , Ly )]/255 + 
                                                                 R[ravel_idx( i   , j   , Ly )]/255 + 
                                                                 R[ravel_idx( i   , j+2 , Ly )]/255 + 
                                                                 R[ravel_idx( i+2 , j   , Ly )]/255 ) > 0) );
    }
}


__kernel void cleanUp(__global unsigned char* R)
{
    if (R[ravel_idx(i, j, Ly)] == 127)
    {
        R[ravel_idx(i, j, Ly)] == 0;
    }
    //R[ravel_idx(i, j, Ly)] = 255*( R[ravel_idx(i, j, Ly)]/255 );
}