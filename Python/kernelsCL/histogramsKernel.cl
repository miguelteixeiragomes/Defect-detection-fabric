#pragma OPENCL EXTENSION cl_khr_int64_base_atomics : enable

unsigned int ravel_idx2(unsigned short i, unsigned short j, unsigned short Lj)
{
    return Lj*i + j;
}


unsigned int ravel_idx3(unsigned short i, unsigned short j, unsigned short k, unsigned short Lj, unsigned short Lk)
{
    return Lk*(Lj*i + j) + k;
}


__kernel void histograms1(__global unsigned char* I, __global unsigned int* hists, unsigned short Ly, unsigned short imgY, unsigned short scan_rateX, unsigned short scan_rateY)
{
    unsigned short i  = get_group_id(0);
    unsigned short j  = get_group_id(1);
    unsigned short k  = get_local_id(0) + scan_rateX*i;
    unsigned short l  = get_local_id(1) + scan_rateY*j;

    atomic_inc( &hists[ ravel_idx3(i, j, I[ravel_idx2(k, l, imgY)], Ly, 256) ] );
}


__kernel void histograms2(__global unsigned char* I, __global unsigned int* hists, unsigned short Ly, unsigned short imgY, unsigned short win_sizeX, unsigned short win_sizeY, unsigned short scan_rateX, unsigned short scan_rateY)
{
    unsigned short i  = get_group_id(0);
    unsigned short j  = get_group_id(1);
    unsigned short k  = get_local_id(0) + scan_rateX*i;
    unsigned short l  = get_local_id(1) + scan_rateY*j;

    atomic_inc( &hists[ ravel_idx3(i, j, I[ravel_idx2(k, l, imgY)], Ly, 256) ] );
}