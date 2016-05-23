#define i  get_global_id(0)
#define j  get_global_id(1)
#define Li get_global_size(0)
#define Lj get_global_size(1)


inline unsigned int ravel_idx(unsigned short idx1, unsigned short idx2, unsigned short len2)
{
    return idx1*len2 + idx2;
}


float bilinearInterpolation(__global float* I, unsigned short Ly, float x, float y)
{
    unsigned short x1, x2, y1, y2;
    float f11, f12, f21, f22;
    x1 = x;
    x2 = x1 + 1;
    y1 = y;
    y2 = y1 + 1;
    f11 = I[ ravel_idx(x1, y1, Ly) ];
    f21 = I[ ravel_idx(x2, y1, Ly) ];
    f12 = I[ ravel_idx(x1, y2, Ly) ];
    f22 = I[ ravel_idx(x2, y2, Ly) ];
    return f11*(x2 - x)*(y2 - y)  +  f21*(x - x1)*(y2 - y)  +  f12*(x2 - x)*(y - y1)  +  f22*(x - x1)*(y - y1);
}


__kernel void rotateUpTo90_horizontal(__global float* I, __global float* R, float theta, float x, unsigned short lenIy)
{
    float r = sqrt((float)(i*i + j*j));
    float o = atan2((float)(j), (float)(i)) - theta;

    float X = r*cos(o) + 0.0f; // falta tratar de centrar o rectandulo quando ele nao toca as pontas.
    float Y = r*sin(o) + x;

    R[ravel_idx(i, j, Lj)] = bilinearInterpolation(I, lenIy, X, Y);
}