#!/bin/bash

# Author: Patrick Lavin
# Information on which MSR to use and how to use it
# was taken from the following webpage. I have not double-
# checked this formation against the Intel docs.
# https://stackoverflow.com/questions/54753423/correctly-disable-hardware-prefetching-with-msr-in-skylake

# NOTE: Since this script modifies MSR values, it requires root access. Additionally, you will need to install
# the "msr-tools" package on Ubuntu systems and check that the msr module is loaded. Otherwise you will encounter
# errors like: "wrmsr: Command not found" if these tools are not installed and "wrmsr: open: No such file or directory"
# if the MSR module is not loaded.
# Ex: []~$ lsmod | grep msr //Check to see if the MSR module is loaded
# msr                    16384  0

# This script appears to work well on Broadwell and Skylake systems.


if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

if [ "$#" -ne 1 ]; then
    echo "Please supply a command to run with prefecthing off"
    echo "Usage: sudo ./noprefetch \"command and args in quotes\""
    exit
fi

# Disable prefetching
wrmsr -a 0x1a4 15

# Run Command
sudo -u $USER env "LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/intel/lib/intel64/" $1

# Re-enable prefetching
wrmsr -a 0x1a4 0
