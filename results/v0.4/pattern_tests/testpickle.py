import pandas as pd

data = pd.read_pickle("./pattern_results.pkl")

print(data.head())

exper = data[data['experiment'] == 'lulesh']

print(exper[exper['config'] == 2])
