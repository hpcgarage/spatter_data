import json

memory = 16 * (1000**3) # 16GB
data = []
elem = 8 #bytes per element
for kernel in ['Scatter', 'Gather']:
    for STRIDE in range(8): #8
        V = 3
        config ={}
        delta = 2**V * 2**STRIDE
        config['pattern'] = 'UNIFORM:{}:{}:NR'.format(2**V, 2**STRIDE)
        config['kernel'] = kernel
        config['count'] = memory // (delta*elem)
        data.append(config)

print(json.dumps(data))
