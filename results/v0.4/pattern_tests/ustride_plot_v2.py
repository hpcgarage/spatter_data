import matplotlib
from matplotlib.lines import Line2D
from matplotlib.colors import ListedColormap
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

    hlines = False

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
    df = pd.concat(dfs, sort=False)
    #print(percent)
    #print(maxpc)
    #print(minpc)
    #print(np.array(minpc)/np.array(maxpc) * 100)


# select only vector length 256 for gpu tests

    #for d in np.unique(df['arch']):
    #    for p in np.unique(df['pat_len']):
    #        t2 = df[df['pat_len'] == p]
    #        t3 = t2[t2['arch'] == d]
    #        print(p, d)
    #        print(max(t3['bw(MB/s)']))


    df_gpu = df[df['arch'].isin(gpus)]
    df_cpu = df[~df['arch'].isin(gpus)]
    #####PATRICK STOP HERE
    df_gpu = df_gpu[df_gpu['pat_len'] == 256]

    b0 = 4

    df = pd.concat([df_cpu, df_gpu])
    df = df[df['kernel'] == kern]
    df = df[['arch', 'bw(MB/s)', 'gap']]

    xs_df = df[df['gap'] ==  0]
    ys_df = df[df['gap'] == b0]

    cvals = xs_df['arch'].isin(gpus).to_numpy()
    cmap = ListedColormap(['red', 'black'])
    classes = ['CPUs', 'GPUs']

    xs = xs_df['bw(MB/s)'].to_numpy()
    ys = ys_df['bw(MB/s)'].to_numpy()

    fig, ax = plt.subplots()
    ys_old = []
    ###########old way#############
    #for bb in np.unique(df['gap'].to_numpy()):
    #    ys_df = df[df['gap'] == bb]
    #    ys = ys_df['bw(MB/s)'].to_numpy()
    #    scatter = plt.scatter(xs, ys, s = 15, c = cvals, cmap = cmap)
    #    if len(ys_old) > 0:
    #        for i in range(len(ys)):
    #            plt.plot([xs[i], xs[i]], [ys[i], ys_old[i]], c='black')
    #    ys_old = ys
    ###########old way#############
    #scatter = plt.scatter(xs, ys, s = 15, c = cvals, cmap = cmap)


    ###########new way#############
    top = 0
    bot = 4
    for bb in [top,bot]:
        ys_df = df[df['gap'] == bb]
        ys = ys_df['bw(MB/s)'].to_numpy()
        scatter = plt.scatter(xs, ys, s = 15, c = cvals, cmap = cmap)
        if len(ys_old) > 0:
            for i in range(len(ys)):
                plt.plot([xs[i], xs[i]], [ys[i], ys_old[i]], c='black')
        ys_old = ys
    #sort ys based on xs
    ys_sorted = [x for _, x in sorted(zip(xs,ys), key=lambda pair: pair[0])]
    xs_sorted = sorted(xs)

    for i in range(0, len(xs_sorted)):
        #plt.plot(xs_sorted[i:i+2], xs_sorted[i:i+2], color='black', linestyle='dashed', linewidth=.75)
        plt.plot(xs_sorted[i:i+2], ys_sorted[i:i+2], color='black', linestyle='dashed', linewidth=.75)

    lenxs = len(xs_sorted)

    plt.text(xs_sorted[lenxs-1]*1.2, xs_sorted[lenxs-1], "Stride-1", ha='left')
    plt.plot([xs_sorted[lenxs-1], xs_sorted[lenxs-1]*1.2], [xs_sorted[lenxs-1],xs_sorted[lenxs-1]], color='black', linestyle='solid', linewidth=.75)

    plt.text(xs_sorted[lenxs-1]*1.2, ys_sorted[lenxs-1], "Stride-{}".format(2**bot), ha='left')
    plt.plot([xs_sorted[lenxs-1], xs_sorted[lenxs-1]*1.2], [ys_sorted[lenxs-1],ys_sorted[lenxs-1]], color='black', linestyle='solid', linewidth=.75)



    ###########new way#############

    
    ########### app line#############
    # Using LULESH Pattern 3
    #ys_app = ['bdw', 'npl', 'clx', 'tx2', 'titan', 'p100', 'gv100']
    ys_app = [116703, 244724, 283956, 243404, 161857, 135297, 243099]
    scatter = plt.scatter(xs_sorted, ys_app, s = 15)
    for i in range(0, len(xs_sorted)):
        plt.plot(xs_sorted[i:i+2], ys_app[i:i+2], color='black', linestyle='dashed', linewidth=.75)

    plt.plot([xs_sorted[lenxs-1], xs_sorted[lenxs-1]*1.2], [ys_app[lenxs-1],ys_app[lenxs-1]], color='black', linestyle='solid', linewidth=.75)
    plt.text(xs_sorted[lenxs-1]*1.2, ys_app[lenxs-1], "Lulesh 3", ha='left')

    #exit()

    ########### app line#############


    ulim = max(max(xs), max(ys))
    llim = min(min(xs), min(ys))
    ulim = ulim*1.2
    llim = llim*.8
    plt.xlim((llim, ulim))
    plt.ylim((llim, ulim))

    labels = xs_df['arch'].to_numpy()
    for i in range(len(labels)):
        plt.text(xs[i], xs[i], labels[i], fontsize=10, ha='right', rotation=-45)
        #plt.text(xs[i]+1000, ys[i], labels[i], fontsize=10)


    x_space = np.linspace(ulim, llim, 20)

    plt.plot(x_space, x_space, linewidth=.5, color='black', linestyle='dashed')
    plt.plot(x_space, x_space/2, linewidth=.5, color='black', linestyle='dashed')
    plt.plot(x_space, x_space/4, linewidth=.5, color='black', linestyle='dashed')
    plt.plot(x_space, x_space/8, linewidth=.5, color='black', linestyle='dashed')
    plt.plot(x_space, x_space/16, linewidth=.5, color='black', linestyle='dashed')

    plt.text(llim, llim*1.1, 'Full BW', rotation=45, fontsize=8)
    plt.text(llim*2, llim*1.1, '1/2 BW', rotation=45, fontsize=8)
    plt.text(llim*4, llim*1.1, '1/4 BW', rotation=45, fontsize=8)
    plt.text(llim*8, llim*1.1, '1/8 BW', rotation=45, fontsize=8)
    plt.text(llim*16, llim*1.1, '1/16 BW', rotation=45, fontsize=8)

    plt.legend(handles=scatter.legend_elements()[0], labels=classes, loc='upper left')
    plt.xlabel('Stride-1 DRAM Bandwidth')
    plt.ylabel('Stride-S DRAM Bandwidth'.format(2**b0))

    plt.gcf().subplots_adjust(left=0.15)
    ax.set_xscale("log")
    ax.set_yscale("log")

    fig.set_size_inches(6,6)
    #outname = "tmpname_{}_{}.png".format(kern.lower(), b0)
    outname = "tmpname_{}_{}.png".format(kern.lower(), 'all')
    trans = False
    plt.savefig(outname, transparent=trans)
    print("wrote to {}".format(outname))

    exit(0)
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

    if hlines:
        if kern == "Gather":
            xs = [3.4, 4, 4, 2]
        else:
            xs = [2.5, 1.8, 1.8, 2]

        plt.hlines(percent, xmin=xs, xmax=8, linestyles='dashed', color=['blue', 'purple','black', 'mediumvioletred'])

    #ax2 = ax.twinx()
    #ax2.set_ylim(3,6)
    #ax2.set_yticks(None)
    #ax2.set_yticks(np.log10(np.array(percent)))
    #lab = [int(i) for i in (np.array(percent)//1000)]
    #ax2.set_yticklabels(lab)
    #ax2.set_yscale("log")

    #ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylabel("Bandwidth (MB/s)")
    ax.set_xlabel("Stride (Doubles)")
    ax.text(0.2, 0.1, kern, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=20)

    ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.set_xticklabels(["$2^{{{}}}$".format(x) for x in range(0,8)])

    handles,labels = ax.get_legend_handles_labels()
    #order = [1,2,3,0]
    #order = [0,1,2,3]
    #plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order])
    handles,labels = ax.get_legend_handles_labels()
    remap = {'k40':'K40c', 'knl':'KNL', 'p100':'P100', 'titan':'Titan', 'gv100':'GV100'}
    labels = [remap[l] for l in labels]
    if kern == "Gather":
        labels.append("25% of peak")
    else:
        labels.append("12.5% of peak")

    handles.append(Line2D([0], [0], color='black', lw=1, dashes=(5,5)))

    if kern == "Gather":
        plt.legend(handles, labels, loc='best', title='')
    else:
        plt.legend(handles, labels, loc='best', title='')
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
