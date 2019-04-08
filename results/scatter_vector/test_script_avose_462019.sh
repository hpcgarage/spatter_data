#Quickly print out serial and vector results with strides

for s in 1 2 4 8 16 32 64 128 ; do for((i=0;i<100;i++)) ; do numactl --cpunodebind=0 ./spatter -k gather -b serial --seed 1337 -l 4000000 -s $s 2>/dev/null | grep "GATHER COPY" | sort -nk 9 | tail -n 1 | cut -sd ' ' -f 9 ; done | sort -nk 1 | tail -n 1 ; done

for s in 1 2 4 8 16 32 64 128 ; do for((i=0;i<100;i++)) ; do OMP_NUM_THREADS=1 OMP_PROC_BIND=true OMP_PLACES="{0}" ./spatter -k gather -b OpenMP --seed 1337 -l 4000000 -s $s 2>/dev/null | grep "GATHER COPY" | sort -nk 10 | tail -n 1 | cut -sd ' ' -f 10 ; done | sort -nk 1 | tail -n 1 ; done

