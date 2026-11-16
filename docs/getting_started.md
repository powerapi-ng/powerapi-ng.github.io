# Getting started

In this tutorial, we will guide you through the first steps to get started with PowerAPI.
The objective is to get a quick view of the capabilities of PowerAPI.
A few things are required before we start:

- A compatible processor (you can see the compatible CPU architecture [here](reference/sensors/hwpc-sensor.md#)). You can take a look on the following links to find your CPU architecture:  
    * For [Intel Processor](https://en.wikipedia.org/wiki/List_of_Intel_processors).  
    * For [Intel Xeon Processor](https://en.wikipedia.org/wiki/List_of_Intel_Xeon_processors).  
    * For [AMD Processor](https://en.wikipedia.org/wiki/Table_of_AMD_processors).  
- You can also use the `lscpu` command to get information about your processor.
- Docker (refer to [this official documentation](https://docs.docker.com/engine/install/) and the [post-install steps](https://docs.docker.com/engine/install/linux-postinstall/) if needed!).
- Root access.

## Which components to get a complete stack  


The complete stack of PowerAPI is composed of:

- A Sensor and a Formula that enable us to define a Software Power Meter. The Sensor retrieves power consumption related metrics and the Formula compute an estimation of the power consumption. Currently, PowerAPI provides [HWPC-Sensor](reference/sensors/hwpc-sensor.md) and [SmartWatts Formula](reference/formulas/smartwatts.md)

- The Sensor and the Formula need an *output*. The supported *output* are listed [here](reference/sensors/hwpc-sensor.md#output). The Formula will also use the Sensor *output* as its *input*.

- Finally, they need a configuration as described in the [HWPC-Sensor](reference/sensors/hwpc-sensor.md#usage) and [SmartWatts](reference/formulas/smartwatts.md#global-parameters) documentation. The configuration parameters can be defined via a configuration file or via the CLI.

To learn more see the [overview section](./reference/overview.md).
