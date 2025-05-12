# HWPC Sensor

HardWare Performance Counter (HWPC) Sensor is a tool that monitors the CPU
performance counters and its power consumption.

The figure below depicts how Sensor works in general:   


![HWPC Sensor Overview](../../assets/images/reference/sensors/PowerAPI_HWPCSensorOverview.drawio.svg){ width="1000px"}

HWPC Sensor uses the RAPL (Running Average Power Limit) technology to monitor CPU
power consumption. Keep in mind that this sensor is mainly developed for "server" architectures.
The following table gives a glimpse of RAPL support regarding
most common architectures:  

!!! tip "CPU architecture"
    `lscpu` will give you the necessary information about your CPU Architecture

| Architecture | RAPL Supported |
|--------------|----------------|
| AMD Zen (2, 3) | :material-check: Supported |
| Intel Sandy Bridge and [newer](https://en.wikipedia.org/wiki/List_of_Intel_Core_processors#Core_i_(2nd_gen)) (except for below mentions) | :material-check: Supported |
| Intel Tiger Lake (11th Gen) | :material-close: Not Supported |
| Intel Alder Lake (12th Gen) | :material-close: Not Supported |
| Intel Raptor Lake (13th & 14th Gen) | :material-close: Not Supported |
| Power / ARM / RISCV | :material-close: Not Supported |

!!! note "HWPC Sensor pre-requisites"
    In addition of a supported architecture, there is some pre-requisites:

    - Using a Linux distribution exposing the [`perf`](https://perf.wiki.kernel.org/index.php/Main_Page) api  
    - Using cgroup version 1 when using version `1.2` or older. See [this section](../cgroup/cgroup_v1_activation.md) about its configuration
    - Using an AMD Zen 1 processor requires version `1.4` or older.
    - Deploying on a physical server as the HWPC Sensor must have access to the real CPU register


## Sensor outputs

The sensor provides raw values of performance counters and `RAPL` raw values in micro-joules.   

## Installation

The default installation is done through a Docker container. The different images can be found on [Docker Hub](https://hub.docker.com/r/powerapi/hwpc-sensor/tags).

Here is the command to deploy the latest image version available.
=== "Docker"

    ```sh
    docker pull powerapi/hwpc-sensor:latest
    ```

## Usage

The following tabs gives a complete overview of available parameters, along with their default values and description.

??? info "Global Parameters"

    The table below shows the different parameters related to the Sensor global configuration:

    | Parameter                | Type   | CLI shortcut  | Default Value                                      | Description                             |
    | -------------            | -----  | :-------------: | :-------------:                                      | ------------------------------------    |
    |`verbose`                 | `bool` (flag) | `v`             | `false`                                            | Verbose or quiet mode                   |
    |`frequency`                 | `int` | `f`             | `1000`                                            | The time in milliseconds between two reports                   |
    |`name`                 | `string` | `n`             | -                                            | Name of the sensor                   |
    |`cgroup_basepath`                 | `string` | `p`             | `/sys/fs/cgroup` (`cgroup` V2)       |  The base path for `cgroups`. To use `cgroup` V1 `/sys/fs/cgroup/perf_event` needs to be used as value                   |
    |`system`                 | `dict` | `s`             | -                                            | A system group with a monitoring type and a list of system events (cf. [`system` Group Parameters](hwpc-sensor.md#system-and-container-groups-parameters))                   |
    |`container`                 | `dict` | `c`          | -                                            | A group with a monitoring type and a list of  events (cf. [`system` Group Parameters](hwpc-sensor.md#system-and-container-groups-parameters))                   |
    |`output`                 | `dict`| `r`             |  { "type": "csv", "directory": "." } | The [output information](hwpc-sensor.md#output), the Sensor only supports [MongoDB](hwpc-sensor.md#output "MongoDB Output") (`mongodb`), [CSV](hwpc-sensor.md#output) (`csv`) and [Socket](hwpc-sensor.md#output) (`socket`) as output.                    |

    Nested parameters (system, container, output) are described in dedicated sections below.
??? info "Group Parameters (`system` and `container`)"

    The table below shows the different parameters related to the Sensor `system` and `container` configuration fields:

    | Parameter                | Type   | CLI shortcut  | Default Value                                      | Description                             |
    | -------------            | -----  | :-------------: | :-------------:                                      | ------------------------------------    |
    |`events`     | `string`   | `e`           | -                                             | List of events to be monitored. As CLI parameter, each event is indicated with `e`. The structure of events is given [below](hwpc-sensor.md#events)                    |
    |`monitoring_type`     | `string` ( **one of** `MONITOR_ONE_CPU_PER_SOCKET` **or** `MONITOR_ALL_CPU_PER_SOCKET` )    | `o` (flag)          |  `MONITOR_ALL_CPU_PER_SOCKET`                                             | The monitoring type. If `o` is specified as CLI parameter, `MONITOR_ONE_CPU_PER_SOCKET` is used as type  |

??? info "Group Events"

    Table below depicts the different group events for compatible Intel and AMD architectures.

    | Architectures                | Group   | Events        |
    | -------------               | -----   | ------------- |
    |Intel Sandy Bridge and newer, AMD Zen 2, 3, 4, 5  | `rapl`  | `RAPL_ENERGY_PKG`, `RAPL_ENERGY_DRAM`|
    |Intel Sandy Bridge and newer, AMD Zen 2, 3, 4, 5  | `msr`  | `TSC`, `APERF`, `MPERF`|
    |Intel Skylake, Whiskey Lake, Coffee Lake| `core` | `CPU_CLK_THREAD_UNHALTED:REF_P`, `CPU_CLK_THREAD_UNHALTED:THREAD_P`, `LLC_MISSES`,`INSTRUCTIONS_RETIRED`|
    |Intel Sandy Bridge, Comet Lake | `core` | `CPU_CLK_UNHALTED:REF_P`, `CPU_CLK_UNHALTED:THREAD_P`, `LLC_MISSES`,`INSTRUCTIONS_RETIRED`|
    |AMD Zen 2 | `core`| `CYCLES_NOT_IN_HALT`, `RETIRED_INSTRUCTIONS` , `RETIRED_UOPS`|
    |AMD Zen 3, 4, 5 | `core`| `CYCLES_NOT_IN_HALT`, `RETIRED_INSTRUCTIONS` , `RETIRED_OPS`|

### Output

Three kinds of outputs are supported: Socket, MongoDB and CSV files.

??? info "MongoDB Output"

    Table below depicts the different parameters for MongoDB type output with HWPC Sensor:  

    | Parameter     | Type   | CLI shortcut  | Default Value | Mandatory                                        |                                             Description                             |
    | ------------- | -----  | :-------------: | :-------------: | :----------:                                              | ------------------------------------    |
    | `uri`          | string | `U`           | - | Yes                                                       | The IP address of your MongoDB instance |
    | `database`          | string | `D`            | - | Yes                                                       | The name of your database               |
    | `collection`   | string | `C`          | - | Yes                                                       | The name of the collection inside `db`  |

??? info "CSV Output"

    Table below depicts the different parameters for CSV type output:  

    | Parameter     | Type    | CLI shortcut  | Default Value | Mandatory | Description                                                                   |
    | ------------- | -----   | :-------------: | :-------------: | :----------:| ------------------------------------                                          |
    | `directory` | string         | `U`           | "." (Current directory)           | No |The directory where output CSV files will be written          |

??? info "Socket Output"

    Table below depicts the different parameters for Socket type output:  

    | Parameter     | Type    | CLI shortcut  | Default Value | Mandatory | DQuoteescription                                                                   |
    | ------------- | -----   | :-------------: | :-------------: | :----------:| ------------------------------------                                          |
    | `uri` | string         | `U`           | -           | Yes | The IP address of the machine running the socket         |
    | `port` | int         | `P`           | -           | Yes | The port of communication        |

### Running the Sensor with a Configuration File

The following snippets describe the configuration file of an HWPC Sensor instance. One example is provided for each possible output:

!!! example "Examples for an Intel Processor, using a Configuration File"

    === "MongoDB Output"

        ```json hl_lines="5-10" title="config_file.json"
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

    === "CSV Output"

        ```json hl_lines="5-8" title="config_file.json"
        {
          "name": "sensor",
          "verbose": true,
          "frequency": 500,
          "output": {
            "type": "csv",
            "directory": "hwpc_reports"
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
    === "Socket Output"

        ```json hl_lines="5-9" title="config_file.json"
        {
          "name": "sensor",
          "verbose": true,
          "frequency": 500,
          "output": {
            "type": "socket",
            "uri": "http://127.0.0.1",
            "port": "9876"
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

      Please notice that you may need to adapt `core` values according to your processor architecture.

The following CLI command shows how to use this configuration file (named `config_file.json`) in the deployment of an HWPC Sensor instance as a Docker container :  

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

The following CLI command shows how to launch an instance of HWPC Sensor with the same configuration as [above](hwpc-sensor.md#running-the-sensor-with-a-configuration-file). One example is provided for each possible output:

!!! example "Examples using a CLI Parameters"

    === "CLI with MongoDB Output"

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

    === "CLI with CSV output"

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
          -r "csv" -U "hwpc_reports" \
          -s "rapl" -o -e "RAPL_ENERGY_PKG" \
          -s "msr" -e "TSC" -e "APERF" -e "MPERF" \
          -c "core" -e "CPU_CLK_THREAD_UNHALTED:REF_P" -e "CPU_CLK_THREAD_UNHALTED:THREAD_P" -e "LLC_MISSES" -e "INSTRUCTIONS_RETIRED"
        ```

    === "CLI with Socket output"

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
          -r "socket "-U "127.0.0.1" -P 9876 \
          -s "rapl" -o -e "RAPL_ENERGY_PKG" \
          -s "msr" -e "TSC" -e "APERF" -e "MPERF" \
          -c "core" -e "CPU_CLK_THREAD_UNHALTED:REF_P" -e "CPU_CLK_THREAD_UNHALTED:THREAD_P" -e "LLC_MISSES" -e "INSTRUCTIONS_RETIRED"
        ```

      Please notice that you may need to adapt core values according to your processor architecture.

!!! tip "CLI parameters' names"
    You can only use shortcuts.
