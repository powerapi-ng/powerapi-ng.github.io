---
title: "Deploying the RAPL formula to report global power consumption"
keywords: homepage
sidebar: home_sidebar 
permalink: howto_monitor_global/deploy_formula.html
---

## Introduction

This tutorial describes how to deploy the [RAPL formula](/rapl.html) to estimate power consumption from metrics collected by the [sensor](/howto_monitor_global/deploy_sensor.html).

We describe how to deploy a RAPL formula that connects to a MongoDB instance to read the raw metrics and to store the estimated values.

## Deploy the RAPL formula

The default architecture of PowerAPI assumes the availability of [two MongoDB collections](/powerapi_howitworks.html#power-meter-architecture) to feed the formula from sensor metrics and to report the power consumption estimations.

We assume that these two collections are hosted on the same mongoDB instance, but different instances can be used.
In the following, the MongoDB instance URI is `mongo://ADDR`.

You can deployed the RAPL formula with the following command: 

	docker run -td --net=host --name powerapi-formula powerapi/rapl-formula \
	           -s \
	           --input mongodb -u mongodb://ADDR -d $INPUT_DB -c $INPUT_COL \
	           --output mongodb -u mongodb://ADDR -d $OUTPUT_DB -c $OUTPUT_COL
{: class="copyable"}

with: 

- `$INPUT_DB` : MongoDB database that stores the input sensor metrics,
- `$INPUT_COL` : MongoDB collection that store the input sensor metrics,
- `$OUTPUT_DB` : MongoDB database that will store the output power consumption estimations,
- `$OUTPUT_COL`	: MongoDB collection that will store the output power consumption estimations.

## Retrieve power consumption estimation with MongoDB client 

To access to the power consumption estimations, you can connect a mongo client to the mongoDB instance and retrieve the esimtations from the `$OUTPUT_COL` collection of the `$OUTPUT_DB` database.

Power estimations are structured as JSON documents: 

	{
        "_id" : XXX # MongoDB object identifier (string)
        "timestamp" : YYY # timestamp of the power measure (iso date)
        "metadata" : {
                "socket" : "N", # socket identifier (int)
				"sensor" : hwpc sensor identifier (str)
        },
        "power" : Z.ZZZ # power consumption expressed in watts (float)
	}

For example, to display a power consumption report from the mongo client, execute:

	mongo ADDR
	use output_db
	db.power_consumption.findOne()
{: class="copyable"}

## Next step: Visualisation

If you want tu use a grafana instance to visualize the power consumption estimation, follow this [tutorial](/howto_monitor_global/connect_to_grafana.html)

