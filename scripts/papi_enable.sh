# This script will disable the kernel being paranoid about using performance counters
# Use this to fix papi_avail returning 0 available events

# Refernce: https://stackoverflow.com/a/48499004
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi
sh -c 'echo -1 >/proc/sys/kernel/perf_event_paranoid'
