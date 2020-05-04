import spatter_util as su
import pandas as pd
import numpy as np
from scipy import stats
import urd
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

def get_window(pattern):
    return max(pattern[0:16]) - min(pattern[0:16])
get_window = np.vectorize(get_window)

def get_varind(pattern):
    return np.var(pattern[0:16])
get_varind = np.vectorize(get_varind)

data = pd.read_pickle("./pattern_results.pkl")
data = data.rename(columns={'bw(MB/s)':'bw'})

data_bak = data.copy()

df_all = pd.DataFrame(columns=['archtype', 'exp', 'kernel', 'param', 'coef', 'pval'])

#for EXP in ['ustride', 'app', 'nekbone', 'lulesh', 'amg', 'pennant']:
for EXP in ['ustride', 'app']:
    for ARCHTYPE in ['CPU', 'GPU']:
        for KERNEL in ['Gather', 'Scatter']:

            data = data_bak.copy()
            if EXP == 'app':
                data = data[data['experiment'] != 'ustride']
            else:
                data = data[data['experiment'] == EXP]

            data = data[data['archtype'] == ARCHTYPE]
            data = data[data['kernel'] == KERNEL]

            if EXP == 'pennant' and ARCHTYPE == 'GPU' and KERNEL == 'Scatter':
                continue

            if (data.shape[0] == 0):
                continue

            y = data['bw'].to_numpy()

            # Add some new data to the table.
            data['window'] = get_window(data['pattern'])
            data['varind'] = get_varind(data['pattern'])

            #urd.gen_and_processurd.process(
            #print(data.shape)
            #reuse = np.zeros(data.shape[0])
            #for ind, row in data.iterrows():
            #    reuse[ind] = urd.thats_just_mean((row['pattern'], row['delta'], 10))
            #    if ind > 3:
            #        break
            #
            #print(reuse)

            #print(data.columns)
            keys = ['length', 'window', 'delta', 'varind']
            for key in keys:
                x = data[key].to_numpy()
                slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
                #print("{} - rsquared - {:.2f}%".format(key, 100*r_value**2))

            # Fit the model
            model = ols("bw ~ delta + length  + window + varind", data).fit()
            try:
                anv = anova_lm(model)
            except:
                print("broken: " + EXP + " " + ARCHTYPE + " " + KERNEL)

            coef = model.params.to_numpy()[1:]
            pval = anv['PR(>F)'].to_numpy()[:4]

            vals = np.stack([coef, pval]).transpose()

            df = pd.DataFrame(vals, columns=['coef', 'pval'])
            df['param'] = keys
            df['exp'] = EXP
            df['archtype'] = ARCHTYPE
            df['kernel'] = KERNEL
            df = df[['archtype', 'exp', 'kernel', 'param', 'coef', 'pval']]
            #print(EXP, ARCHTYPE, KERNEL)
            #print(df)
            df_all = df_all.append(df)

print(df_all)



