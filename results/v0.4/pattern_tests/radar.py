import matplotlib.pyplot as plt
import seaborn as sns; sns.set(style="ticks", color_codes=True)
import pandas as pd
import numpy as np
from math import pi

df = pd.DataFrame({
    'group': ['A','B','C','D'],
    'var1': [38, 1.5, 30, 4],
    'var2': [29, 10, 9, 34],
    'var3': [8, 39, 23, 24],
    'var4': [7, 31, 33, 14],
    'var5': [28, 15, 32, 14]
    })

#print(df.loc[0])

#kernel = 'scatter'
kernel = 'gather'

df = pd.read_pickle("./radar_data_{}.pkl".format(kernel))
df = df.drop(['kernel', 'archtype'], axis=1)

categories=list(df)[1:]
N = len(categories)

values = df.iloc[0].drop('arch').values.flatten().tolist()
values += values[:1]


# What will be the angle of each axis in the plot? (we divide the plot / number of variable)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]


# Initialise the spider plot
ax = plt.subplot(111, polar=True)

# Draw one axe per variable + add labels labels yet
plt.xticks(angles[:-1], categories, color='grey', size=8)

# Draw ylabels
ax.set_rlabel_position(0)
plt.yticks([*np.arange(10, max(values), 10)],  color="grey", size=7)
plt.ylim(0,40)

# Plot data
ax.plot(angles, values, linewidth=1, linestyle='solid')

ax.set_ylim(0, max(values))

# Fill area
ax.fill(angles, values, 'b', alpha=0.1)

outname = 'radar_{}.png'.format(kernel)
print('Wrote {}'.format(outname))
plt.savefig(outname)
