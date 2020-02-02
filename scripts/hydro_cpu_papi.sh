# Make sure to set the following two environment variables appropaitely
# You can set them here or on the command line
# DATA=$HOME/spatter_data
# ARCH=bdw
# NCPUS=12

# Notes on the hydro512-2.json file
# THe first test the the natural ordering
# The tests after that are block size 4, 8, ... 256.
# For a domain of size 512^3, block size 512 is the same as the
# natural ordering
# Block size 2 is the same as block size 1.

if [ -z "$DATA" ];
then
    echo "Please set the location of spatter_data";
    exit;
else
    JSON=$DATA/json/hydro512-2.json
    echo "Running with the json file: $JSON"
fi

if [ -z "$ARCH" ];
then
    echo "Please set the architecture in ARCH";
    exit;
else
    OUT=./hydro512-2_$ARCH.txt
    echo "The output will be written to: $OUT"
fi

if [ -z "$NCPUS" ];
then
    echo "Please set the the number of cpus in NCPUS";
    exit;
else
    echo "Running on $NCPUS CPUs"
fi

echo -n "Running Spatter... "

likwid-pin -c N:0-$((NCPUS-1)) -q ./spatter -pFILE=$JSON --papi=perf::L1-DCACHE-LOADS,perf::L1-DCACHE-LOAD-MISSES,perf::LLC-LOADS,perf::LLC-LOAD-MISSES > $OUT

echo "DONE"
