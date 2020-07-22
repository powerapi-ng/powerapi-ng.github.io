---
title: "Deploying smartwatts formula to compute process power consumption"
keywords: homepage
sidebar: home_sidebar 
permalink: howto_monitor_process/deploy_formula.html
---

## Introduction

This tutorial describes how to deploy the [Smartwatts formula](/smartwatts.html) to estimate process power consumption from metrics collected by the [sensor](/howto_monitor_process/deploy_sensor.html).

We describe how to deploy a smartwatts formula that connects to a MongoDB instance to read the raw metrics and to store the estimated values.

## Deploy the smartwatts formula

The default architecture of PowerAPI assumes the availability of [two MongoDB collections](/powerapi_howitworks.html#power-meter-architecture) to feed the formula from sensor metrics and to report the power consumption estimations.

We assume that these two collections are hosted on the same mongoDB instance, but different instances can be used.
In the following, the MongoDB instance URI is `mongo://ADDR`.

You can deployed the smartwatts formula with the following command:

	docker run -td --net=host --name powerapi-formula powerapi/smartwatts-formula \
	           -s \
	           --input mongodb --model HWPCReport \
	                           -u mongodb://ADDR -d $INPUT_DB -c $INPUT_COL \
	           --output mongodb --name power --model PowerReport \
	                            -u mongodb://ADDR -d $OUTPUT_DB -c $OUTPUT_COL \
	           --output mongodb --name formula --model FormulaReport \
	                            -u mongodb://ADDR -d $OUTPUT_DB -c frep \
	           --formula smartwatts --cpu-ratio-base $BASE_CPU_RATIO \
	                                --cpu-ratio-min $MIN_CPU_RATIO \
	                                --cpu-ratio-max $MAX_CPU_RATIO \
	                                --cpu-error-threshold 2.0 \
	                                --dram-error-threshold 2.0 \
	                                --disable-dram-formula
{: class="copyable"}

with:

- `$INPUT_DB` : MongoDB database that stores the input sensor metrics,
- `$INPUT_COL` : MongoDB collection that store the input sensor metrics,
- `$OUTPUT_DB` : MongoDB database that will store the output power consumption estimations,
- `$OUTPUT_COL`	: MongoDB collection that will store the output power consumption estimations.
- `$XXX_CPU_RATIO` : see section [CPU Ratio](/howto_monitor_process/deploy_formula.html#cpu-ratio) below

if you are also monitoring dram power consumption of your process (see [here](/howto_monitor_process/deploy_sensor.html#monitor-dram-domains)), you have to remove the last parameter : `--disable-dram-formula`

### CPU Ratio
You have to setup the formula with the frequency of the monitored cpu :

- `$BASE_CPU_RATIO` : divide the base CPU frequency (in MHz) by 100 to obtain the base CPU ratio. You can find the CPU frequency on [intel website](https://ark.intel.com/content/www/fr/fr/ark.html#@Processors)
- `$MIN_CPU_RATIO` : divide the minimum CPU frequency (in MHz) by 100 to obtain the min cpu ratio. You can find the minimum CPU frequency with the command `lscpu` ("CPU min MHz" line)
- `$MAX_CPU_RATIO` : divide the maximum CPU frequency (in MHz) by 100 to obtain the max cpu ratio. You can find the maximum CPU frequency with the command `lscpu` ("CPU max MHz" line)

For example for an **Intel(R) Core(TM) i7-8650U** CPU, we find a base frequency of 1900 MHz on the intel website.

The `lscpu` command returns the following output :

```
Architecture:                    x86_64
CPU op-mode(s):                  32-bit, 64-bit
Byte Order:                      Little Endian
Address sizes:                   39 bits physical, 48 bits virtual
CPU(s):                          8
On-line CPU(s) list:             0-7
Thread(s) per core:              2
Core(s) per socket:              4
Socket(s):                       1
NUMA node(s):                    1
Vendor ID:                       GenuineIntel
CPU family:                      6
Model:                           142
Model name:                      Intel(R) Core(TM) i7-8650U CPU @ 1.90GHz
Stepping:                        10
CPU MHz:                         799.991
CPU max MHz:                     4200.0000
CPU min MHz:                     400.0000
BogoMIPS:                        4201.88
Virtualization:                  VT-x
L1d cache:                       128 KiB
L1i cache:                       128 KiB
L2 cache:                        1 MiB
L3 cache:                        8 MiB
NUMA node0 CPU(s):               0-7
Vulnerability L1tf:              ...
Vulnerability Mds:               ...
Vulnerability Meltdown:          ...
Vulnerability Spec store bypass: ...
Vulnerability Spectre v1:        ...
Vulnerability Spectre v2:        ...
Flags:                           ...
```

we need the following lines : 

```
CPU max MHz:                     4200.0000
CPU min MHz:                     400.0000
```

with these information, we can deduce the formula parameters :

	docker run powerapi/smartwatts-formula \
	          ...
	           --formula smartwatts --cpu-ratio-base 19
	                                --cpu-ratio-min 4
	                                --cpu-ratio-max 42
									...

## Retrieve power consumption estimation with MongoDB client

To access to the power consumption estimations, you can connect a mongo client to the mongoDB instance and retrieve the estimations from the `$OUTPUT_COL` collection of the `$OUTPUT_DB` database.

Power estimations are structured as JSON documents:

	{
        "_id" : ..., # MongoDB object identifier (string)
        "timestamp" : ..., # timestamp of the power measure (iso date)
	    "sensor" : ..., # hwpc sensor identifier (str)
	    "target": ..., # name of the monitored process,  (str)
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


## Next step: Visualisation

If you want tu use a grafana instance to visualize the power consumption estimation, follow this [tutorial](/howto_monitor_process/connect_to_grafana.html)
