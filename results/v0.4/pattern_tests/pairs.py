import matplotlib.pyplot as plt
import seaborn as sns; sns.set(style="ticks", color_codes=True)
import pandas as pd
import numpy as np

def is_app(exp):
    if exp == 'ustride':
        return 'Uniform Stride'
    else:
        return 'App'

data = pd.read_pickle("./pattern_results_ext.pkl")
data['pct'] = data['s0'] / data['bw']
#data['pct_log2'] = np.log2(data['s0'] / data['bw'])
data['log2_bw'] = np.log2(data['bw'])
data['sd_ind'] = np.sqrt(data['varind'])
data['log2_var'] = np.log2(data['varind'])
data['log2_len'] = np.log2(data['length'])
data['log2_s0'] = np.log2(data['s0'])
data['pct_log2'] = data['log2_s0'] / data['log2_bw']
data['log2_window'] = np.log2(data['window'])
data['log2_delta'] = np.sign(data['delta'])*np.log2(np.abs(1+data['delta']))
keep = ['kernel', 'experiment', 'archtype', 'pct', 'pct_log2', 'log2_bw', 'log2_len', 'log2_window', 'log2_delta', 'log2_var']
data = data[keep]

#print(np.count_nonzero(data['log2_delta'] <= np.abs(data['log2_delta'])))
#data = data[data['log2_window'] <= np.abs(data['log2_delta'])]
#print(data)

#for row in data.itertuples():
#    print(row.experiment)
#    if row.experiment != 'app':
#        print(row.log2_bw)
#        exit()
#exit()

# Repurpose experiment column
#data = data[(data['experiment'] == 'ustride') | (data['experiment'] == 'amg')]
#data['experiment'] = data.apply(lambda row: is_app(row.experiment), axis=1)

# Make copy
data_bak = data.copy()

for ARCHTYPE in ['CPU', 'GPU']:
    for KERNEL in ['Gather', 'Scatter']:

        outfile = "pairs_{}_{}_pct.png".format(ARCHTYPE, KERNEL).lower()

        data = data_bak.copy()
        data = data[data['archtype'] == ARCHTYPE]
        data = data[data['kernel'] == KERNEL]

        g = sns.pairplot(data, hue='experiment', corner=True, palette='husl')
        g.fig.suptitle("{} {} Pairs Plot".format(ARCHTYPE, KERNEL), y=1.04, size=40)
        #plt.setp(g.get_legend().get_texts(), fontsize='22')
        g._legend.remove()
        g.add_legend(fontsize=20, title_fontsize=20)

        g.savefig(outfile)
        print("wrote {}".format(outfile))
        exit()
