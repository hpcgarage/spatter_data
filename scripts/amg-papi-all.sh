#!/bin/bash
tmpfiles="tmp1.txt tmp2.txt"
rm -f $tmpfiles
for s in 36 40 44 48 52 56 60;
do
	rm -f tmp1.txt
	cp papi_config_01.txt papi_config.txt
	for i in `seq 1 10`; 
	do
		OMP_NUM_THREADS=1 likwid-pin -c N:0 ./amg -problem 1 -n $s $s $s | grep PROFILE | cut -d' ' -f2,3,4 >> tmp1.txt
	done
	
	line=`sort -nk 1 tmp1.txt | head -n 1`
	echo "AMG PAPI01 $s $line" >> tmp2.txt
	
	rm -f tmp1.txt
	cp papi_config_23.txt papi_config.txt
	for i in `seq 1 10`; 
	do
		OMP_NUM_THREADS=1 likwid-pin -c N:0 ./amg -problem 1 -n $s $s $s | grep PROFILE | cut -d' ' -f2,3,4 >> tmp1.txt
	done
	
	line=`sort -nk 1 tmp1.txt | head -n 1`
	echo "AMG PAPI23 $s $line" >> tmp2.txt

	rm -f tmp1.txt
	cp papi_config_456.txt papi_config.txt
	for i in `seq 1 10`; 
	do
		OMP_NUM_THREADS=1 likwid-pin -c N:0 ./amg -problem 1 -n $s $s $s | grep PROFILE | cut -d' ' -f2,3,4,5 >> tmp1.txt
	done
	
	line=`sort -nk 1 tmp1.txt | head -n 1`
	echo "AMG PAPI456 $s $line" >> tmp2.txt
done

cat tmp2.txt


rm -f $tmpfiles
