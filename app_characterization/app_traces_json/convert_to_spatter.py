import sys
import json

def file_to_dict(filename):
    with open(filename, 'r') as file:
        data = file.read().replace('\n', '')
        return eval(data)

if (len(sys.argv) != 2):
    print("Usage: python3 {} file.json".format(sys.argv[0]))
    exit(1)
    
configs = file_to_dict(sys.argv[1])
for c in configs:
    c['pattern'] = [p//8 for p in c['pattern']]
    c['delta']   = c['delta'] // 8
print(json.dumps(configs))
