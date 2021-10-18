# How to create a cgroup

If you want to monitor a specific process (or group of process), you have to
create a cgroup with `perf_event` controller and add the process you want to
monitor to this cgroup

You can easly do this with the following command :

- to create the cgroup : `cgcreate -g perf_event:new_cgroup_name`

with `new_cgroup_name` the name of the cgroup you want to create (this will be the name wich will identify power consumption of you process)

- to add your process to the newly created cgroup : `cgclassify -g perf_event:new_cgroup_name PID`

with `PID`, the pid of the process you want to monitor. If you want to monitor a
program composed of many process, replace PID with `$(pidof program_name)`
