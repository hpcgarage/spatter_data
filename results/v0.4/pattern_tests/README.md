This directory contains the majority of our Spatter results in various files. The script `consolidate_spatter.py` is used to consolidate it into a single pandas dataframe. This frame is called `pattern_results.pkl` which is generated sing the pandas `to_pickle()` method. 

You should also be aware of the file `spatter_util.py`. This file contains the utility function `file2df` which is used to turn Spatter output into pandas data frames. To properly use this function with data you have generated yourself, you should do three things. 

1) Name your file `<experiment>_<arch>.txt`.
2) Add your arch as a key to the approrpiate dict (CPU or GPU) and add a \"pretty name\" for it as the value in the dict. 
3) Add a color for your arch.
4) Add your experiment to the EXPERIMENTS list.
