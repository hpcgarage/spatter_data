#!/bin/bash -l
#Quickly print out serial and vector results with strides

rm -f omp.txt
rm -f scalar.txt

export OMP_NUM_THREADS=1

for s in 1 2 4 8 16 32 64 128;
do
        rm -f tmp1.txt tmp2.txt
        for i in `seq 1 10`;
        do
                numactl --cpunodebind=0 ./spatter -b openmp -s $s -q -R 100 --no-print-header -l 4000000 | cut -d' ' -f10 >> tmp1.txt
                numactl --cpunodebind=0 ./spatter -b serial -s $s -q -R 100 --no-print-header -l 4000000 | cut -d' ' -f9 >> tmp2.txt
        done;
        sort -nr tmp1.txt | head -n1 >> omp.txt
        sort -nr tmp2.txt | head -n1 >> scalar.txt

done;

rm -f tmp1.txt tmp2.txt

echo omp.txt:
cat omp.txt
echo scalar.txt:
cat scalar.txt
