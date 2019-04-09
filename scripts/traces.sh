#!/bin/bash
# Author: Patrick Lavin
# Yes I know this script looks like garbage. But it was written at midnight 48 hours before a paper dealine. 

make > /dev/null

skipstr=`cat ../src/sgbuf.c | grep SKIP | head -n 1`

outfile=/dev/stdout


if [[ $# -gt 0 ]]
then
	if [[ $skipstr == *0* ]]
	then 
		skipsuffix="use16"
	else
		skipsuffix="skip16"
	fi
	outfile=traces_${1}_${skipsuffix}.txt
	echo "writing results to $outfile"
	rm -rf $outfile
else
	echo $skipstr
fi

nekbone_size=47183040
amg_size=27150000
nekbone_trace=../traces/nekbone.pat
amg_trace=../traces/amg.pat
tmpfiles="tmp1.txt tmp2.txt tmp3.txt"
rm -f $tmpfiles

cp papi_config_01.txt papi_config.txt
for i in `seq 1 10`; 
do 
	OMP_NUM_THREADS=1 likwid-pin -c N:0 ./spatter -l $nekbone_size -t $nekbone_trace -q --nph -R 20 | grep OPENMP > tmp1.txt
	tail -n +2 papi_output.txt > tmp2.txt
	pr -w 180 -m -t tmp1.txt tmp2.txt > tmp3.txt
	#OMP_NUM_THREADS=1 likwid-pin -c N:0 ./spatter -l $amg_size -t ../traces/amg.pat -q --nph -R 20 | grep OPENMP | cut -f 10 -d' ' | sort -r | head -n 1 >> tmp2.txt
done;

echo -n "NEKBONE $nekbone_size PAPI01 " >> $outfile
cat tmp3.txt | sort -nrk10 | head -n 1 | cut -f 4,10,11,12 -d' ' >> $outfile

rm -f $tmpfiles

cp papi_config_23.txt papi_config.txt
for i in `seq 1 10`; 
do 
	OMP_NUM_THREADS=1 likwid-pin -c N:0 ./spatter -l $nekbone_size -t $nekbone_trace -q --nph -R 20 | grep OPENMP > tmp1.txt
	tail -n +2 papi_output.txt > tmp2.txt
	pr -w 180 -m -t tmp1.txt tmp2.txt > tmp3.txt
	#OMP_NUM_THREADS=1 likwid-pin -c N:0 ./spatter -l $amg_size -t ../traces/amg.pat -q --nph -R 20 | grep OPENMP | cut -f 10 -d' ' | sort -r | head -n 1 >> tmp2.txt
done;

echo -n "NEKBONE $nekbone_size PAPI23 "  >> $outfile
cat tmp3.txt | sort -nrk10 | head -n 1 | cut -f 4,10,11,12 -d' ' >>$outfile

cp papi_config_456.txt papi_config.txt
for i in `seq 1 10`; 
do 
	OMP_NUM_THREADS=1 likwid-pin -c N:0 ./spatter -l $nekbone_size -t $nekbone_trace -q --nph -R 20 | grep OPENMP > tmp1.txt
	tail -n +2 papi_output.txt > tmp2.txt
	pr -w 180 -m -t tmp1.txt tmp2.txt > tmp3.txt
	#OMP_NUM_THREADS=1 likwid-pin -c N:0 ./spatter -l $amg_size -t ../traces/amg.pat -q --nph -R 20 | grep OPENMP | cut -f 10 -d' ' | sort -r | head -n 1 >> tmp2.txt
done;

echo -n "NEKBONE $nekbone_size PAPI456 " >> $outfile
cat tmp3.txt | sort -nrk10 | head -n 1 | cut -f 4,10,11,12,13 -d' ' >> $outfile

cp papi_config_01.txt papi_config.txt
for i in `seq 1 10`; 
do 
	OMP_NUM_THREADS=1 likwid-pin -c N:0 ./spatter -l $amg_size -t $amg_trace -q --nph -R 20 | grep OPENMP > tmp1.txt
	tail -n +2 papi_output.txt > tmp2.txt
	pr -w 180 -m -t tmp1.txt tmp2.txt > tmp3.txt
	#OMP_NUM_THREADS=1 likwid-pin -c N:0 ./spatter -l $amg_size -t ../traces/amg.pat -q --nph -R 20 | grep OPENMP | cut -f 10 -d' ' | sort -r | head -n 1 >> tmp2.txt
done;

echo -n "AMG $amg_size PAPI01 " >> $outfile
cat tmp3.txt | sort -nrk10 | head -n 1 | cut -f 4,10,11,12 -d' ' >> $outfile

rm -f $tmpfiles

cp papi_config_23.txt papi_config.txt
for i in `seq 1 10`; 
do 
	OMP_NUM_THREADS=1 likwid-pin -c N:0 ./spatter -l $amg_size -t $amg_trace -q --nph -R 20 | grep OPENMP > tmp1.txt
	tail -n +2 papi_output.txt > tmp2.txt
	pr -w 180 -m -t tmp1.txt tmp2.txt > tmp3.txt
	#OMP_NUM_THREADS=1 likwid-pin -c N:0 ./spatter -l $amg_size -t ../traces/amg.pat -q --nph -R 20 | grep OPENMP | cut -f 10 -d' ' | sort -r | head -n 1 >> tmp2.txt
done;

echo -n "AMG $amg_size PAPI23 "  >> $outfile
cat tmp3.txt | sort -nrk10 | head -n 1 | cut -f 4,10,11,12 -d' ' >> $outfile

cp papi_config_456.txt papi_config.txt
for i in `seq 1 10`; 
do 
	OMP_NUM_THREADS=1 likwid-pin -c N:0 ./spatter -l $amg_size -t $amg_trace -q --nph -R 20 | grep OPENMP > tmp1.txt
	tail -n +2 papi_output.txt > tmp2.txt
	pr -w 180 -m -t tmp1.txt tmp2.txt > tmp3.txt
	#OMP_NUM_THREADS=1 likwid-pin -c N:0 ./spatter -l $amg_size -t ../traces/amg.pat -q --nph -R 20 | grep OPENMP | cut -f 10 -d' ' | sort -r | head -n 1 >> tmp2.txt
done;

echo -n "AMG $amg_size PAPI456 " >> $outfile
cat tmp3.txt | sort -nrk10 | head -n 1 | cut -f 4,10,11,12,13 -d' ' >> $outfile

rm -f $tmpfiles
