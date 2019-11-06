---
title: "How to deploy HWPC-sensor to get hardware power information"
keywords: homepage
sidebar: home_sidebar 
permalink: howto_deploy_hwpc_sensor.html
---

## Introduction

This tutorial presents you how to deploy a [power sensor](hwpc.html) to acquire metrics about global power consumption of a node.

## Prerequisites
This tutorial assumes that:

- a mongoDB instance that is remotely accessible from all nodes to be monitored,
- CPUs of monitored node(s) must have an intel Sandy Bridge architecture or higher,
- monitored node(s) run a Linux distribution that is not hosted in a virtual environment,
- Docker is installed on the monitored node(s).

## RAPL events

The global power consumption is reported the RAPL (*Running Average Power Limit*) interface.
This sensor can be used to monitor the power consumption of some specific RAPL domains 
(depending on your processor architecture), such as:

- Socket power consumption,
- DRAM power consumption (on server architectures),
- Integrated graphics processing unit (on client architectures).

You can list the available domains on your node with the command `perf list power`.

## Deploy the sensor

Before deploying the sensor, a MongoDB instance should be available. We assume the instance URI is `mongo://ADDR`.

Then, deploy the sensor as a Docker container with the following command:

	docker run --net=host --name powerapi-sensor --privileged -td -v /sys:/sys -v /var/lib/docker/containers:/var/lib/docker/containers:ro -v /tmp/powerapi-sensor-reporting:/reporting powerapi/hwpc-sensor -n $NAME -r "mongodb" -U "mongodb://ADDR" -D $DB -C $COLLECTION -s "rapl" -o -e $HARDWARE_1 -e $HARDWARE_2 ... -e $HARDWARE_N
	
with: 

- `$NAME` : name of the sensor, if you use multiple sensors and connect them to one formula, this parameter must be different for each sensor.
- `$DB` : name of the mongodb database used to store the collected data
- `$COLLECTION` : name of the mongodb collection used to store the collected data
- `$HARDWARE_N` : name of the monitored hardware : 

	- `RAPL_ENERGY_PKG` : to monitor CPU socket,
	- `RAPL_ENERGY_DRAM` : to monitor DRAM (server only),
	- `RAPL_ENERGY_GPU` : to monitor integrated graphics processing unit (client only).


## Next step: deploy the formula

Metrics retrieved by the sensor need to be handle by a [RAPL formula](howto_deploy_rapl_formula.html) to complete the deployment of the power meter.
