import pandas as pd
import numpy as np
import re

# gather
rename = {'pennant-000': 'PENNANT-G2',
 'pennant-001': 'PENNANT-G3',
 'pennant-002': 'PENNANT-G12',
 'pennant-003': 'PENNANT-G0',
 'pennant-004': 'PENNANT-G1',
 'pennant-005': 'PENNANT-G7',
 'pennant-007': 'PENNANT-G11',
 'pennant-008': 'PENNANT-G10',
 'pennant-009': 'PENNANT-G5',
 'pennant-010': 'PENNANT-G15',
 'pennant-011': 'PENNANT-G13',
 'pennant-012': 'PENNANT-G14',
 'pennant-013': 'PENNANT-G6',
 'pennant-014': 'PENNANT-G8',
 'pennant-015': 'PENNANT-G4',
 'pennant-016': 'PENNANT-G9',
 'lulesh-001': 'LULESH-G2',
 'lulesh-004': 'LULESH-G4',
 'lulesh-005': 'LULESH-G6',
 'lulesh-006': 'LULESH-G3',
 'lulesh-008': 'LULESH-G1',
 'lulesh-009': 'LULESH-G7',
 'lulesh-010': 'LULESH-G0',
 'lulesh-011': 'LULESH-G5',
 'nekbone-000': 'NEKBONE-G0',
 'nekbone-001': 'NEKBONE-G2',
 'nekbone-002': 'NEKBONE-G1',
 'amg-000': 'AMG-G1',
 'amg-001': 'AMG-G0'}
# scatter
rename.update({'pennant-006': 'PENNANT-S0',
 'lulesh-000': 'LULESH-S3',
 'lulesh-002': 'LULESH-S0',
 'lulesh-003': 'LULESH-S1',
 'lulesh-007': 'LULESH-S2'})

inverse = {v: k for k, v in rename.items()}

def get_int(s):
    return int(re.sub('[^0-9]','', s))

d = pd.read_pickle('./table_gen.pkl')
d = d[d['experiment'] != 'ustride']
d = d[d['archtype'] == 'CPU']

pats = np.unique(d['pattern_name'].to_numpy())
pats = [rename[p] for p in pats]

order_kern = ['-G', '-S']
order_app = ['PENNANT', 'LULESH', 'NEKBONE', 'AMG']

def emit_line(name, pattern, delta):
    print('{} & {} & {} & \\\\'.format(name, str(pattern).replace(' ', ''), delta))

for k in order_kern:
    for a in order_app:
        subset = [p for p in pats if k in p]
        subset = [p for p in subset if a in p]
        subset = sorted(subset, key=get_int)
        if len(subset) == 0:
            continue
        for name in subset:
            old_name = inverse[name]
            pattern = d[d['pattern_name'] == old_name]['pattern'].to_numpy()[0]
            delta = d[d['pattern_name'] == old_name]['delta'].to_numpy()[0]
            emit_line(name, pattern, delta)



