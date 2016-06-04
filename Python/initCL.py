import pyopencl as cl
1/0

def get_ready_cl(platform_idx = None  ,  device_idx = None):
    if platform_idx == None:
        plat_lst_str = [str(platform) for platform in cl.get_platforms()]
        for i in range(len(plat_lst_str)):
            if ('NVIDIA' in plat_lst_str[i])  or  ('CUDA' in plat_lst_str[i])  or  ('AMD' in plat_lst_str[i]):
                platform_idx = i
                break
        if platform_idx == None:
            platform_idx = 0
    
    if device_idx == None:
        dev_lst_str = [cl.device_type.to_string(device.type) for device in cl.get_platforms()[platform_idx].get_devices()]
        for i in range(len(dev_lst_str)):
            if dev_lst_str[i] == 'GPU':
                device_idx = i
                break
        if device_idx == None:
            platform_idx = 0
    
    my_device = cl.get_platforms()[platform_idx].get_devices()[device_idx]
    print 'chosen device:', my_device
    
    ctx   = cl.Context([my_device])
    queue = cl.CommandQueue(ctx)
    mf    = cl.mem_flags
    return ctx, queue, mf, my_device


if __name__ == '__main__':
    ctx, queue, mf, device = get_ready_cl(0,0)
    prg = cl.Program(ctx, open('kernelsCL\\gaussianSubSamplingKernel.cl', 'r').read()).build()
    print prg
    print device.max_work_group_size