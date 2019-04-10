#!/bin/bash
tmpfiles="tmp1.txt tmp2.txt"
rm -f $tmpfiles

for s in 6 12 18 24 30 36 42 48;
do

	
	file=data${s}.rea
	cp $file data.rea


	rm -rf tmp1.txt
	cp papi_config_01.txt papi_config.txt
	for i in `seq 1 3`;
	do
		OMP_NUM_THREADS=1 likwid-pin -c N:0 ./nekbone | grep PROFILE | cut -d' ' -f2,3,4 >> tmp1.txt
	done;
	line=`sort -nk 1 tmp1.txt | head -n 1`
	echo "NEKBONE PAPI01 $s $line" >> tmp2.txt

	rm -rf tmp1.txt
	cp papi_config_23.txt papi_config.txt
	for i in `seq 1 3`;
	do
		OMP_NUM_THREADS=1 likwid-pin -c N:0 ./nekbone | grep PROFILE | cut -d' ' -f2,3,4 >> tmp1.txt
	done;
	line=`sort -nk 1 tmp1.txt | head -n 1`
	echo "NEKBONE PAPI23 $s $line" >> tmp2.txt


	rm -rf tmp1.txt
	cp papi_config_456.txt papi_config.txt
	for i in `seq 1 3`;
	do
		OMP_NUM_THREADS=1 likwid-pin -c N:0 ./nekbone | grep PROFILE | cut -d' ' -f2,3,4,5 >> tmp1.txt
	done;
	line=`sort -nk 1 tmp1.txt | head -n 1`
	echo "NEKBONE PAPI456 $s $line" >> tmp2.txt


done

cat tmp2.txt


rm -f $tmpfiles
