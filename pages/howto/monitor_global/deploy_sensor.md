---
title: "How to deploy HWPC-sensor to get hardware power information"
keywords: homepage
sidebar: home_sidebar 
permalink: howto_monitor_global/deploy_sensor.html
---

## Introduction

This tutorial presents you how to deploy a [power sensor](/hwpc.html) to acquire metrics about global power consumption of a node.

## Prerequisites
This tutorial assumes that:

- a mongoDB instance that is remotely accessible from all nodes to be monitored,
- CPUs of monitored node(s) must have an intel Sandy Bridge architecture or higher,
- monitored node(s) run a Linux distribution that is not hosted in a virtual environment,
- Docker is installed on the monitored node(s).

## Deploy the sensor

Before deploying the sensor, a MongoDB instance should be available. We assume the instance URI is `mongo://ADDR`.

Then, deploy the sensor as a Docker container with the following command:

	docker run --net=host --name powerapi-sensor --privileged -td -v /sys:/sys -v /var/lib/docker/containers:/var/lib/docker/containers:ro -v /tmp/powerapi-sensor-reporting:/reporting powerapi/hwpc-sensor -n $NAME -r "mongodb" -U "mongodb://ADDR" -D $DB -C $COLLECTION -s "rapl" -o -e RAPL_ENERGY_PKG
	
with: 

- `$NAME` : name of the sensor instance, if you use multiple sensors and connect them to one formula, this parameter must be different for each sensor.
- `$DB` : name of the mongodb database used to store the collected data
- `$COLLECTION` : name of the mongodb collection used to store the collected data

## Monitor more domains

The previous command line will only monitor the CPU socket power consumption

You can also monitor the following domains by adding additional parameter to the command line : 

- DRAM power consumption : add `-e RAPL_ENERGY_PKG` at the end of the command line
- Integrated graphics processing unit (on client architectures) : add `-e
  RAPL_ENERGY_GPU` at the end of the command line

Some domains may not be supported by your node. If you launch the sensor to
monitor domains that are not supported by your node, the sensor will crash with
a message indicating which event is not supported.

## Next step: deploy the formula

Metrics retrieved by the sensor need to be handle by a [RAPL formula](/howto_monitor_global/deploy_formula.html) to complete the deployment of the power meter.
