# Getting started

!!! info "Pre-Requisites"
    
    **In order to follow this tutorial, you will need several elements ready on
    the target server:  
    - A compatible processor  
    - A python installation ready  
    - Docker & Docker-Compose ready  
    - Root access**

!!! warning "Testing purpose tutorial"
    
    This quick Getting-Started will guide you to get a quick view of PowerAPI 
    capabilities.  
    To do so in a light way, **the final output displayed is not the 
    intended use of the tools for an everyday deployment**, you'll only get quick & concise 
    statistics on the tested period.

## Define elements to monitor

PowerAPI being a monitoring tool for energy consumption, we will need to define 
the necessary elements to monitor. 
In the testing archive, we will be able to see the consumption of the docker container by the default.
But if we want to monitor a specific process, we can use the Linux abstraction of [cGroups](https://www.redhat.com/sysadmin/cgroups-part-one).  

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

Only in the context of this testing archive, after the monitoring, you can use the following command to get a pretty print of the result directly inside the terminal.  

```sh
python3 pretty_print.py
```
