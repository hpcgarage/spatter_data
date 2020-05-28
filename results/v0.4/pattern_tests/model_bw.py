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


def get_models(data):
    data = data.rename(columns={'bw(MB/s)':'bw'})

    # Add a column with stride-1 (gap-0) bandwidth
    stride0 = data[data['experiment'] == 'ustride']
    stride0 = stride0[stride0['gap']==0]
    gth_s0 = {}
    sct_s0 = {}
    for row in stride0.itertuples():
        if row.kernel == 'Scatter':
            sct_s0[row.arch] = row.bw
        else:
            gth_s0[row.arch] = row.bw
    s0 = {'Gather':gth_s0, 'Scatter':sct_s0}

    data['s0'] = data.apply(lambda row: s0[row.kernel][row.arch], axis=1)
    data['window'] = get_window(data['pattern'])
    data['varind'] = get_varind(data['pattern'])

    #data.to_pickle("pattern_results_ext.pkl")
    #exit()
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
                all_keys = ['length', 'window', 'delta', 'varind', 's0']
                #keys = ['window', 'delta', 'varind', 's0']

                print(EXP, ARCHTYPE, KERNEL)
                for key in all_keys:
                    x = data[key].to_numpy()
                    print("\t{} {:.2f} {:.2f} {:.2f} {:.2f}".format(key, np.min(x), np.mean(x), np.max(x), np.std(x)))


                keys = ['delta', 'window' ]
                for key in keys:
                    x = data[key].to_numpy()
                    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
                    #print("{} - rsquared - {:.2f}%".format(key, 100*r_value**2))

                # Fit the model
                #model = ols("bw ~ delta + window + varind + s0", data).fit()
                model = ols("bw ~ delta + window ", data).fit()
                try:
                    anv = anova_lm(model)
                except:
                    print("broken: " + EXP + " " + ARCHTYPE + " " + KERNEL)

                coef = model.params.to_numpy()[1:]
                pval = anv['PR(>F)'].to_numpy()[:len(keys)]

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


    return(df_all)

data = pd.read_pickle("./pattern_results.pkl")
print(get_models(data))

