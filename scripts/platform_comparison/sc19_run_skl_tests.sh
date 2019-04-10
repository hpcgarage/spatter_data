#!/bin/bash
#This script runs the uniform stride and random access tests used to generate the plots in Figures 3,4, and 7.

export OMP_PROC_BIND=master
export OMP_WAIT_POLICY=active
export OMP_NUM_THREADS=12
export OMP_PLACES=sockets

#Specify the name for your system and CPU/accelerator type; this is used to sort results
LONGNAME=skylar-skl
SHORTNAME=skl

###########Run the test scripts


#Run STREAM
./run-stream.sh $LONGNAME
./sg-sparse-roofline.sh openmp $SHORTNAME
./sg-rdm-roofline.sh openmp $SHORTNAME
#Sort results
#./organize-results.sh openmp $SHORTNAME skl
