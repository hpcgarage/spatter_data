import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from math import pi
import pandas as pd
import string
#plt.style.use('ggplot')

# Filename
kernel = 'scatter'
outfile = 'sm2_scatter.pdf'

# Figure params
figsize=[4.1,3.25] # width, height in inches

# Outer grid params
outer_grid_rows = 2
outer_grid_cols = 1
outer_grid_height_ratios = [1,1]
outer_grid_width_ratios = [1]

if len(outer_grid_width_ratios) != outer_grid_cols:
    print("Error, wrong number of width ratios")
    exit()

if len(outer_grid_height_ratios) != outer_grid_rows:
    print("Error, wrong number of height ratios")
    exit()

pretty_names = {'tx2':'TX2',
                'skx':'SKX',
                'bdw':'BDW',
                'npl':'NPL',
                'clx':'CLX',
                'knl':'KNL',
                'titan':'TITAN Xp',
                'k40':'K40',
                'gv100':'V100',
                'p100':'P100',}

def small_plot(ax, xs, title, max_y, col, label='', app='', names=[], no_color=False):

    # Calculate angles
    angles = [n / float(len(xs)) * 2 * pi for n in range(len(xs))]

    # Complete circle
    xs += xs[:1]
    angles += angles[:1]


    # Title
    if title != '':
        if kernel == 'Gather':
            title = 'G{}'.format(title)
        else:
            title = 'S{}'.format(title)

    ax.set_title(title, fontsize=8, y=.90)

    # Plot image
    #ax.plot(angles, xs)
    alpha = 0.6
    if no_color:
        alpha = 0
    ax.fill(angles, xs, color=col, alpha=alpha)

    ax.set_yticklabels([])

    ax.set_xticks(angles[:-1])
    names = [pretty_names[a] for a in names]
    ax.set_xticklabels(names, fontdict={'fontsize':12})
    ax.tick_params(pad=2)

    if not ABS:
        if max_y < 100:
            max_y = 100
        ax.set_ylim(0, max_y)
    else:
        ax.set_ylim(0, max_y)

    if not ABS:
        circle = plt.Circle((0.0, 0.0), 100, transform=ax.transData._b, color="black", alpha=.9, linewidth=1, fill=False)
        ax.add_artist(circle)

    ax.text(-.25, .5, label,
            ha='center',va='center',
            rotation=90, transform=ax.transAxes)
    if app == 'Legend':
        ax.text(-.50,0, app,
                ha='center',va='center',
                rotation=90, transform=ax.transAxes,
                fontsize=15)
        ax.text(1,-1.5, 'Percent of Stride-1 BW:\n  Inner circle: 100%\n  Outer circle: 325%',
                ha='left',va='center',
                transform=ax.transAxes,
                fontsize=10)
    else:
        ax.text(-.65,0, app,
                ha='center',va='center',
                rotation=90, transform=ax.transAxes,
                fontsize=15)
    #ax.grid(color='white', axis='y')
    #ax.grid(alpha=0, axis='x')
    ax.grid(alpha=0)
    #ax.set_axis_off()

ABS=False
if ABS:
    data_in = pd.read_pickle('./radar_data_{}_abs.pkl'.format(kernel))
else:
    data_in = pd.read_pickle('./radar_data_{}.pkl'.format(kernel))

data = data_in

# Reorder rows
data = data.set_index('arch', drop=False)
data = data.reindex(['bdw', 'skx', 'clx', 'knl', 'tx2', 'npl', 'k40', 'titan', 'p100', 'gv100'])


patterns = [*data.columns][3:]
max_y = max(data_in[patterns].to_numpy().flatten())
print('The max_y value is {}'.format(max_y))

head_cols = ['kernel', 'archtype', 'arch']

apps = ['pennant', 'lulesh']
pat_dict = {}
for a in apps:
    pat_dict[a] = [p for p in patterns if a in p]

data_dict = {}
for a in apps:
    data_dict[a] = data[head_cols + pat_dict[a]]

for a in apps:
    col = data_dict[a].columns
    rename_dict = {}
    ind = 0
    for c in col:
        if a in c:
            rename_dict[c] = str(ind)
            print('{} becomes {}'.format( c, ind))
            ind = ind + 1
        else:
            rename_dict[c] = c
    data_dict[a] = data_dict[a].rename(columns=rename_dict)
    sort_dict = {} 
    for i in range(ind):
        vals = data_dict[a][str(i)].tolist()
        maxv = np.sum(vals)
        sort_dict[i] = maxv
    k1 = sorted(sort_dict, key=sort_dict.get, reverse=True)
    sorter = {}
    for i in range(ind):
        sorter[str(k1[i])] = str(i)
    print('Renaming {} patterns as follows'.format(a))
    print(sorter)
    data_dict[a] = data_dict[a].rename(columns=sorter)

fig, ax_all =  plt.subplots()
fig.set_size_inches(figsize)
ax_all.axis('off')
height=.54
boxcolor = 'ghostwhite'

#PENNANT Box
ax_all.add_patch(plt.Rectangle((-.125,-.025),1.12,height,
                 clip_on=False,linewidth = 1, ec='black', fc='white'))
#LULESH Box
ax_all.add_patch(plt.Rectangle((-.125,height),1.12,height-.015,
                 clip_on=False,linewidth = 1, ec='black', fc='white'))


outer_grid = gridspec.GridSpec(nrows=outer_grid_rows,
                               ncols=outer_grid_cols,
                               height_ratios=outer_grid_height_ratios,
                               width_ratios=outer_grid_width_ratios,
                                figure=fig)

gs = {}
gs['pennant']     = outer_grid[1,:].subgridspec(nrows=2,ncols=4)
gs['lulesh']      = outer_grid[0,:].subgridspec(nrows=2,ncols=4)

n_pats   = {'pennant':1, 'lulesh':4,}
max_cols = {'pennant':4, 'lulesh':4,}

col = {'cpu':'mediumblue', 'gpu':'mediumseagreen'}



# Pennant first, why not
irow = 0
icol = 0
count_row = 0
for i in range(n_pats['pennant']):
    ax_cpu = fig.add_subplot(gs['pennant'][irow,   icol], projection='polar')
    ax_gpu = fig.add_subplot(gs['pennant'][irow+1, icol], projection='polar')
    title = icol + count_row*max_cols['pennant']


    if icol == 0:
        label_cpu = 'CPU'
        label_gpu = 'GPU'
        if irow == 0:
            app='PENNANT'

    xs_cpu = data_dict['pennant'][data['archtype']=='CPU'][str(title)].tolist()
    xs_gpu = data_dict['pennant'][data['archtype']=='GPU'][str(title)].tolist()

    small_plot(ax_cpu, xs_cpu, title, max_y, col['cpu'], label=label_cpu, app=app)
    small_plot(ax_gpu, xs_gpu, '',    max_y, col['gpu'], label=label_gpu, app='')


    label_cpu = ''
    label_gpu = ''
    app=''

    #small_plot(ax_cpu, xs, title, max_y, col)
    #small_plot(ax_gpu, xs, title, max_y, col)

    icol = icol + 1
    if icol == max_cols['pennant']:
        icol = 0
        irow = irow + 2
        count_row = count_row + 1


# Lulesh first, why not

irow = 0
icol = 0
count_row = 0
for i in range(n_pats['lulesh']):
    ax_cpu = fig.add_subplot(gs['lulesh'][irow,   icol], projection='polar')
    ax_gpu = fig.add_subplot(gs['lulesh'][irow+1, icol], projection='polar')
    title = icol + count_row*max_cols['lulesh']


    if icol == 0:
        label_cpu = 'CPU'
        label_gpu = 'GPU'
        if irow == 0:
            app='LULESH'

    xs_cpu = data_dict['lulesh'][data['archtype']=='CPU'][str(title)].tolist()
    xs_gpu = data_dict['lulesh'][data['archtype']=='GPU'][str(title)].tolist()

    small_plot(ax_cpu, xs_cpu, title, max_y, col['cpu'], label=label_cpu, app=app)
    small_plot(ax_gpu, xs_gpu, '',    max_y, col['gpu'], label=label_gpu, app='')

    label_cpu = ''
    label_gpu = ''
    app=''

    #small_plot(ax_cpu, xs, title, max_y, col)
    #small_plot(ax_gpu, xs, title, max_y, col)

    icol = icol + 1
    if icol == max_cols['lulesh']:
        icol = 0
        irow = irow + 2
        count_row = count_row + 1

fig.suptitle('Scatter Patterns on CPUs and GPUs', y=.99, fontsize=14, x=.475)
plt.savefig(fname=outfile)
print('wrote to ', outfile)
