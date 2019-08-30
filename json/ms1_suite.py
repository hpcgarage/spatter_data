import ms1
import json
import pandas as pd

cacheline = 128 #bytes
elem      = 8   #bytes
veclen    = 8   #elem
data      = []

memory    = 16 * (1000 ** 3) #16 GB

count = 0
for num in range(1,9):
    for delta in range(1,16):
        for kernel in ['Gather', 'Scatter']:
            config = ms1.ms1(delta, num, cacheline, elem, veclen)
            config['count'] = memory // (config['delta'] * elem)
            config['kernel'] = kernel
            data.append(config)

print(json.dumps(data))

