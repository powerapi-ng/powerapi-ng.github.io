---
title: "How to deploy HWPC-sensor to get hardware power information"
keywords: homepage
sidebar: home_sidebar 
permalink: howto_deploy_hwpc_sensor.html
---

## Introduction

This tutorial present you how to deploy a sensor : [HWPC Sensor](hwpc.html) to
retrieve information about global power consumption of a whole machine.

Sensors are the first part of a power meter, their goal is to retrieve raw
information correlated to power consumption. You need to deploy a formula to
compute power consumption from data retrieved by sensors (see
[here](howto_deploy_rapl_formula.html)).

## Prerequisites
This tutorial assumes that you have access to a mongoDB instance that is
remotely accessible by all nodes you want to monitor.

CPUs of Monitored nodes must have an intel Sandy Bridge architecture or higher.

The sensor must be run on a Linux operating system that is not on a virtual
environement.

## RAPL Events

The global power consumption are given by a CPU internal sensor : RAPL (Running
Average Power Limit).

RAPL sensor could be used to monitor some particular harwdware power consumption
(depend of you CPU architecture) such as :

- Socket power consumption
- DRAM power consumption
- Integrated graphics processing unit

You can list the hardware that you can monitor with the command `perf list power`

## Deploy the HWPC sensor

This section will show you how to launch the HWPC-sensor to monitor hardware
power consumption. You need a MongoDB instance to store the collected data. We
assume that the URI of this instance is `mongo://ADDR`

Deploy the sensor with docker with the following command line :

	docker run --net=host --name powerapi-sensor --privileged -td -v /sys:/sys -v /var/lib/docker/containers:/var/lib/docker/containers:ro -v /tmp/powerapi-sensor-reporting:/reporting powerapi/hwpc-sensor -n $NAME -r "mongodb" -U "mongodb://ADDR" -D $DB -C $COLLECTION -s "rapl" -o -e $HARDWARE_1 -e $HARDWARE_2 ... -e $HARDWARE_N
	
with : 

- `$NAME` : name of the sensor, if you use multiple sensors and connect them to one formula, this parameter must be different for each sensor.
- `$DB` : name of the mongodb database used to store the collected data
- `$COLLECTION` : name of the mongodb collection used to store the collected data
- `$HARDWARE_N` : name of the monitored hardware : 

	- RAPL_ENERGY_PKG : to monitor Socket
	- RAPL_ENERGY_DRAM : to monitor DRAM
	- RAPL_ENERGY_GPU : to monitor integrated graphics processing unit


## Next step : deploy the formula

Data retrieved by HWPC-sensor need to be handle by a RAPL formula, see [here](howto_deploy_rapl_formula.html) to complete the deployment of a whole power meter.
