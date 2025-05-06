# Getting started

In this tutorial, we will guide you through the first steps to get started with PowerAPI.
The objective is to get a quick view of the capabilities of PowerAPI.
A few things are required before we start: 

- A compatible processor (you can see the compatible CPU architecture [here](./reference/sensors/hwpc-sensor.md#)), and you can look on the following pages to find your CPU architecture:  
    * For [Intel Processor](https://en.wikipedia.org/wiki/List_of_Intel_processors)  
    * For [Intel Xeon Processor](https://en.wikipedia.org/wiki/List_of_Intel_Xeon_processors)  
    * For [AMD Processor](https://en.wikipedia.org/wiki/Table_of_AMD_processors)  
- Docker & Docker-Compose ready (refer to [this official documentation](https://docs.docker.com/engine/install/) and the [post-install steps](https://docs.docker.com/engine/install/linux-postinstall/) if needed !)
- Root access

## Which components to get a complete stack  


The complete stack of PowerAPI is composed of :

- The Sensor and the Formula, these are the two main parts of PowerAPI, the Sensor retrieve power consumption related metrics and the Formula compute an estimation of the power consumption.

- The Sensor and the Formula both need an *output*, the supported *output* are listed [here](./reference/database/sources_destinations.md). The formula will also use the Sensor *output* as his *input*

- Finally, they will both need configuration files, as described in the [HWPC-Sensor Documentation](./reference/sensors/hwpc-sensor.md#global-parameters) and in the [SmartWatts Documentation](./reference/formulas/smartwatts.md#global-parameters), several parameters can be set, both globally and for specific Groups monitored. These parameters can also be set using CLI parameters.

To learn more see the [overview section](./reference/overview.md).


## Test powerAPI

If you wish to get started as soon as possible, using the following cURL link below will allow you to setup everything quickly using Docker.

curl -sSL https://raw.githubusercontent.com/Inkedstinct/powerapi-ng.github.io/refs/heads/7_doc/nld_proofread/docs/script/getting_started/curl_version/start.sh | bash

This curl link will run [this script](./script/getting_started/curl_version/start.sh). It will detect the CPU used, and download the appropriate Docker compose file and environnement file for your configuration.

It will then execute the Docker compose file, deploying the following elements for 3 minutes: 

1. A MongoDB instance to store the [Sensor](./reference/sensors/hwpc-sensor.md) reports.

2. An [HWPC-Sensor](./reference/sensors/hwpc-sensor.md) that outputs its 
[HWPC Reports](./reference/reports/reports.md#hwpc-reports) in a MongoDB Database, 
within the HWPC Report Collection

3. A [SmartWatts](./reference/formulas/smartwatts.md) that streams the 
[HWPC Reports](./reference/reports/reports.md#hwpc-reports) from the MongoDB 
Database Collection, processes it and outputs its 
[Power Reports](./reference/reports/reports.md#power-reports) into CSV.

In this specific case, we don't use configuration file for the Sensor or the Formula and directly use the CLI parameters in the Docker compose file. 

After he result will be visible under the *csv* directory.


