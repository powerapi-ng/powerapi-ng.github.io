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
the necessary elements to monitor. An example is also given if you do not already 
have a process you wish to monitor.  

### Create a cGroup

We need a subset of running processes to be monitored. For this, we use the 
Linux abstraction of [cGroups](https://www.redhat.com/sysadmin/cgroups-part-one).  

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
within the HWPCReport Collection.  

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

From this archive, you will have all the necessary files to get started, let us break down each elements.  

### Archive content

```sh
|powerapi-stack/
|--docker-compose.yaml
|--configs.d/
|----hwpc-sensor-config.json
|----smartwatts-config.json
|--start.py
|--reports.d/
|----powerreports.csv
```

#### HWPC-Sensor Configuration

As described in the [HWPC-Sensor Documentation](./reference/sensors/hwpc-sensor.md#global-parameters) 
several parameters can be set, both globally and for specific Groups monitored. 
The provided docker-compose.yaml file use configuration files to set those parameters.  
An example configuration file for HWPC-Sensor is given below and available in the archive presented [above](./getting_started.md#preparation) :  

```json title="powerapi-stack/hwpc-sensor-config.json"

{
  "verbose": false,
  "frequency": 1000,
  "name": "hwpc-sensor",
  "cgroup_basepath": "/sys/fs/cgroup/perf_event",
  "system": {
    "type": "MONITOR_ALL_CPU_PER_SOCKET",
    "events": ["RAPL_ENERGY_PKG", "RAPL_ENERGY_DRAM"]
  },
  "container": {
    "type": "MONITOR_ALL_CPU_PER_SOCKET",
    "events": ["RAPL_ENERGY_PKG", "RAPL_ENERGY_DRAM"]
  },
  "output": {
    "type": "mongodb",
    "uri": "mongodb://mongodb:27017",
    "db": "powerapi",
    "collection": "HWPCReports"
  }
}
```

### SmartWatts Configuration

As described in the [SmartWatts Documentation](./reference/formulas/smartwatts.md#global-parameters) 
several parameters can be set for the Formulas. 
The provided docker-compose.yaml file use configuration files to set those parameters.  
An example configuration file for SmartWatts is given below and available in the archive presented [above](./getting_started.md#preparation) :  

```json title="powerapi-stack/smartwatts-config.json"
{
  "verbose": true,
  "stream": true,
  "input": {
    "puller": {
      "model": "HWPCReport",
      "type": "mongodb",
      "uri": "mongodb://127.0.0.1",
      "db": "powerapi",
      "collection": "HWPCReports"
    }
  },
  "output": {
    "pusher_power": {
      "type": "csv",
      "directory": "reports.d",
      "files": "powerreports.csv"
    }
  },
  "cpu-base-freq": 1900,
  "cpu-error-threshold": 2.0,
  "disable-dram-formula": true,
  "sensor-reports-frequency": 1000
}
```

## Turn the key 

Once all set, you shall be able to initiate the stack with :  

```sh
python3 start.py
```

