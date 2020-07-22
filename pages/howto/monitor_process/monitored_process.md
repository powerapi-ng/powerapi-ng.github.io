---
title: "Select process to monitor"
keywords: homepage
sidebar: home_sidebar 
permalink: howto_monitor_process/monitored_process.html
---

In this part, we will se wich process are monitored by default and how to select process to monitor

# Process monitored by default
By default, process which are member of cgroup under `perf_event` controller are monitored.

This means that the following groups of process are monitored : 
- docker container
- kubernetes pod
- lxc container
- virtual machine that use libvirt API

# Select a process to monitor

if you want to monitor a specific process (or group of process), you have to
create a cgroup with `perf_event` controller and add the process you want to
monitor to this cgroup

you can easly do this with the following command :

- to create the cgroup : `cgcreate -g perf_event:new_cgroup_name`


with `new_cgroup_name` the name of the cgroup you want to create (this will be the name wich will identify power consumption of you process)


- to add your process to the newly created cgroup : `cgclassify -g perf_event:new_cgroup_name PID`


with `PID`, the pid of the process you want to monitor. If you want to monitor a program composed of many process, replace `PID` with `$(pidof program_name)`

## Next step: deploy the sensor

When you have selected the process you want to monitor, you could deploy the
sensor following [this tutorial](/howto_monitor_process/deploy_sensor.html).

Begin to monitor a process after lauching the sensor is not a problem. When you
create a new cgroup, the sensor will automatically add it to the monitored
cgroup
