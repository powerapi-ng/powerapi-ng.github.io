---
title: "Deploying smartwatts formula to compute docker containers power consumption"
keywords: homepage
sidebar: home_sidebar 
permalink: howto_monitor_docker/deploy_formula.html
---

## Introduction

This tutorial describes how to deploy the [Smartwatts formula](/smartwatts.html) to estimate docker container power consumption from metrics collected by the [sensor](/howto_monitor_docker/deploy_sensor.html).

We describe how to deploy a smartwatts formula that connects to a MongoDB instance to read the raw metrics and to store the estimated values.

## Deploy the RAPL formula

The default architecture of PowerAPI assumes the availability of [two MongoDB collections](/powerapi_howitworks.html#power-meter-architecture) to feed the formula from sensor metrics and to report the power consumption estimations.

We assume that these two collections are hosted on the same mongoDB instance, but different instances can be used.
In the following, the MongoDB instance URI is `mongo://ADDR`.

You can deployed the RAPL formula with the following command:

	docker run -td --net=host --name powerapi-formula powerapi/smartwatts-formula \
	           -s \
	           --input mongodb --model HWPCReport \
	                           -u mongodb://ADDR -d $INPUT_DB -c $INPUT_COL \
	           --output mongodb --name power --model PowerReport \
	                            -u mongodb://ADDR -d $OUTPUT_DB -c $OUTPUT_COL \
	           --output mongodb --name formula --model FormulaReport \
	                            -u mongodb://ADDR -d $OUTPUT_DB -c frep \
	           --formula smartwatts --cpu-ratio-base $CPU_RATIO \
	                                --cpu-error-threshold 2.0 \
	                                --dram-error-threshold 2.0 \
	                                --disable-dram-formula
{: class="copyable"}

with:

- `$INPUT_DB` : MongoDB database that stores the input sensor metrics,
- `$INPUT_COL` : MongoDB collection that store the input sensor metrics,
- `$OUTPUT_DB` : MongoDB database that will store the output power consumption estimations,
- `$OUTPUT_COL`	: MongoDB collection that will store the output power consumption estimations.
- `$CPU_RATIO` : CPU base ratio : multiply the base CPU frequency by 10 to obtain the CPU ratio. You can find the CPU frequency on [intel website](https://ark.intel.com/content/www/fr/fr/ark.html#@Processors)

if you are also monitoring dram power consumption of your docker containers (see [here](/howto_monitor_docker/deploy_sensor.html#monitor-dram-domains)), you have to remove the last parameter : `--disable-dram-formula`

## Retrieve power consumption estimation with MongoDB client

To access to the power consumption estimations, you can connect a mongo client to the mongoDB instance and retrieve the estimations from the `$OUTPUT_COL` collection of the `$OUTPUT_DB` database.

Power estimations are structured as JSON documents:

	{
        "_id" : ..., # MongoDB object identifier (string)
        "timestamp" : ..., # timestamp of the power measure (iso date)
	    "sensor" : ..., # hwpc sensor identifier (str)
	    "target": ..., # name of the monitored docker container,  (str)
        "power" : ..., # power consumption expressed in watts (float)
        "metadata" : {
                "socket" : ..., # CPU socket identifier (int)
                "scope": ..., # domain where the power consumption was measured (dram or cpu)
        },
	}

For example, to display a power consumption report from the mongo client, execute:

	mongo ADDR
	use $OUTPUT_DB
	db.$OUTPUT_COL.findOne()
{: class="copyable"}

<!-- ### About target names -->

<!-- Target attribute is usually the name of a monitored docker container but smartwatts also monitors other target than docker container such as : -->

<!-- - **rapl** : the power consumption of the rapl target is the global power consumption of the domain scope (cpu or dram) -->
<!-- - **global** :  -->

## Next step: Visualisation

If you want tu use a grafana instance to visualize the power consumption estimation, follow this [tutorial](/howto_monitor_docker/connect_to_grafana.html)
