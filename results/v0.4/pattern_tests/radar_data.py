import matplotlib.pyplot as plt
import seaborn as sns; sns.set(style="ticks", color_codes=True)
import pandas as pd
import numpy as np
from math import pi

def is_app(exp):
    if exp == 'ustride':
        return 'Uniform Stride'
    else:
        return 'App'

data = pd.read_pickle("./pattern_results_ext.pkl")
data['pct'] = data['bw'] / data['s0']*100
#data['pct_log2'] = np.log2(data['s0'] / data['bw'])
data['log2_bw'] = np.log2(data['bw'])
data['sd_ind'] = np.sqrt(data['varind'])
data['log2_var'] = np.log2(data['varind'])
data['log2_len'] = np.log2(data['length'])
data['log2_s0'] = np.log2(data['s0'])
data['pct_log2'] = data['log2_bw'] / data['log2_s0']
data['log2_window'] = np.log2(data['window'])
data['log2_delta'] = np.sign(data['delta'])*np.log2(np.abs(1+data['delta']))

keep = ['kernel', 'experiment', 'archtype', 'pct', 'pct_log2', 'log2_bw', 'log2_len', 'log2_window', 'log2_delta', 'log2_var', 'config', 'arch']

data = data[keep]

def pattern_name(app, config):
    return '{}-{:0>3d}'.format(app, config)

data['pattern_name'] = data.apply(lambda row: pattern_name(row.experiment, row.config), axis=1)

## Also comment out the data=data[keep] line above lol
#data.to_pickle('table_gen.pkl')
#print('wrote to {}'.format('table_gen.pkl'))
#exit()

data_gather = data[data['kernel'] == 'Gather']
data_scatter = data[data['kernel'] == 'Scatter']

kernel = 'scater'

if kernel == 'scatter':
    data = data_scatter
    outfile = 'radar_data_scatter.pkl'
else:
    data = data_gather
    outfile = 'radar_data_gather.pkl'





#print(data['pattern_name'])

data = data[data['experiment'] != 'ustride']
patterns = list(set(data['pattern_name'].tolist()))
patterns.sort()

# TMP
keep2 = ['kernel', 'pattern_name', 'archtype', 'arch', 'pct']
data2 = data[keep2].copy()
data2 = data2[data2['pattern_name'] == patterns[0]]
pct = data2['pct'].to_numpy()
data2 = data2.drop(['pct', 'pattern_name'], axis=1)
data2[patterns[0]] = pct

#data4 = data[keep2].copy()
#print(data4[data4['pattern_name'] == patterns[len(patterns)-1]])
#print(data4[data4['pattern_name'] == patterns[1]])


# need to split scatter gather?
for pattern in patterns[1:]:
    data3 = data[keep2].copy()
    pct = data3[data3['pattern_name'] == pattern]['pct'].to_numpy()
#    print(len(pct))
#    print(pct)
#    if (len(pct) != len(data.index)):
#        print("continuing")
#        continue

    data2[pattern] = pct


print(data2)

data2.to_pickle(outfile)
print('wrote to {}'.format(outfile))

# Exit early before old code
exit()

# Make copy
#data_bak = data.copy()
#
#for ARCHTYPE in ['CPU', 'GPU']:
#    for KERNEL in ['Gather', 'Scatter']:
#
#        outfile = "pairs_{}_{}_pct.png".format(ARCHTYPE, KERNEL).lower()
#
#        data = data_bak.copy()
#        data = data[data['archtype'] == ARCHTYPE]
#        data = data[data['kernel'] == KERNEL]
#
#        g = sns.pairplot(data, hue='experiment', corner=True, palette='husl')
#        g.fig.suptitle("{} {} Pairs Plot".format(ARCHTYPE, KERNEL), y=1.04, size=40)
#        #plt.setp(g.get_legend().get_texts(), fontsize='22')
#        g._legend.remove()
#        g.add_legend(fontsize=20, title_fontsize=20)
#
#        g.savefig(outfile)
#        print("wrote {}".format(outfile))
#        exit()
