import matplotlib
from matplotlib.lines import Line2D
matplotlib.use('Agg')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.compat import StringIO
import matplotlib.ticker as ticker
import sys
import re
import os
import ntpath
import math

colors={'tx2':'orange', 'skx':'#26CAD3', 'bdw':'#005596', 'hsw':'#64d1a2', 'p100':'black', 'k40':'blue', 'titan':'purple', 'knl':'green', 'gv100':'mediumvioletred'}
gpus = ['p100', 'k40', 'titan', 'gv100']

def file_to_df(filename):
    with open(filename, 'r') as file:
        contents = file.read()

    # Read run configurations
    start = contents.find("[", contents.find("Run Configurations"))
    end = contents.find("config")
    config = pd.DataFrame(eval(contents[start:end]))
    #config['config'] = [i for i in range(config.shape[0])]

    # Read data
    stats = contents.find("Min")
    data = pd.read_csv(StringIO(contents[end:stats]), delim_whitespace=True)

    # Join tables and return 
    return data.join(config, on='config', how='inner')

def _is_nr(str):
    return str.find("NR") != -1
is_nr = np.vectorize(_is_nr)

def _gap(arr):
    if len(arr) < 2:
        raise Exception('length 0 or 1 pattern')
    tmp = arr.split(':')
    return int(math.log2(int(tmp[2])))
gap = np.vectorize(_gap)

def _pct(name):
    return int(re.findall('\d+', name)[0])
pct = np.vectorize(_pct)

def get_arch(name):
    n = ntpath.basename(os.path.splitext(name)[0])
    n = n[n.find("_")+1:]
    return n

def _pat_len(pat):
    return len(pat)
pat_len = np.vectorize(_pat_len)

kern = 'Scatter'


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 {} input.dat".format(sys.argv[0]))
        exit(1)

    #Read files
    dfs = []
    percent = []
    minpc = []
    maxpc = []
    for f in sys.argv[1:]:
        tmp = file_to_df(f)
        tmp['arch'] = get_arch(f)
        tmp['gap'] = gap(tmp['name'])
        tmp2 = tmp[tmp['kernel']==kern]
        if kern == "Gather":
            percent.append(max(tmp2['bw(MB/s)']) * .25)
        else:
            percent.append(max(tmp2['bw(MB/s)']) * .125)
        maxpc.append(max(tmp2['bw(MB/s)']))
        minpc.append(min(tmp2['bw(MB/s)']))
        tmp['norm_local'] = tmp['bw(MB/s)'] / max(tmp['bw(MB/s)'])
        tmp['pat_len'] = pat_len(tmp['pattern'])
        if np.any(tmp['arch'] == 'knl'):
            knl = tmp.copy()
        dfs.append(tmp)
    df = pd.concat(dfs)
    print(percent)
    print(maxpc)
    print(minpc)
    print(np.array(minpc)/np.array(maxpc) * 100)


# select only vector length 256 for gpu tests
    
    #for d in np.unique(df['arch']):
    #    for p in np.unique(df['pat_len']):
    #        t2 = df[df['pat_len'] == p]
    #        t3 = t2[t2['arch'] == d]
    #        print(p, d)
    #        print(max(t3['bw(MB/s)']))

    #exit(0)
    df = df[df['pat_len'] == 256]

    #df = df.append(knl)
    df = df[df['kernel'] == kern]
    #print(len(df))

    symbol = {'k40':'v', 'knl':'>', 'p100':'^', 'titan':'<','skx':'d', 'bdw':'p', 'tx2':'D', 'npl':'h','clx':'+', 'gv100':'s'}



    #xp = df[df['arch'] == 'titan']
    #xpa = np.array(xp['bw(MB/s)'])
    #mmm = max(xpa)
    #xpa = xpa / mmm * 100
    #print(xpa)
    #exit(0)


    #print(np.unique(df['gap']))

    df['norm_global'] = df['bw(MB/s)'] / max(df['bw(MB/s)'])

    SMALL_SIZE = 15
    MEDIUM_SIZE = 18
    BIGGER_SIZE = 20

    plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

    #Plot against global max
    fig, ax = plt.subplots()
    for key, grp in df.groupby(['arch']):
        ax = grp.plot(ax=ax, kind='line', x='gap', y='bw(MB/s)', label=key, color=colors[key], linewidth=3, marker=symbol[key], markersize=8, markeredgecolor=colors[key])
        print(key)

    #if kern == "Gather":
    #    xs = [4, 4, 3.5, 2.4]
    #else:
    #    xs = [2, 1.8, 2.5, 4]
    if kern == "Gather":
        xs = [3.5, 4, 4]
    else:
        xs = [2.5, 2, 1.8]
    
    plt.hlines(percent, xmin=xs, xmax=8, linestyles='dashed', color=['blue', 'black','purple'])

    #ax2 = ax.twinx()
    #ax2.set_ylim(3,6)
    #ax2.set_yticks(None)
    #ax2.set_yticks(np.log10(np.array(percent)))
    #lab = [int(i) for i in (np.array(percent)//1000)]
    #ax2.set_yticklabels(lab)
    #ax2.set_yscale("log")
    


    #ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylabel("Log(Bandwidth)")
    ax.set_xlabel("Stride (Doubles)")

    ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.set_xticklabels(["$2^{{{}}}$".format(x) for x in range(0,8)])

    handles,labels = ax.get_legend_handles_labels()
    #handles = [handles[2], handles[0], handles[1], handles[3]]
    #labels = [labels[2], labels[0], labels[1], labels[3]]
    remap = {'k40':'K40c', 'knl':'KNL', 'p100':'P100', 'titan':'Titan', 'gv100':'GV100'}
    labels = [remap[l] for l in labels]
    if kern == "Gather":
        labels.append("25% of peak")
    else:
        labels.append("12.5% of peak")

    handles.append(Line2D([0], [0], color='black', lw=1, dashes=(5,5)))

    if kern == "Gather":
        plt.legend(handles, labels, loc='lower left', title='')
    else:
        plt.legend(handles, labels, loc='lower left', title='')
    print(labels)
    #ax2.get_legend().remove()
    #plt.rcParams.update({'font.size': 28})

    fig.set_size_inches(6,6)
    outname = "ustride_gpu_{}.png".format(kern.lower())
    plt.savefig(outname, transparent=True)
    print("wrote to {}".format(outname))
    outname = "ustride_gpu_{}.pdf".format(kern.lower())
    plt.savefig(outname, transparent=True)
    print("wrote to {}".format(outname))
    exit(0)
    plt.clf()
    exit(0)
