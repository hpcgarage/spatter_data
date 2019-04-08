#! /bin/sh

# Linux data-gathering commands; adjust as necessary for your platform.
#
# Be sure to remove any information from the output that would violate
# SC's double-blind review policies. 

SCRIPT='./'`basename "$0"`
USAGE='\nUsage: \n  '$SCRIPT' <system_name=ibmpower9>\n\n'

# Check arguments to script.
if [ $# -lt 1 ]; then
    echo -ne $USAGE
    exit
fi

#Each environment should go into a separate file
OUTFILE="exe_environments/sc19_env_$1.txt"


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

#Strip any full hostnames from system names; edit to add more domains
sed -i "s/cc.gatech.edu//g" ${OUTFILE}
