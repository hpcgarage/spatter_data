import spatter_util as su
import pandas as pd

GPU_FILES = [
        'cuda/ustride_k40.txt',
        'cuda/ustride_titan.txt',
        'cuda/ustride_p100.txt',
        'cuda/ustride_gv100.txt',

        'cuda/nekbone_k40.txt',
        'cuda/nekbone_titan.txt',
        'cuda/nekbone_p100.txt',
        'cuda/nekbone_gv100.txt',

        'cuda/amg_k40.txt',
        'cuda/amg_titan.txt',
        'cuda/amg_p100.txt',
        'cuda/amg_gv100.txt',

        'cuda/lulesh_k40.txt',
        'cuda/lulesh_titan.txt',
        'cuda/lulesh_p100.txt',
        'cuda/lulesh_gv100.txt',

        'cuda/pennant_k40.txt',
        'cuda/pennant_titan.txt',
        'cuda/pennant_p100.txt',
        'cuda/pennant_gv100.txt',
        ]

CPU_FILES = [
        'openmp/kay-bdw/ustride_bdw.txt',
        'openmp/kay-bdw/pennant_bdw.txt',
        'openmp/kay-bdw/nekbone_bdw.txt',
        'openmp/kay-bdw/amg_bdw.txt',
        'openmp/kay-bdw/lulesh_bdw.txt',

        'openmp/kay-skx/ustride_skx.txt',
        'openmp/kay-skx/pennant_skx.txt',
        'openmp/kay-skx/nekbone_skx.txt',
        'openmp/kay-skx/amg_skx.txt',
        'openmp/kay-skx/lulesh_skx.txt',

        'openmp/kay-tx2/ustride_tx2.txt',
        'openmp/kay-tx2/pennant_tx2.txt',
        'openmp/kay-tx2/nekbone_tx2.txt',
        'openmp/kay-tx2/amg_tx2.txt',
        'openmp/kay-tx2/lulesh_tx2.txt',

        'openmp/cori-knl/ustride_knl.txt',
        'openmp/cori-knl/pennant_knl.txt',
        'openmp/cori-knl/nekbone_knl.txt',
        'openmp/cori-knl/amg_knl.txt',
        'openmp/cori-knl/lulesh_knl.txt',

        'openmp/kay-clx/ustride_clx.txt',
        'openmp/kay-clx/pennant_clx.txt',
        'openmp/kay-clx/nekbone_clx.txt',
        'openmp/kay-clx/amg_clx.txt',
        'openmp/kay-clx/lulesh_clx.txt',

        'openmp/pe23vega-npl/ustride_npl.txt',
        'openmp/pe23vega-npl/pennant_npl.txt',
        'openmp/pe23vega-npl/nekbone_npl.txt',
        'openmp/pe23vega-npl/amg_npl.txt',
        'openmp/pe23vega-npl/lulesh_npl.txt',
        ]

GPU_DATA = [su.file2df(file, restrict_pat_len=256) for file in GPU_FILES]
CPU_DATA = [su.file2df(file)                       for file in CPU_FILES]

DATA = GPU_DATA + CPU_DATA
all_data = pd.concat(DATA, sort=False)

outname = "./pattern_results.pkl"
print("Writing to " + outname)
all_data.to_pickle(outname)

