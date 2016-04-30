unsigned int ravel_idx(unsigned short i, unsigned short j, unsigned short Lj)
{
    return Lj*i + j;
}


__kernel void LBP_transform(__global const float* I, __global float* R)
{
    unsigned short i  = get_global_id(0);
    unsigned short j  = get_global_id(1);
    unsigned short Ly = get_global_size(1);
    
    float pixel = I[ravel_idx(i + 1, j + 1, Ly + 2)];
    float s = 0.0f;

    if ( I[ravel_idx(i    , j    , Ly + 2)]  >  pixel )   s +=   1.0f;
    if ( I[ravel_idx(i    , j + 1, Ly + 2)]  >  pixel )   s +=   2.0f;
    if ( I[ravel_idx(i    , j + 2, Ly + 2)]  >  pixel )   s +=   4.0f;

    if ( I[ravel_idx(i + 1, j + 2, Ly + 2)]  >  pixel )   s +=   8.0f;
    if ( I[ravel_idx(i + 2, j + 2, Ly + 2)]  >  pixel )   s +=  16.0f;

    if ( I[ravel_idx(i + 2, j + 1, Ly + 2)]  >  pixel )   s +=  32.0f;
    if ( I[ravel_idx(i + 2, j    , Ly + 2)]  >  pixel )   s +=  64.0f;

    if ( I[ravel_idx(i + 1, j    , Ly + 2)]  >  pixel )   s += 128.0f;

    R[ravel_idx(i, j, Ly)] = s;
}


__kernel void LBP_transform_U(__global const float* I, __global float* R)
{
    unsigned short i  = get_global_id(0);
    unsigned short j  = get_global_id(1);
    unsigned short Ly = get_global_size(1);
    
    float pixel = I[ravel_idx(i + 1, j + 1, Ly + 2)];
    unsigned char s = 0;

    if ( I[ravel_idx(i    , j    , Ly + 2)]  >  pixel )   s +=   1;
    if ( I[ravel_idx(i    , j + 1, Ly + 2)]  >  pixel )   s +=   2;
    if ( I[ravel_idx(i    , j + 2, Ly + 2)]  >  pixel )   s +=   4;

    if ( I[ravel_idx(i + 1, j + 2, Ly + 2)]  >  pixel )   s +=   8;
    if ( I[ravel_idx(i + 2, j + 2, Ly + 2)]  >  pixel )   s +=  16;

    if ( I[ravel_idx(i + 2, j + 1, Ly + 2)]  >  pixel )   s +=  32;
    if ( I[ravel_idx(i + 2, j    , Ly + 2)]  >  pixel )   s +=  64;

    if ( I[ravel_idx(i + 1, j    , Ly + 2)]  >  pixel )   s += 128;

    char U;
    if ( (s >> 7)  ==  (s & 1) )   U = 0;
    else   U = 1;

    for (char k = 0; k < 7; k++){
        if ( ((s >> k) & 1)  !=  ((s >> (k + 1)) & 1) )
            U++;
    }
    
    if (U < 3){
        char l = 0;
        for (char k = 0; k < 8; k++)
            l  +=  ((s >> k) & 1)*(k + 1);
        R[ravel_idx(i, j, Ly)] = l;}
    else
        R[ravel_idx(i, j, Ly)] = 9;
}