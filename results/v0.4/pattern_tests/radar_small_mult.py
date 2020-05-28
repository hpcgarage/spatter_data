import numpy as np
import matplotlib.pyplot as plt
from math import pi
import pandas as pd

def make_space_above(axes, topmargin=1):
    """ increase figure size to make topmargin (in inches) space for 
        titles, without changing the axes sizes"""
    fig = axes.flatten()[0].figure
    s = fig.subplotpars
    w, h = fig.get_size_inches()

    figh = h - (1-s.top)*h  + topmargin
    fig.subplots_adjust(bottom=s.bottom*h/figh, top=1-topmargin/figh)
    fig.set_figheight(figh)


def small_plot(ax, xs, title, max_y, col, no_color=False):

    # Calculate angles
    angles = [n / float(len(xs)) * 2 * pi for n in range(len(xs))]

    # Complete circle
    xs += xs[:1]
    angles += angles[:1]

    # Title
    ax.set_title(title, fontsize=8)

    # Plot image
    #ax.plot(angles, xs)
    alpha = 0.4
    if no_color:
        alpha = 0
    ax.fill(angles, xs, color=col, alpha=alpha)
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    if not ABS:
        if max_y < 100:
            max_y = 100
        ax.set_ylim(0, max_y)
    else:
        ax.set_ylim(0, max_y)

    if not ABS:
        circle = plt.Circle((0.0, 0.0), 100, transform=ax.transData._b, color="black", alpha=.9, linewidth=1, fill=False)
        ax.add_artist(circle)

    #ax.grid(color='white', axis='y')
    #ax.grid(alpha=0, axis='x')
    ax.grid(alpha=0)
    ax.set_axis_off()

ABS = False

for kernel in ['gather']:#, 'scatter']:
    if ABS:
        data_in = pd.read_pickle('./radar_data_{}_abs.pkl'.format(kernel))
    else:
        data_in = pd.read_pickle('./radar_data_{}.pkl'.format(kernel))

    for archtype in ['CPU', 'GPU']:
        data = data_in[data_in['archtype'] == archtype]

        patterns = [*data.columns][3:]

        max_y = max(data_in[patterns].to_numpy().flatten())


        N = len(patterns)
        if N >= 8:
            cols = 8
        else:
            cols = N
        if N <= 8:
            rows = 1
        else:
            rows = N//8
            if rows*cols < N:
                rows = rows + 1

        fig, ax = plt.subplots(rows, cols, subplot_kw={'projection':'polar',
                                                 'alpha':0})

        color = {'CPU':'blue', 'GPU':'green'}

        for i in range(len(patterns)):
            val = data[patterns[i]].tolist()
            if rows == 1:
                small_plot(ax[i], val, patterns[i], max_y, color[archtype])
            else:
                small_plot(ax[i//8,i%8], val, patterns[i], max_y, color[archtype])

        if(len(patterns) != rows * cols):
            for i in range(len(patterns), rows*cols):
                if rows == 1:
                    small_plot(ax[i], [0]*len(val), "", max_y, color[archtype], no_color=True)
                else:
                    small_plot(ax[i//8, i%8], [0]*len(val), "", max_y, color[archtype], no_color=True)

        plt.subplots_adjust(left=0.05, right=.95)
        fig.suptitle("{} patterns on {}s (percentage of stride-1 bw)".format(kernel, archtype))
        fig.set_size_inches(cols,rows*1.5)
        make_space_above(ax, topmargin=.5)
        if ABS:
            outfile = 'radar_{}_{}.png'.format(kernel, archtype)
        else:
            outfile = 'radar_{}_{}_pct.png'.format(kernel, archtype)
        print('wrote to ' + outfile)
        plt.savefig(outfile)





