import json

memory = 8 * (1000**3) # 8GB
data = []
elem = 8
for kernel in ['Scatter', 'Gather']:
    for V in range(3, 11):
        for STRIDE in range(8):
            config ={}
            delta = 2**V * 2**STRIDE
            config['pattern'] = 'UNIFORM:{}:{}:NR'.format(2**V, 2**STRIDE)
            config['kernel'] = kernel
            config['count'] = memory // (delta*elem)
            config['local-work-size'] = 1024
            data.append(config)

print(json.dumps(data))
