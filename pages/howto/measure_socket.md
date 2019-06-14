---
title: "How to monitor power consumption of a socket"
keywords: homepage
sidebar: home_sidebar 
permalink: howto_monitor_socket.html
---

## Introduction

This tutorial presents how to assemble a formula (RAPL-formula) and a sensor
(HWPC-sensor) to build a power meter that monitor the power consumption of each
CPU socket.

First of all, we describe the power meter that we want to build. Then, we
describe how to deploy the power meter's component and how to connect
them. Each component could be deployed with docker or directly by installing it
on the system.


## Compatible Architecture

The power meter will use hardware counters that exist only on Intel CPU with
Sandy Bridge architecture or higher. The power meter can't be used without
theses counters.

## Power meter description

Power meter estimations are based on the Running Average Power Limit (RAPL)
technology. RAPL provide a set of hardware counters that report data about the
current energy consumption of each CPU socket. The power meter use the
HWPC-sensor to collect these data and send them to the RAPL-formula to compute
the current energy consumption of monitored sockets.

Each component of the power meter could be hosted on a different machine. In
this tutorial, we assume that each component are hosted on the same machine.

## Data and database

As explained [here](powerapi_howitworks.html#power-meter-architecture) The power
meter need two mongoDB databases to connect the formula to the sensor and to
store the power consumption information computed by the formula.

We assume that this two databases are hosted on the same mongoDB instance but
different instances could be used for each database. In the rest of its
tutorial, the URI of the mongoDB instance will be `mongo://ADDR`

The first database (that connect the formula and the sensor) will be called
`connection_db` and the data will be store on the `hwrep` collection.
  
The second database (that store power consumption computed by the formula) will
be called `output_db` and data will be stored on the `power_consumption`
collection.

## Get power meter result

To access to the power consumption information computed by the power meter just
connect a mongo client to the mongoDB instance and retrieve the data of the
`power_consumption` collection of the `output_db` database.

Power information data are structured as this json format : 


	{
        "_id" : XXX # MongoDB object identifier (string)
        "timestamp" : YYY # timestamp of the power measure (iso date)
        "metadata" : {
                "socket" : "N", # socket identifier (int)
        },
        "power" : Z.ZZZ # power consumption expressed in watts (float)
	}
	
For example to display a power consumption report with the mongo client :

	mongo ADDR
	use output_db
	db.power_consumption.findOne()


## Deployment with docker

This section present how to deploy and connect each component of the power
meter with docker. You will see how to : 

- deploy a mongoDB instance in a docker container
- deploy the HWPC-sensor in a docker container and connect it to the mongoDB instance
- deploy the RAPL-formula in a docker container and connect it to the mongoDB instance

### Setup docker environment

Download components image : 

	docker pull powerapi/hwpc-sensor
	docker pull powerapi/rapl-formula
	docker pull mongo

Setup a docker network that will be used to connect each containers

	docker network create powerapi
	
### Launch the different component

Launch the mongoDB instance : 

	docker run -td --name powerapi-mongo --net=powerapi -p 27017:27017 mongo
	
Launch the sensor :

	docker run --net=powerapi --privileged --name powerapi-sensor -td -v /sys:/sys -v /var/lib/docker/containers:/var/lib/docker/containers:ro -v /tmp/powerapi-sensor-reporting:/reporting powerapi/hwpc-sensor -n "test-sensor" -r "mongodb" -U "mongodb://powerapi-mongo" -D "connection_db" -C "hwrep" -s "rapl" -o -e "RAPL_ENERGY_CORES" -e "RAPL_ENERGY_PKG" -e "RAPL_ENERGY_GPU"
	
Launch the formula : 

	docker run -td --net=powerapi --name powerapi-formula powerapi/rapl-formula --input mongodb -u mongodb://powerapi-mongo -d connection_db -c hwrep --output mongodb -u mongodb://powerapi-mongo -d output_db -c power_consumption -s
	
## Deployment without docker

This section present how to deploy and connect each component of the power
meter without docker, by installing each of them on the monitored machine. You
will see how to :

- compile the HWPC-sensor and connect it to an existing mongoDB instance
- install the RAPL-formula and connect it to an existing mongoDB instance
- launch the sensor and the formula from the command line

### Prerequisites

- python 3.7
- pip
- a mongoDB instance runing and accessible from the address `mongodb://ADDR`
- root privilege to launch the sensor

### Component installation

install the sensor from sources

	git clone https://github.com/powerapi-ng/hwpc-sensor.git
	cd hwpc-sensor
	cmake .
	make
	
install the RAPL-formula
	
	pip3 install rapl-formula
	
### Launch the different component

On the HWPC-sensor repository launch the sensor : 

	sudo ./hwpc-sensor -n "sensor" -r "mongodb" -U "mongodb://ADDR" -D "connection_db" -C "hwrep" -s "rapl" -o -e "RAPL_ENERGY_CORES" -e "RAPL_ENERGY_PKG" -e "RAPL_ENERGY_GPU" &
	
launch the formula

	python3 -m rapl_formula --input mongodb -u mongodb://ADDR -d connection_db -c hwrep --output mongodb -u mongodb://ADDR -d output_db -c power_consumption -s
