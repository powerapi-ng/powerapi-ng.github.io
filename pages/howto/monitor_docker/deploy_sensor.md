---
title: "How to deploy HWPC-sensor to get docker containers power information"
keywords: homepage
sidebar: home_sidebar 
permalink: howto_monitor_docker/deploy_sensor.html
---

## Introduction

This tutorial presents you how to deploy a [hwpc sensor](/hwpc.html) to acquire data relative to docker containers power consumption.

## Prerequisites
This tutorial assumes that:

- a mongoDB instance that is remotely accessible from all nodes that are monitored,
- CPUs of monitored node(s) must have an intel Sandy Bridge architecture or higher,
- monitored node(s) run a Linux distribution that is not hosted in a virtual environment,
- Docker is installed on the monitored node(s),
- Each container must have a different name even if they are not hosted in the same node.

## Deploy the sensor

Before deploying the sensor, a MongoDB instance should be available. We assume the instance URI is `mongodb://ADDR`.

Then, deploy the sensor as a Docker container with the following command:

	docker run --net=host --privileged --name powerapi-sensor -d \
	           -v /sys:/sys -v /var/lib/docker/containers:/var/lib/docker/containers:ro \
	           -v /tmp/powerapi-sensor-reporting:/reporting \
			   powerapi/hwpc-sensor:latest \
			   -n "$NAME" \
			   -r "mongodb" -U "mongodb://ADDR" -D "$DB" -C "$COLLECTION" \
			   -s "rapl" -o -e "RAPL_ENERGY_PKG" \
			   -s "msr" -e "TSC" -e "APERF" -e "MPERF" \
			   -c "core" -e "CPU_CLK_THREAD_UNHALTED:REF_P" -e "CPU_CLK_THREAD_UNHALTED:THREAD_P" \
	                     -e "LLC_MISSES" -e "INSTRUCTIONS_RETIRED"
{: class="copyable"}

with:

- `$NAME` : name of the sensor instance, if you use multiple sensors and connect them to one formula, this parameter must be different for each sensor.
- `$DB` : name of the mongodb database used to store the collected data
- `$COLLECTION` : name of the mongodb collection used to store the collected data

{% include warning.html content="Don't use the sensor outside of its docker container.<br/> Subtle bugs could happen due to compilation or execution environment if you compile and run the sensor by your own." %}

## Monitor DRAM domains

The previous command line will only give you data relative to containers power consumption on CPU socket

On Xeon architecture, you can also get data relative to power consumption on DRAM domain. To enable this features, add the parameter `-e "RAPL_ENERGY_DRAM"` in the previous command line just after `-s "rapl" -o -e "RAPL_ENERGY_PKG"`

## Next step: deploy the formula

Data retrieved by the sensor need to be handle by a [smartwatts formula](/howto_monitor_docker/deploy_formula.html) to complete the deployment of the power meter.
