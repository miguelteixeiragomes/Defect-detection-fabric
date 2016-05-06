//#pragma OPENCL EXTENSION cl_khr_int64_base_atomics : enable

int ravel_idx2(int i, int j, int Lj)
{
    return Lj*i + j;
}


int ravel_idx3(int i, int j, int k, int Lj, int Lk)
{
    return Lk*(Lj*i + j) + k;
}


__kernel void setHistsTo0(__global int* hists)
{
    hists[ get_global_id(0) ] = 0;
}


__kernel void histograms(__global unsigned char* I, __global int* hists, __global int* sum_hist, int Ly, int imgY, int win_sizeX, int win_sizeY, int scan_rateX, int scan_rateY)
{
    int i  = get_global_id(0) / win_sizeX;
    int j  = get_global_id(1) / win_sizeY;
    int k  = get_global_id(0) % win_sizeX   +   scan_rateX * i;
    int l  = get_global_id(1) % win_sizeY   +   scan_rateY * j;

    int pixel = I[ravel_idx2(k, l, imgY)];

    atomic_inc( &hists[ ravel_idx3(i, j, pixel, Ly, 256) ] );
    atomic_inc( &sum_hist[ pixel ] );
}


__kernel void histogramSubtraction(__global float* R, __global int* hists, __global int* sum_hist, int Lx, int Ly, int imgY)
{
    int i = get_group_id(0);
    int j = get_global_id(1);
    int k = get_local_id(0);

    __local float diff_hist[256];

    diff_hist[k]  = ((float)(sum_hist[k])) / ((float)(Lx*Ly));
    diff_hist[k] -= (float)(hists[ravel_idx3(i,j,k,Ly,256)]);
    diff_hist[k] *= diff_hist[k];
    int n = 128;
    barrier( CLK_LOCAL_MEM_FENCE );

    while (n != 0){
        if (k < n)
            diff_hist[k] += diff_hist[k + n];
        barrier( CLK_LOCAL_MEM_FENCE );
        n /= 2;
    }
    if (k == 0)
        R[ravel_idx2(i, j, Ly)] = diff_hist[0];
}