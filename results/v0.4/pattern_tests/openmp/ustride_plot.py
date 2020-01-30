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

colors={'tx2':'orange', 'skx':'#26CAD3', 'bdw':'#005596', 'hsw':'#64d1a2', 'p100':'black', 'k40':'blue', 'titan':'purple', 'knl':'green', 'npl':'tomato', 'clx':'darkorchid'}

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

kern = 'Gather'


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
        tmp = tmp[tmp['kernel']==kern]
        tmp['norm_local'] = tmp['bw(MB/s)'] / max(tmp['bw(MB/s)'])
        tmp['pat_len'] = pat_len(tmp['pattern'])
        dfs.append(tmp)
    df = pd.concat(dfs)


# select only vector length 256 for gpu tests

    #for d in np.unique(df['arch']):
    #    for p in np.unique(df['pat_len']):
    #        t2 = df[df['pat_len'] == p]
    #        t3 = t2[t2['arch'] == d]
    #        print(p, d)
    #        print(max(t3['bw(MB/s)']))

    #exit(0)

    #df = df.append(knl)
    df = df[df['kernel'] == kern]
    #print(len(df))

    symbol = {'k40':'v', 'knl':'>', 'p100':'^', 'titan':'<','skx':'d', 'bdw':'p', 'tx2':'D', 'npl':'h','clx':'+'}


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

    print(df)

    #Plot against global max
    fig, ax = plt.subplots()
    for key, grp in df.groupby(['arch']):
        ax = grp.plot(ax=ax, kind='line', x='gap', y='bw(MB/s)', label=key, color=colors[key], linewidth=3, marker=symbol[key], markersize=8, markeredgecolor=colors[key])
        print(key)

    #if kern == "Gather":
    #    xs = [4, 4, 3.5, 2.4]
    #else:
    #    xs = [2, 1.8, 2.5, 4]

    #ax2 = ax.twinx()
    #ax2.set_ylim(3,6)
    #ax2.set_yticks(None)
    #ax2.set_yticks(np.log10(np.array(percent)))
    #lab = [int(i) for i in (np.array(percent)//1000)]
    #ax2.set_yticklabels(lab)
    #ax2.set_yscale("log")



    #ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylim(10**2*2, 10**5*2)
    ax.set_ylabel("Bandwidth (MB/s)")
    ax.set_xlabel("Stride (Doubles)")
    ax.text(0.8, 0.9, kern, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=20)
    #ax.text(3, 5, "Scatter")

    ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.set_xticklabels(["$2^{{{}}}$".format(x) for x in range(0,8)])

    handles,labels = ax.get_legend_handles_labels()
    #handles = [handles[2], handles[0], handles[1], handles[3]]
    #labels = [labels[2], labels[0], labels[1], labels[3]]
    remap = {'k40':'K40c', 'knl':'KNL', 'p100':'P100', 'titan':'Titan','skx':'SKX', 'bdw':'BDW', 'tx2':'TX2', 'npl':'Naples','clx':'CLX'}
    labels = [remap[l] for l in labels]

    if kern == "Gather":
        plt.legend(handles, labels, loc='lower left', title='')
    else:
        plt.legend(handles, labels, loc='lower left', title='')
    print(labels)
    #ax2.get_legend().remove()
    #plt.rcParams.update({'font.size': 28})

    fig.set_size_inches(6,6)
    outname = "ustride_cpu_{}.png".format(kern.lower())
    plt.savefig(outname, transparent=True)
    print("wrote to {}".format(outname))
    outname = "ustride_cpu_{}.pdf".format(kern.lower())
    plt.savefig(outname, transparent=True)
    print("wrote to {}".format(outname))
    exit(0)
    plt.clf()
    exit(0)
