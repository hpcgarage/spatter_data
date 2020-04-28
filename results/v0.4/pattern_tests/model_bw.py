import spatter_util as su
import pandas as pd
import numpy as np
from scipy import stats
import urd

def get_window(pattern):
    return max(pattern[0:16]) - min(pattern[0:16])
get_window = np.vectorize(get_window)

def get_vardel(pattern):
    return np.var(pattern[0:16])
get_vardel = np.vectorize(get_vardel)

data = pd.read_pickle("./pattern_results.pkl")
data = data[data['experiment'] != 'ustride']
data = data[data['archtype'] == 'GPU']
y = data['bw(MB/s)'].to_numpy()

# Add some new data to the table.
data['window'] = get_window(data['pattern'])
data['vardel'] = get_vardel(data['pattern'])

#urd.gen_and_processurd.process(
print(data.shape)
reuse = np.zeros(data.shape[0])
for ind, row in data.iterrows():
    reuse[ind] = urd.thats_just_mean((row['pattern'], row['delta'], row['length']))

print(reuse)


#print(data.columns)
#keys = ['length', 'window', 'delta', 'vardel']
#for key in keys:
#    x = data[key].to_numpy()
#    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
#    print("{} - rsquared - {:.2f}%".format(key, 100*r_value**2))

