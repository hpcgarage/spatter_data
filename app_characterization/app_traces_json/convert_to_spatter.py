import sys
import json
import numpy as np

def file_to_dict(filename):
    with open(filename, 'r') as file:
        data = file.read().replace('\n', '')
        return eval(data)

if (len(sys.argv) < 2):
    print("Usage: python3 {} file.json [GPU]".format(sys.argv[0]))
    exit(1)

gpu_mode=0
block_size = 1024
vec_len = 256
if (len(sys.argv) > 2):
    if (sys.argv[2] == 'GPU'):
        gpu_mode = 1
    

configs = file_to_dict(sys.argv[1])
size = 2 * (1000 ** 3)
for c in configs:
    ca = (np.array(c['pattern']) // 8).cumsum()
    ca = ca - min(ca)
    c['pattern'] = ca.tolist()
    c['delta']   = abs(c['delta'] // 8)
    if (gpu_mode):
        pat_len = len(c['pattern'])
        mult = vec_len // pat_len
        p = np.array(c['pattern'])
        for i in range(1,mult):
            c['pattern'] = c['pattern'] + (p+i*c['delta']).tolist() 
        c['delta'] = c['delta']*mult
        c['local-work-size'] = block_size
    #c['pattern'] = sort(c['pattern'])
    c['count']   = int(size / ((c['delta']+1) * 8))

       
print(json.dumps(configs))
