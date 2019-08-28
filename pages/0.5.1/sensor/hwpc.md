---
title: "HWPC Sensor"
keywords: homepage
sidebar: home_sidebar 
permalink: 0.5.0/hwpc.html
summary: "The HWPC-Sensor (*Hardware Performance Counters Sensor*) read data from the hardware performance counters exposed by the processor." 
---

## Install and run

The HWPC sensor is deployed in a docker container. You can download it with : 

	docker pull powerapi/hwpc-sensor

To run the sensor use : 

	docker run --privileged --name hwpc-sensor -td \
             -v /sys:/sys \
             -v /var/lib/docker/containers:/var/lib/docker/containers:ro \
             -v /tmp/powerapi-sensor-reporting:/reporting \
             HWPC_DOCKER_IMAGE -n "SENSOR_NAME" -r "mongodb" -U "mongodb://MONGO_ADDRESS" -D "DATABASE_NAME" -C "COLLECTION_NAME" \
             -c "sys" -e "INSTRUCTIONS_RETIRED" \
             -c "cycles" -e "CYCLES" \
             -c "llc" -e "LLC_MISSES" \
             -c "rapl" -e "RAPL_ENERGY_CORES" -e "RAPL_ENERGY_PKG" -e "RAPL_ENERGY_GPU" -e "RAPL_ENERGY_DRAM"

This command monitors the following hardware performance counters:
``INSTRUCTIONS_RETIRED``, ``CYCLES``, ``LLC_MISSES``, ``RAPL_ENERGY_CORES``,
``RAPL_ENERGY_PKG``, ``RAPL_ENERGY_GPU``, ``RAPL_ENERGY_DRAM`` when available
and uploads the collected metrics into a MongoDB endpoint exposed at
``mongodb://MONGO_ADDRESS``, as a collection ``COLLECTION_NAME`` stored in the
database ``DATABASE_NAME``.

With : 

- `HWPC_DOCKER_IMAGE` :*HWPC-Sensor* docker image name
- `SENSOR_NAME`: Sensor name
- `MONGO_ADDRESS`: MongoDB server address
- `DATABASE_NAME`: MongoDB database name
- `COLLECTION_NAME`: MongoDB collection name

## Source

Source are available on [github](https://github.com/powerapi-ng/hwpc-sensor)
