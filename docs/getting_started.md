# Getting started

If you want to monitor the energy consumption of your process we have some
ready-to-use tools

???+ info "Source and Destination"
    In order to use any Formula, you need to run a Source and a Destination. The former is used by a Sensor to store metrics. The later allows the Formula to make available the estimations. For starting, you can use [MongoDB](https://hub.docker.com/_/mongo) as Source and [InfluxDB:1.8](https://hub.docker.com/_/influxdb) as Destination by installing them as Docker containers.
    For more details about Sources and Destinations please check this [section](reference/database/sources_destinations.md).


## **RAPL Formula**

!!! note ""
    for monitoring the energy consumption of your device

RAPL Formula is made for tracking the energy consumption of your machine.
To install RAPL Formula on a baremetal server or a PC run [the following
script](script/rapl_install.sh) in a Terminal.

The script explains what it will do and then pauses before it does it.

Please notice that you need a **Linux distribution** in order to use the HWPC Sensor installed by the script as
well as a **comptible Intel** (Sandy Bridge and newer) or **AMD Processor** (Zen). **Power/ARM/RISCV are not supported** architectures. HWPC Sensor will **not work on a Virtual Machine**. However, you can install the Formula by hand in a Virtual Machine if need it.

## **SmartWatts Formula**

!!! note ""
    for monitoring the energy consumption of your process

Smartwatts is made for tracking the energy consumption of processes on a
machine.
To install Smartwatts on a baremetal server or a PC run [the following
script](script/smartwatts_install.sh) in a Terminal.

The script explains what it will do and then pauses before it does it.

Please notice that you need a **Linux distribution** in order to use the HWPC Sensor installed by the script as
well as a **comptible Intel** (Sandy Bridge and newer) or **AMD Processor** (Zen). **Power/ARM/RISCV are not supported** architectures. HWPC Sensor will **not work on a Virtual Machine**. However, you can install the Formula by hand in a Virtual Machine if need it.



#### CGroups
If you need to monitor a process or a group of process via SmartWatts, please follow this [tutorial](reference/cgroup/cgroup.md). Please notice that **cgroup V1** is required for HWPC Sensor. If you need to enable this `cgroup` version please follow this [tutorial](reference/cgroup/cgroup_v1_activation.md).    

<!---
## **Jouleit**

!!! note ""
    for mesuring the energy consumption of a program

Jouleit is made for tracking the energy consumption of a program.
Jouleit need `gawk` to run.
You can get the script from the [github repository](https://github.com/powerapi-ng/jouleit)
Start jouleit by using `./jouleit.sh cmd`.
-->
