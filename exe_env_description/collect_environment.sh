#! /bin/sh

# Linux data-gathering commands; adjust as necessary for your platform.
# Adapted from the SC environment collection script.

SCRIPT='./'`basename "$0"`
USAGE='\nUsage: \n  '$SCRIPT' <system_name=ibmpower9>\n\n'

# Check arguments to script.
if [ $# -lt 1 ]; then
    echo -ne $USAGE
    exit
fi

#Each environment should go into a separate file
OUTFILE="exe_environments/spatter_env_$1.txt"


env | sed "s/$USER/USER/g"
set -x
lsb_release -a &>> ${OUTFILE}
uname -a &>> ${OUTFILE}
(lscpu || cat /proc/cpuinfo) &>> ${OUTFILE}
cat /proc/meminfo &>> ${OUTFILE}
inxi -F -c0 &>> ${OUTFILE}
lsblk -a &>> ${OUTFILE}
lsscsi -s &>> ${OUTFILE}
module list &>> ${OUTFILE}
nvidia-smi &>> ${OUTFILE}
(lshw -short -quiet -sanitize || lspci) | cat &>> ${OUTFILE}

# Strip any full hostnames from system names; edit to add more domains
# This example removes gatech.edu from any hostnames for instance.
sed -i "s/gatech.edu//g" ${OUTFILE}
