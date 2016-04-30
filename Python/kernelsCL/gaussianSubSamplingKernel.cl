//#define ravel_idx(i, j, Lj) Lj*i + j

unsigned int ravel_idx(unsigned short i, unsigned short j, unsigned short Lj)
{
    return Lj*i + j;
}


__kernel void gaussSS(__global const float* I, __global float* R, __global const float* gaussKer, unsigned short imgY, unsigned short blurRadiusX, unsigned short blurRadiusY, unsigned short nX, unsigned short nY)
{
    unsigned short i  = get_global_id(0);
    unsigned short j  = get_global_id(1);
    unsigned short Ly = get_global_size(1);

    unsigned short idx1  = blurRadiusX + i*nX;
    unsigned short idx2  = blurRadiusY + j*nY;
    
    float s = gaussKer[ravel_idx(blurRadiusX, blurRadiusY, 2*blurRadiusY + 1)] * I[ravel_idx(idx1, idx2, imgY)];
    for (short k = -blurRadiusX  ;  k < blurRadiusX  ;  k++)
    {
        for (short l = -blurRadiusY  ;  l < blurRadiusY  ;  l++)
        {
            s += gaussKer[ravel_idx(k + blurRadiusX, l + blurRadiusY, 2*blurRadiusY + 1)] * I[ravel_idx(idx1 + k, idx2 + l, imgY)];
        }
    }

    R[ravel_idx(i, j, Ly)] = s;
}