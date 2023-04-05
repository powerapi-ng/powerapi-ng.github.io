# HWPC Sensor

HardWare Performance Counter (HWPC) Sensor is a tool that monitors the Intel CPU
performance counter and the power consumption of CPU.

HWPC Sensor uses the RAPL (Running Average Power Limit) technology to monitor CPU
power consumption. This technology is only available on **Intel Sandy Bridge**
architecture or **newer**. It is also available on **AMD Zen (1,2,34)**. **Power/ARM/RISCV are not supported** architectures.

In particular, it exploits the `perf` API of the **Linux kernel**. It is only available on Linux
and need to have **root access** to be used.

**The sensor can not be used in a virtual machine**, it must have access (via Linux
kernel API) to the real CPU register to read performance counter values.

## Installation

=== "Docker"

    ```bash
    docker pull powerapi/hwpc-sensor
    ```

=== "Deb file"

    Download the `.deb` file from the [latest
    release](https://github.com/powerapi-ng/hwpc-sensor/releases)

    Install the sensor with
    ```bash
    sudo apt install hwpc-sensor-<version>.deb
    ```
=== "Binary file"

    You can use the compiled version of the sensor (available
    [here](https://github.com/powerapi-ng/hwpc-sensor/releases))

## Usage

For running the sensor, a Destination and a configuration defined via a file or CLI parameters are required.

### Destination

For running HWPCSensor we are using MongoDB as Destination as a docker container.

To start a MongoDB instance via the command line

```
docker run -d --name mongo_destination -p 27017:27017 mongo
```

### Root Parameters

The table below shows the different parameters related to the Sensor Configuration:

| Parameter                | Type   | CLI shortcut  | Default Value                                      | Description                             |
| -------------            | -----  | ------------- | -------------                                      | ------------------------------------    |
|`verbose`                 | `bool` (flag) | `v`             | `false`                                            | Verbose or quiet mode                   |
|`frequency`                 | `int` | `f`             | `1000`                                            | The time in milliseconds between two reports                   |
|`name`                 | `string` | `n`             | -                                            | Name of the sensor                   |
|`cgroup_basepath`                 | `string` | `p`             | `/sys/fs/cgroup/perf_event`        |  The default base path for `cgroups`                   |
|`system`                 | `dict` | `s`             | -                                            | A system group with a monitoring type and a list of system events (cf. [`system` Group Parameters](hwpc-sensor.md#system-and-container-groups-parameters))                   |
|`container`                 | `dict` | `c`          | -                                            | A group with a monitoring type and a list of  events (cf. [`system` Group Parameters](hwpc-sensor.md#system-and-container-groups-parameters))                   |
|`output`                 | Destination | `r`             | ` csv`                                            | The Destination used as output. The Sensor only supports [MongoDB](../database/sources_destinations.md#mongodb) (`mongodb`) and [CSV](../database/sources_destinations.md#csv) (`csv`) as Destination.                    |



### `system` and `container` Groups Parameters

| Parameter                | Type   | CLI shortcut  | Default Value                                      | Description                             |
| -------------            | -----  | ------------- | -------------                                      | ------------------------------------    |
|`events`     | `string`   | `e`           | -                                             | List of events to be monitored. As CLI parameter, each event is indicated with `e`                    |
|`monitoring_type`     | `string` (`MONITOR_ONE_CPU_PER_SOCKET`, `MONITOR_ALL_CPU_PER_SOCKET` )    | `o` (flag)          |  `MONITOR_ALL_CPU_PER_SOCKET`                                             | The monitoring type. If `o` is specified as CLI parameter, `MONITOR_ONE_CPU_PER_SOCKET` is used as type   

### Events

Table below depicts the different group events for comptible Intel and AMD architectures.

| Architectures                | Group   | Events        |
| -------------               | -----   | ------------- |
|Intel Sandy Bridge and newer, AMD Zen (1,2,3,4)  | `rapl`  | `RAPL_ENERGY_PKG`|
|Intel Sandy Bridge and newer, AMD Zen (1,2,3,4)  | `msr`  | `TSC`, `APERF`, `MPERF`|
|Intel Sandy Bridge through Broadwell | `core` | `CPU_CLK_THREAD_UNHALTED:REF_P`, `CPU_CLK_THREAD_UNHALTED:THREAD_P`, `LLC_MISSES`,`INSTRUCTIONS_RETIRED`|
|Intel Skylake and newer | `core` | `CPU_CLK_UNHALTED:REF_P`, `CPU_CLK_UNHALTED:THREAD_P`, `LLC_MISSES`,`INSTRUCTIONS_RETIRED`|
|AMD Zen (1,2,3,4)| `core`| `CYCLES_NOT_IN_HALT`, `RETIRED_INSTRUCTIONS` , `RETIRED_UOPS`|


### Running the Sensor with a Configuration File

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

Once you have your configuration file, run HWPCSensor using one of the following command lines, depending on the installation you use:

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

=== "Binary file"

    ```sh
    ./hwpc-sensor --config-file config_file.json
    ```

### Running the Sensor via CLI parameters

In order to run the Sensor without a configuration file, run HWPCSensor using one of the following command lines, depending on the installation you use:

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

=== "Binary file"

    ```sh
    ./hwpc-sensor -n "$(hostname -f)" \
    -r "mongodb" -U "mongodb://127.0.0.1" -D "db_sensor" -C "report_0" \
    -s "rapl" -o -e "RAPL_ENERGY_PKG" \
    -s "msr" -e "TSC" -e "APERF" -e "MPERF" \
    -c "core" -e "CPU_CLK_THREAD_UNHALTED:REF_P" -e "CPU_CLK_THREAD_UNHALTED:THREAD_P" -e "LLC_MISSES" -e "INSTRUCTIONS_RETIRED"
    ```



???+ info "Reports' Storage"
    Your [`HWPCReports`](../reports/reports.md#hwpc-report) will be stored on MongoDB.

???+ tip "CLI parameters' names"
    You can only use shortcuts.
