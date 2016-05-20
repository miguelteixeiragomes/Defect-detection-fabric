unsigned int ravel_idx(unsigned short i, unsigned short j, unsigned short Lj)
{
    return Lj*i + j;
}


__kernel void LBP_transform(__global float* I, __global unsigned char* R)
{
    unsigned short i  = get_global_id(0);
    unsigned short j  = get_global_id(1);
    unsigned short Ly = get_global_size(1);
    
    float pixel = I[ravel_idx(i + 1, j + 1, Ly + 2)];
    unsigned char s = 0;

    if ( I[ravel_idx(i    , j    , Ly + 2)]  >=  pixel )   s +=   1;
    if ( I[ravel_idx(i    , j + 1, Ly + 2)]  >=  pixel )   s +=   2;
    if ( I[ravel_idx(i    , j + 2, Ly + 2)]  >=  pixel )   s +=   4;

    if ( I[ravel_idx(i + 1, j + 2, Ly + 2)]  >=  pixel )   s +=   8;
    if ( I[ravel_idx(i + 2, j + 2, Ly + 2)]  >=  pixel )   s +=  16;

    if ( I[ravel_idx(i + 2, j + 1, Ly + 2)]  >=  pixel )   s +=  32;
    if ( I[ravel_idx(i + 2, j    , Ly + 2)]  >=  pixel )   s +=  64;

    if ( I[ravel_idx(i + 1, j    , Ly + 2)]  >=  pixel )   s += 128;

    R[ravel_idx(i, j, Ly)] = s;
}


//__kernel void LBP_transform_U(__global const float* I, __global float* R)
//{
//    unsigned short i  = get_global_id(0);
//    unsigned short j  = get_global_id(1);
//    unsigned short Ly = get_global_size(1);
//    
//    float pixel = I[ravel_idx(i + 1, j + 1, Ly + 2)];
//    unsigned char s = 0;
//
//    if ( I[ravel_idx(i    , j    , Ly + 2)]  >  pixel )   s +=   1;
//    if ( I[ravel_idx(i    , j + 1, Ly + 2)]  >  pixel )   s +=   2;
//    if ( I[ravel_idx(i    , j + 2, Ly + 2)]  >  pixel )   s +=   4;
//
//    if ( I[ravel_idx(i + 1, j + 2, Ly + 2)]  >  pixel )   s +=   8;
//    if ( I[ravel_idx(i + 2, j + 2, Ly + 2)]  >  pixel )   s +=  16;
//
//    if ( I[ravel_idx(i + 2, j + 1, Ly + 2)]  >  pixel )   s +=  32;
//    if ( I[ravel_idx(i + 2, j    , Ly + 2)]  >  pixel )   s +=  64;
//
//    if ( I[ravel_idx(i + 1, j    , Ly + 2)]  >  pixel )   s += 128;
//
//    char U = 1 - (char)((s >> 7)  ==  (s & 1));
//    u += ;
//    
//    char l = 0;
//    for (char k = 0; k < 8; k++)
//        l  +=  ((s >> k) & 1)*(k + 1);
//
//
//}