#!/bin/bash

cmd="icc -o new-stream stream.c -DSTREAM_ARRAY_SIZE=70000000 -Ofast -qopenmp"

echo "Compiling with \"${cmd}\""
icc -o new-stream stream.c -DSTREAM_ARRAY_SIZE=70000000 -Ofast -qopenmp > /dev/null

echo "1 thread: "
OMP_NUM_THREADS=1 likwid-pin -c N:0 ./new-stream | grep -A 4 "Function"

echo "24 Threads: "
likwid-pin -c N:0-23 ./new-stream | grep -A 4 "Function"
