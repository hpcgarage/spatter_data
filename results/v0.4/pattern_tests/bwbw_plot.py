import spatter_util as su
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

######################### Script Params ###########################
PLATFORMS = ['bdw', 'npl', 'clx', 'tx2', 'titan', 'p100', 'gv100']
STRIDES   = [0, 4]
EXPER     = {'pennant': [2, 5, 14]}
KERNEL    = 'Gather'
###################################################################

## Globals
ORDER = []
min_ys = [np.inf]
max_ys = [0]

def set_order(ord):
    global ORDER
    ORDER = ord.copy()

def reorder(a):
    global ORDER
    return [x for _, x in sorted(zip(ORDER,a), key=lambda pair: pair[0])]

# Read data from pickle file
data = pd.read_pickle("./pattern_results.pkl")

# Subset data based on PLATFORMS and KERNEL param
def member(a):
   return a in PLATFORMS
member = np.vectorize(member)
data = data[member(list(data['arch']))]
data = data[data['kernel'] == KERNEL]

# We need to plot uniform stride results first
ustride = data[data['experiment'] == 'ustride']

# Initialize plot
fig, ax = plt.subplots()

# Get x's and store them to use for reordering other data. Then sort x's.
xs = ustride[ustride['gap'] == 0]['bw(MB/s)'].to_numpy()
set_order(xs)
xs = reorder(xs)

# Get architecture names
names = ustride[ustride['gap'] == 0]['arch'].to_numpy()
names = reorder(names)

# Plot uniform stride results
for g in STRIDES:
    ys = ustride[ustride['gap'] == g]['bw(MB/s)'].to_numpy()
    ys = reorder(ys)
    plt.scatter(xs, ys, s=15, color='black')

    # Used for setting bounds later
    min_ys = min([min_ys, *ys])
    max_ys = max([max_ys, *ys])

    # Add Line Label
    plt.text(xs[len(xs)-1]*1.1, ys[len(ys)-1]*1.1, "Stride-{}".format(2**g), rotation=45)

    # Plot lines connecting points
    for i in range(len(xs)):
        plt.plot(xs[i:i+2], ys[i:i+2], color='black', linestyle='solid', linewidth=.75)
    # Plot line connecting stride MAX with stride 0
    if g == max(STRIDES):
        for i in range(len(xs)):
            line, = ax.plot([xs[i], xs[i]], [xs[i], ys[i]], color='black', linewidth=.75)
            line.set_dashes([6,4])

# Plot application results
for ex in EXPER.keys():
    for con in EXPER[ex]:
        ys = data[(data['experiment'] == ex) & (data['config'] == con)]['bw(MB/s)'].to_numpy()
        if len(ys) == 0:
            print('Warning: ys is length 0. This likely means the experiment+config you are looking for does not use the kernel you specified. Skipping [{},{}].'.format(ex, con))
            continue
        ys = reorder(ys)
        plt.scatter(xs, ys, s=15, color='blue')

        # Used for setting bounds later
        min_ys = min([min_ys, *ys])
        max_ys = max([max_ys, *ys])

        for i in range(len(xs)):
            plt.plot(xs[i:i+2], ys[i:i+2], color='blue', linestyle='solid', linewidth=.75)
        # Add Line Label
        plt.text(xs[len(xs)-1]*1.1, ys[len(ys)-1]*1.1, "{}-{}".format(su.EXPERIMENTS[ex], con), rotation=45, color='blue')

###########
# Visuals #
###########

plt.gcf().subplots_adjust(left=0.15)
ax.set_xscale('log')
ax.set_yscale('log')

#x and y axis limits
ulim = max(max(xs), max_ys) * 1.2
llim = min(min(xs), min_ys) * 0.7
plt.xlim((llim, ulim))
plt.ylim((llim, ulim))

# Remove top and right borders
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Add arch names
for i in range(len(xs)):
    plt.text(xs[i]*.95, xs[i], names[i].upper(), fontsize=8, ha='right')

# Axis Labels
plt.xlabel('Stride-1 DRAM Bandwidth', labelpad=15)
plt.ylabel('Pattern Bandwidth', labelpad=15)

# Title
if len(EXPER) == 0:
    app_str = ''
elif (len(EXPER) == 1):
    app_str = ' vs {} Patterns'.format(su.EXPERIMENTS[list(EXPER.keys())[0]])
else:
    app_str = ' vs Application Patterns'

plt.suptitle('Uniform Stride Bandwidth{}'.format(app_str))

# Subtitle
plt.title('{} Bandwidths'.format(KERNEL), fontsize=10, y=1.04)

# Ticks
plt.minorticks_off()

locs = [10**x for x in range(10) if 10**x >= llim and 10**x <= ulim]
labs_dict = {1:'1 MB/s', 10:'10 MB/s', 100:'100 MB/s',
        1000:'1 GB/s',10000:'10 GB/s', 100000:'100 GB/s',
        1000000:'1 TB/s', 10000000:'10 TB/s', 100000000:'100 TB/s',
        1000000000:'1 PB/s'}
labs = [labs_dict[i] for i in locs]
plt.xticks(locs, labs)
plt.yticks(locs, labs, rotation='vertical')

# Diagonal lines
x_space = np.linspace(llim, max_ys, 20)

plt.plot(x_space, x_space, linewidth=.5, color='#4f4f4f', linestyle='dashed')
plt.plot(x_space, x_space/2, linewidth=.5, color='#4f4f4f', linestyle='dashed')
plt.plot(x_space, x_space/4, linewidth=.5, color='#4f4f4f', linestyle='dashed')
plt.plot(x_space, x_space/8, linewidth=.5, color='#4f4f4f', linestyle='dashed')
plt.plot(x_space, x_space/16, linewidth=.5, color='#4f4f4f', linestyle='dashed')

# Text for diagonal line
plt.text(llim, llim*1.1, 'Full DRAM Bandwidth', rotation=45, fontsize=8)
plt.text(llim*2*.9, llim*1.0, '1/2 BW', rotation=45, fontsize=8)
plt.text(llim*4*.9, llim*1.0, '1/4', rotation=45, fontsize=8)
plt.text(llim*8*.9, llim*1.0, '1/8', rotation=45, fontsize=8)
plt.text(llim*16*.9, llim*1.0, '1/16', rotation=45, fontsize=8)


#############
# Save File #
#############

fig.set_size_inches(6, 6)
outname = "bwbw_tmp.png"
plt.savefig(outname)
print('worte to {}'.format(outname))
