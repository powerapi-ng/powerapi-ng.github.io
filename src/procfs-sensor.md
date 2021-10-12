# Procfs-Sensor

The Proc Filesystem Sensor is a tool that monitor the CPU usage of cgroup via
the linux's proc filesystem.
It use `pidstat` to retreive the percentage of CPU usage of each process.
It then use the `/sys/fs/perf_event` directory to find the appartenance of
processes to cgroup.

The sensor need the cgroup version 1. The version 2 is not supported yet.
