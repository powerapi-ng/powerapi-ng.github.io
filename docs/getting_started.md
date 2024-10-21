# Getting started

In this tutorial, we will guide you through the first steps to get started with PowerAPI.
The objective is to get a quick view of the capabilities of PowerAPI, by monitoring a process and getting a quick glimpse at the energy consumption.
A few things are required before we start : 

- A compatible processor, you can see the compatible CPU architecture [here](./reference/sensors/hwpc-sensor.md#) and you can look on the following pages to find your CPU architecture :  
    * For [Intel Processor](https://en.wikipedia.org/wiki/List_of_Intel_processors)  
    * For [Intel Xeon Processor](https://en.wikipedia.org/wiki/List_of_Intel_Xeon_processors)  
    * For [AMD Processor](https://en.wikipedia.org/wiki/Table_of_AMD_processors)  
- A python installation ready
- Docker & Docker-Compose ready
- Root access

The first step of the tutorial will be to define the elements to monitor. 
In the testing archive, we will be able to see the consumption of the docker container by the default.
So feel free to skip directly to the [preparation part](#preparation) if you don't want to monitor a specific process.

## Define elements to monitor

PowerAPI being a monitoring tool for energy consumption, we will need to define 
the necessary elements to monitor.
To do so we can use the Linux abstraction of [cGroups](https://www.redhat.com/sysadmin/cgroups-part-one).  

### Create a cGroup

In order to create a cGroup, the following command can be used from CLI :  

```sh
cgcreate -g perf_event:new_cgroup_name
```

Check [here](./reference/cgroup/cgroup_v1_activation.md) if you have trouble 
creating the cgroup.  

### Add processes to the group

Once the group created, we need to fill it with processes to be monitored. 
To do so, you can use the following :  

```sh
cgclassify -g perf_event:new_cgroup_name PID
```

with `PID`, the pid of the process you want to monitor. If you want to monitor a
process composed of many processes, replace PID with `$(pidof process_name)`.

### Installing a process to monitor

[stress-ng](https://wiki.ubuntu.com/Kernel/Reference/stress-ng) can be used to 
generate load on one's system.  
An example usage, once installed :  

```sh  
cgcreate -g perf_event:stress-ng-cgroup
stress-ng --cpu 1 --timeout 5m
cgclassify -g perf_event:stress-ng-cgroup $!
```

## Which components to get a complete stack  

If you wish to get started as soon as possible, the following archive will allow you to deploy the following elements :  

1. A MongoDB instance to store the [Sensor](./reference/sensors/hwpc-sensor.md)
Reports

3. An [HWPC-Sensor](./reference/sensors/hwpc-sensor.md) that outputs its 
[HWPCReports](./reference/reports/report.md#HWPCReport) in a MongoDB Database, 
within the HWPCReport Collection

4. A [SmartWatts](./reference/formulas/smartwatts.md) that streams the 
[HWPCReports](./reference/reports/report.md#HWPCReport) from the MongoDB 
Database Collection, processes it and outputs its 
[PowerReports](./reference/reports/report.md#PowerReports) as CSV files for a 
quick glimpse 

## Preparation

You can download the archive using :   

```sh 
wget "https://github.com/powerapi-ng/powerapi-ng.github.io/tree/master/examples/powerapi-stack.zip"
unzip powerapi-stack.zip && cd powerapi-stack
```

From this archive, you will have all the necessary files to get started, let us break down each element.  

### Archive content

```sh
|getting_started/
|--csv/
|--fomula/
|----smartwatts-mongodb-csv.json
|--sensor/
|----hwpc-mongodb.json
|--start.sh
|--start.py
|--pretty_print.py
|--docker-compose.yaml
|--.env
```

#### HWPC-Sensor and SmartWatts Configuration

As described in the [HWPC-Sensor Documentation](./reference/sensors/hwpc-sensor.md#global-parameters) and in the [SmartWatts Documentation](./reference/formulas/smartwatts.md#global-parameters) 
several parameters can be set, both globally and for specific Groups monitored for the sensor or the formula.

The provided docker-compose.yaml file use configuration files and the **.env** to set those parameters.
You can find example of both those configuration files in the archive under the **formula** and **sensor** directories.


## Turn the key 

Once all set, you shall be able to initiate the stack with :  

```sh
python3 start.py
```

After the 2 minutes of monitoring, you will be able to see the result inside the **csv** directory.
If you have trouble understanding the output, you can read the [Power Report documentation](./reference/reports/reports.md#power-Reports).

!!! info "Quick results overview"
    Only in the context of this testing archive, after the monitoring, you can use the following command to get a pretty print of the result directly inside the terminal.  

    ```sh
    python3 pretty_print.py
    ```
