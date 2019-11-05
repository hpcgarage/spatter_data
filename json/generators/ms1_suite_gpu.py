import ms1
import json

cacheline = 128 #bytes
elem      = 8   #bytes
veclen    = 8   #elem
data      = []

memory    = 8 * (1000 ** 3) #8 GB

count = 0
for num in range(1,9):
    for delta in range(1,16):
        for kernel in ['Gather', 'Scatter']:
            for lws in range(4,11):
                config = ms1.ms1(delta, num, cacheline, elem, veclen)
                config['count'] = memory // (config['delta'] * elem)
                config['kernel'] = kernel
                config['local-work-size'] = 2**lws
                data.append(config)

print(json.dumps(data))

