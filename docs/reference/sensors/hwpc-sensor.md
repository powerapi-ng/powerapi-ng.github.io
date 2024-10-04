# HWPC Sensor

HardWare Performance Counter (HWPC) Sensor is a tool that monitors the Intel CPU
performance counter and the power consumption of CPU.

HWPC Sensor uses the RAPL (Running Average Power Limit) technology to monitor CPU
power consumption. The following table gives a glimpse of RAPL support regarding
most common architectures:  

???+ info "HWPC Sensor PreRequisites"
    `lscpu` will give you the necessary information about your CPU Architecture 

| Architecture | RAPL Supported |
|--------------|----------------|
| Intel Tiger Lake | :material-close: Not Supported |
| Intel Alder Lake | :material-close: Not Supported |
| Intel Raptor Lake | :material-close: Not Supported |
| Power / ARM / RISCV | :material-close: Not Supported |
| AMD Zen (1, 2, 3, 4) | :material-check: Supported |
| Intel Sandy Bridge and [newer](https://en.wikipedia.org/wiki/List_of_Intel_Core_processors#Core_i_(2nd_gen)) (except for above mentions) | :material-check: Supported |

???+ info "HWPC Sensor PreRequisites"
    In addition of a supported architecture, there is some pre-requisites:
    - Using a Linux distribution exposing the [perf](https://perf.wiki.kernel.org/index.php/Main_Page) api  
    - Using Cgroup version 1 when using version 1.2 or older. See [this section](../cgroup/cgroup_v1_activation.md) about its configuration 
    - Deploying on a physical device as the HWPC Sensor must have access to the real CPU register

![HWPC Sensor Overview](../../assets/images/reference/sensors/hwpc-sensor-overview.svg){ width="1000px"}

## Sensor outputs

The sensor provides raw values of performance counters as well as `RAPL` raw values in microjoules.   

## Installation

The default installation is done through Docker container.  
The different images can be found on the [Docker Hub](https://hub.docker.com/r/powerapi/hwpc-sensor/tags)

Here is a sample to deploy the latest image version available.
=== "Docker"

    ```bash
    docker pull powerapi/hwpc-sensor:latest

    ```

## Usage

An HWPC Sensor instance needs several parameteres to be configured in order to be used.  
The following tabs gives a complete overview of available parameters, along with their default values and description.

### Global parameters

The table below shows the different parameters related to the Sensor global configuration, nested objects (system, container, output) are described in dedicated sections below:

| Parameter                | Type   | CLI shortcut  | Default Value                                      | Description                             |
| -------------            | -----  | ------------- | -------------                                      | ------------------------------------    |
|`verbose`                 | `bool` (flag) | `v`             | `false`                                            | Verbose or quiet mode                   |
|`frequency`                 | `int` | `f`             | `1000`                                            | The time in milliseconds between two reports                   |
|`name`                 | `string` | `n`             | -                                            | Name of the sensor                   |
|`cgroup_basepath`                 | `string` | `p`             | `/sys/fs/cgroup` (`cgroup` V2)       |  The base path for `cgroups`. To use `cgroup` V1 `/sys/fs/cgroup/perf_event` needs to be used as value                   |
|`system`                 | `dict` | `s`             | -                                            | A system group with a monitoring type and a list of system events (cf. [`system` Group Parameters](hwpc-sensor.md#system-and-container-groups-parameters))                   |
|`container`                 | `dict` | `c`          | -                                            | A group with a monitoring type and a list of  events (cf. [`system` Group Parameters](hwpc-sensor.md#system-and-container-groups-parameters))                   |
|`output`                 | Output | `r`             | ` csv`                                            | The [output information](hwpc-sensor.md#output), the Sensor only supports [MongoDB](../database/sources_destinations.md#mongodb) (`mongodb`) and [CSV](../database/sources_destinations.md#csv) (`csv`) as output.                    |

### `system` and `container` Groups Parameters

The table below shows the different parameters related to the Sensor `system` and `container` configuration fields:

| Parameter                | Type   | CLI shortcut  | Default Value                                      | Description                             |
| -------------            | -----  | ------------- | -------------                                      | ------------------------------------    |
|`events`     | `string`   | `e`           | -                                             | List of events to be monitored. As CLI parameter, each event is indicated with `e`. The structure of events is given [below](hwpc-sensor.md#events)                    |
|`monitoring_type`     | `string` (`MONITOR_ONE_CPU_PER_SOCKET`, `MONITOR_ALL_CPU_PER_SOCKET` )    | `o` (flag)          |  `MONITOR_ALL_CPU_PER_SOCKET`                                             | The monitoring type. If `o` is specified as CLI parameter, `MONITOR_ONE_CPU_PER_SOCKET` is used as type  |

### Events

Table below depicts the different group events for compatible Intel and AMD architectures.

| Architectures                | Group   | Events        |
| -------------               | -----   | ------------- |
|Intel Sandy Bridge and newer, AMD Zen 2  | `rapl`  | `RAPL_ENERGY_PKG`, `RAPL_ENERGY_DRAM`|
|Intel Sandy Bridge and newer, AMD Zen 2  | `msr`  | `TSC`, `APERF`, `MPERF`|
|Intel Skylake, Whiskey Lake, Coffee Lake| `core` | `CPU_CLK_THREAD_UNHALTED:REF_P`, `CPU_CLK_THREAD_UNHALTED:THREAD_P`, `LLC_MISSES`,`INSTRUCTIONS_RETIRED`|
|Intel Sandy Bridge, Comet Lake | `core` | `CPU_CLK_UNHALTED:REF_P`, `CPU_CLK_UNHALTED:THREAD_P`, `LLC_MISSES`,`INSTRUCTIONS_RETIRED`|
|AMD Zen 2 | `core`| `CYCLES_NOT_IN_HALT`, `RETIRED_INSTRUCTIONS` , `RETIRED_UOPS`|
|AMD Zen 3 | `core`| `CYCLES_NOT_IN_HALT`, `RETIRED_INSTRUCTIONS` , `RETIRED_OPS`|

### Output

As precised, two kinds of outputs are supported, MongoDB and CSV files.

#### MongoDB Output

Table below depicts the different parameters for MongoDB type output with HWPC Sensor:  
| Parameter     | Type   | CLI shortcut  | Default Value | Mandatory                                        |                                             Description                             |
| ------------- | -----  | ------------- | ------------- | ----------                                              | ------------------------------------    |
| `uri`          | string | `U`           | N/A | Yes                                                       | The IP address of your MongoDB instance |
| `database`          | string | `D`            | N/A | Yes                                                       | The name of your database               |
| `collection`   | string | `HWPCSensor`          | N/A | Yes                                                       | The name of the collection inside `db`  |

You can start a MongoDB instance via a Docker container by running:

```
docker run -d --name mongo_output -p 27017:27017 mongo:latest
```

The different images can be found on the [Docker Hub](https://hub.docker.com/_/mongo/tags)

#### CSV Output

Table below depicts the different parameters for CSV type output:  
| Parameter     | Type    | CLI shortcut  | Default Value | Mandatory | Description                                                                   |
| ------------- | -----   | ------------- | ------------- | ----------| ------------------------------------                                          |
| `directory` | string         | `U`           | "." (Current directory)           | No |The directory where output CSV files will be written          |

### Running the Sensor with a Configuration File

The following snippet describe the configuration of an HWPC Sensor instance, writting reports to a MongoDB intance as output:

```json
{
  "name": "sensor",
  "verbose": true,
  "frequency": 500,
  "output": {
    "type": "mongodb",
    "uri": "mongodb://127.0.0.1",
    "database": "db_sensor",
    "collection": "report_0"
  },
  "system": {
    "rapl": {
      "events": ["RAPL_ENERGY_PKG"],
      "monitoring_type": "MONITOR_ONE_CPU_PER_SOCKET"
    },
    "msr": {
      "events": ["TSC", "APERF", "MPERF"]
    }
  },
  "container": {
    "core": {
      "events": [
        "CPU_CLK_THREAD_UNHALTED:REF_P",
        "CPU_CLK_THREAD_UNHALTED:THREAD_P",
        "LLC_MISSES",
        "INSTRUCTIONS_RETIRED"
      ]
    }
  }
}
```

The following CLI command shows how to use this configuration file in the deployment of an HWPC Sensor container :
=== "Docker"

    ```sh
    docker run --rm  \
    --net=host \
    --privileged \
    --pid=host \
    -v /sys:/sys \
    -v /var/lib/docker/containers:/var/lib/docker/containers:ro \
    -v /tmp/powerapi-sensor-reporting:/reporting \
    -v $(pwd):/srv \
    -v $(pwd)/config_file.json:/config_file.json \
    powerapi/hwpc-sensor --config-file /config_file.json
    ```

### Running the Sensor via CLI parameters

The following CLI command shows how to launch an instance of HWPC Sensor with the same configuration as [above](hwpc-sensor.md#running-the-sensor-with-a-configuration-file)
=== "Docker"

    ```sh
    docker run --rm \
    --net=host \
    --privileged \
    --pid=host \
    -v /sys:/sys \
    -v /var/lib/docker/containers:/var/lib/docker/containers:ro \
    -v /tmp/powerapi-sensor-reporting:/reporting \
    -v $(pwd):/srv \
    powerapi/hwpc-sensor \
    -n "$(hostname -f)" \
    -r "mongodb" -U "mongodb://127.0.0.1" -D "db_sensor" -C "report_0" \
    -s "rapl" -o -e "RAPL_ENERGY_PKG" \
    -s "msr" -e "TSC" -e "APERF" -e "MPERF" \
    -c "core" -e "CPU_CLK_THREAD_UNHALTED:REF_P" -e "CPU_CLK_THREAD_UNHALTED:THREAD_P" -e "LLC_MISSES" -e "INSTRUCTIONS_RETIRED"
    ```

???+ info "Reports' Storage"
    Your [`HWPCReports`](../reports/reports.md#hwpc-reports) will be stored on MongoDB.

???+ tip "CLI parameters' names"
    You can only use shortcuts.
