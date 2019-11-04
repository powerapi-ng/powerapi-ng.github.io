---
title: "HWPC Sensor"
keywords: homepage
sidebar: home_sidebar 
permalink: hwpc.html
summary: "The HWPC-Sensor (*Hardware Performance Counters Sensor*) read data from the hardware performance counters exposed by the processor." 
---

HardWare Performance Counter (HWPC) Sensor is a tool that monitor the Intel CPU
performance counter and the power consumption of CPU.

## Prerequisites
Hwpc-sensor use the RAPL (Running Average Power Limit) technology to monitor CPU
power consumption. This technology is only available on Intel Sandy Bridge
architecture or
[higher](https://fr.wikipedia.org/wiki/Intel#Historique_des_microprocesseurs_produits).

The sensor use the **perf** API of the Linux kernel. It is only available on
Linux and need to have root access to be used.

The sensor couldn't be used in a virtual machine, it must access (via Linux
kernel API) to the real CPU register to read performance counter values.

## Installation

### Docker usage

You can directly use a docker container that contains the sensor with the
following command :

	docker pull powerapi/hwpc-sensor
	
###	From source
	
You can install hwpc-sensor from source

hwpc-sensor depends of the following packages 

- czmq library
- pfm4 library
- cmake
- bson library (if you use mongoDB as sensor output)
- mongoc library (if you use mongoDB as sensor output)

To compile the source code, run the following command (replace
`MONGO_DB_SUPPORT` with `ON` or `OFF` depend if you want to compile it with the
mongoDB support or not :

	git clone https://github.com/powerapi-ng/hwpc-sensor
	cd hwpc-sensor
	cmake -DWITH_MONGODB="MONGO_DB_SUPPORT" .
	make

it will produce an executable `hwpc-sensor`

## Usage Example

Here is an example of how to launch a sensor to monitor two performance counters
(`LLC_MISSES` and `CYCLES`) and the power consumption of the CPU socket. The
sensor is named **sensor_test**. The monitored value are stored on a mongoDB
database (uri: 127.0.0.1:1234, database : db1, collection: col1)

Docker usage : 

	docker run --privileged --name hwpc-sensor -td \
               -v /sys:/sys \
               -v /var/lib/docker/containers:/var/lib/docker/containers:ro \
               -v /tmp/powerapi-sensor-reporting:/reporting \
                  powerapi/hwpc-sensor -n sensor_test \ 
			       -c hwpc -e LLC_MISSES -e CYCLES \
			       -c rapl -e RAPL_ENERGY_PKG \
			       -r mongodb -U mongodb://127.0.0.1:1234 -D db1 -C col1
			 
Non docker usage : 

	sudo ./hwpc-sensor -n sensor_test -c hwpc -e LLC_MISSES -e CYCLES -c rapl -e RAPL_ENERGY_PKG \
	                   -r mongodb -U mongodb://127.0.0.1:1234 -D db1 -C col1


## Command Line Interface

This section presents each parameter from the sensor's command line interface

### Main Parameters

- `-n NAME` specify the sensor name. This name will be used as a key to identify
  the value reported by the sensor.

### Specify Performance Counter to monitor

Specify the events you want to monitor with the `-e EVENT_NAME` parameter. You
have to specify an event group for each group of events you want to monitor with
the `-c EVENT_GROUP_NAME` parameter. The `-c` parameter must be placed before
the events that are part of it.

Usage example : `hwpc-sensor ... -c GROUP1 -e GROUP1_EVENT1 -e GROUP1_EVENT2 -c
GROUP2 -e GROUP2_EVENT1 ...`

### Specify Power consumption monitoring

To make the sensor monitor CPU power consumption, you have to specify an event
group that will contains RAPL events. If you want to use the sensor with the
other **powerapi** tools, you have to name this group `rapl`.

The following events may be available depend on your CPU architecture: 

- `RAPL_ENERGY_PKG` : whole CPU socket power consumption
- `RAPL_ENERGY_DRAM` :RAM power consumption
- `RAPL_ENERGY_GPU` : CPU integrated graphics processing unit

Usage example : `hwpc-sensor ... -c rapl -e RAPL_ENERGY_PKG -e RAPL_ENERGY_GPU ...`

### Output Parameter

Hwpc-sensor could report performance counter and power consumption value in a
CSV file or in a mongoDB database

Use the `-r` parameter to specify output type : `mongodb` or `csv`

To use a mongodb output, you must configure how to access to the database with
the following parameters:

- `-U uri` : specify the URI of the mongoDB instance
- `-D DATABASE_NAME` : specify the name of the database where to store the reported
  values
- `-C COLLECTION_NAME` : specify the name of the collection where to store the
  reported values

Usage example : `hwpc-sensor ... -r mongodb -U mongodb://127.0.0.1:1234 -D db1 -C col1 ...` 

To use a csv output, you must indicate a directory where the csv files will be
created with the `-U` parameter. There is one csv file per event group.

Usage example : `hwpc-sensor ... -r csv -U /tmp/sensor_output/ ...`

### Docker usage

To use the docker container powerapi/hwpc-sensor, you have to launch it with the following parameters : 

	docker run --privileged --name hwpc-sensor -td \
             -v /sys:/sys \
             -v /var/lib/docker/containers:/var/lib/docker/containers:ro \
             -v /tmp/powerapi-sensor-reporting:/reporting \
             powerapi/hwpc-sensor ...

## Use Case

hwpc-sensor could be used to measure global power consumption with the **rapl-formula** see this [tutorial](/monitor_global_power_consumption)

## Source

Source are available on [github](https://github.com/powerapi-ng/hwpc-sensor)


