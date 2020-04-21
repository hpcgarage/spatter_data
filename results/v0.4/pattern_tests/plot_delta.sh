#!/bin/bash
python3 ustride_plot_v2.py cuda/ustride_k40.txt cuda/ustride_titan.txt cuda/ustride_p100.txt cuda/ustride_gv100.txt openmp/cori-knl/ustride_knl.txt openmp/pe24clx-clx/ustride_clx.txt openmp/kay-bdw/ustride_bdw.txt openmp/kay-skx/ustride_skx.txt openmp/pe23vega-npl/ustride_npl.txt openmp/kay-tx2/ustride_tx2.txt
