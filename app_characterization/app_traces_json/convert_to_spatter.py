import sys
import json
import numpy as np

def file_to_dict(filename):
    with open(filename, 'r') as file:
        data = file.read().replace('\n', '')
        return eval(data)

if (len(sys.argv) != 2):
    print("Usage: python3 {} file.json".format(sys.argv[0]))
    exit(1)
    
configs = file_to_dict(sys.argv[1])
for c in configs:
    ca = (np.array(c['pattern']) // 8).cumsum()
    ca = ca - min(ca)
    c['pattern'] = ca.tolist()
    c['delta']   = c['delta'] // 8
       
print(json.dumps(configs))
