---
title: "How to deploy RAPL-Formula to compute hardware power information"
keywords: homepage
sidebar: home_sidebar 
permalink: howto_deploy_rapl_formula.html
---

## Introduction

This tutorial presents you how to deploy a formula : [RAPL-formula](rapl.html) to
compute power consumption estimation from data collected by an HWPC sensor (see
[this tutorial](howto_deploy_hwpc_sensor.html) to see how to deploy the HWPC sensor)

We describe how to deploy a RAPL-formula and connect to a mongodb database that
contains measure collected by a HWPC-sensor. The power consumption estimations
computed by the formula will be stored in another mongodb database. At the end,
we will see how to retrieve this data with the mongodb client.

## Deploy the RAPL-Formula

As explained [here](powerapi_howitworks.html#power-meter-architecture) The power
meter need two mongoDB databases. One to connect the formula to the sensor and
an other to store the power consumption information computed by the formula.

We assume that this two databases are hosted on the same mongoDB instance but
different instances could be used for each database. In the rest of its
tutorial, the URI of the mongoDB instance will be `mongo://ADDR`

You can launch the RAPL-formula with the following command : 

	docker run -td --net=host --name powerapi-formula powerapi/rapl-formula --input mongodb -u mongodb://ADDR -d $INPUT_DB -c $INPUT_COL --output mongodb -u mongodb://ADDR -d $OUTPUT_DB -c $OUTPUT_COL -s
	
with : 

- `$INPUT_DB` : mongodb database that store hwpc sensor data
- `$INPUT_COL` : mongodb collection that store hwpc sensor data
- `$OUTPUT_DB` : mongodb database that will store the power consumption estimation
- `$OUTPUT_COL`	: mongodb collection that will store the power consumption estimation

## Retrieve power consumption estimation with MongoDB client 

To access to the power consumption information computed by the power meter just
connect a mongo client to the mongoDB instance and retrieve the data of the
`power_consumption` collection of the `output_db` database.

Power information data are structured as this json format : 

	{
        "_id" : XXX # MongoDB object identifier (string)
        "timestamp" : YYY # timestamp of the power measure (iso date)
        "metadata" : {
                "socket" : "N", # socket identifier (int)
				"sensor" : hwpc sensor identifier (str)
        },
        "power" : Z.ZZZ # power consumption expressed in watts (float)
	}
	
For example to display a power consumption report with the mongo client :

	mongo ADDR
	use output_db
	db.power_consumption.findOne()
