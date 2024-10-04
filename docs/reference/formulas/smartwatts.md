# SmartWatts Formula

SmartWatts is a Formula, a configurable software that can estimate the power consumption of software in real-time.
SmartWatts needs to receive several metrics available in [Reports](../report/report.md), [HWPC Sensor](../sensors/hwpc-sensor.md#events) is a Sensor compatible (i.e making the necessary metrics available in HWPC Reports):

- The Running Average Power Limit (`RAPL`)
- `msr` events (`TSC`, `APERF`, `MPERF`)
- `core` events which depend on the Processor Architucture

These metrics are then used as inputs for a power model that estimates the power consumption of each software, those estimations are recorded in Power Reports.
The model is calibrated each time a `cpu-error-threshold` is
reached by learning a new power model with previous reports.

The choice of those specific metrics is motivated in [SmartWatts: Self-Calibrating
Software-Defined Power Meter for Containers](https://hal.inria.fr/hal-02470128)

## Installation

The default installation is done through Docker container.  
The different images can be found on the [Docker Hub](https://hub.docker.com/r/powerapi/smartwatts-formula/tags)

=== "Docker"
    ```
    docker pull powerapi/smartwatts-formula
    ```
=== "Pypi"

    ```sh
    pip install smartwatts
    ```

## Usage

For running the SmartWatts Formula you need: a Source and a Destination, a Sensor that provides `HWPCReports` and a configuration.

### Input and Output
As any Formula, SmartWatts needs both inputs and outputs.
We can choose those among [this list](../database/sources_destinations.md#summary)

#### MongoDB as input
MongoDB can be used as input for Reports.
You can start a MongoDB instance via a Docker container by running:
```
docker run -d --name mongo_output -p 27017:27017 mongo:latest
```
The different images can be found on the [Docker Hub](https://hub.docker.com/_/mongo/tags)

#### InfluxDB as output
On the other hand, we can use InfluxDB instance as output for our Power Reports

You can start an InfluxDB instance, in version >= 2.0.0 via a Docker container by running:
```sh
docker run -p 8086:8086 -v "/tmp/powerapi-influx/data:/var/lib/influxdb2" -v "/tmp/powerapi-influx/config:/etc/influxdb2" influxdb:2
```
The different images can be found on the [Docker Hub](https://hub.docker.com/_/influxdb/tags?name=2)

???+ tip "Set up influxdb 2.X for the first time"
    If it is the first time that you are using `influxdb 2.X`, there are several methods (UI, CLI, API) to make a set up. Please check [here](https://docs.influxdata.com/influxdb/v2/get-started/setup/) for more information.  


### Sensor
[HWPC Sensor](../sensors/hwpc-sensor.md) can be used in order to get `HWPCReports` which provided the necessary information for SmartWatts.
If you wish to use it : 
- Install the HWPC Sensor (see [here](../sensors/hwpc-sensor.md#installation))
- Start the Sensor (see [here](../sensors/hwpc-sensor.md#usage))


### Parameters

Besides the [basic parameters](../formulas/configuration_files.md), the following ones are specific to SmartWatts:

???+ info "Hardware dependent values"
    Some parameters values depend of your hardware. In particular, `cpu-base-freq`. You can obtain this value from `CPU MHz` field by using `lscpu` command.


| Parameter                | Type   | CLI shortcut  | Default Value                                      | Description                             |
| -------------            | -----  | ------------- | -------------                                      | ------------------------------------    |
|`disable-cpu-formula`     | `bool` (flag)    | -           | `false`                                             | Disable CPU Formula                    |
|`disable-dram-formula`    | `bool` (flag) | -           | `false`                                                | Disable RAM Formula |
|`cpu-rapl-ref-event`    | `string` | -           | `"RAPL_ENERGY_PKG"`  | RAPL event used as reference for the CPU power models |
|`dram-rapl-ref-event`    | `string` | -           | `"RAPL_ENERGY_DRAM"`  | RAPL event used as reference for the DRAM power models |
|`cpu-tdp`         | `int` | -           | `125`  | CPU TDP (in Watt)|
|`cpu-base-clock`         | `int` | -           | `100`  | CPU base clock (in MHz) |
|`cpu-base-freq`     | `int` | -           | `2100`  | CPU base frequency (in MHz), depend of your hardware. You can obtain this value from `CPU MHz` field by using `lscpu` command. |
|`cpu-error-threshold`    | `float` | -           | `2.0`  | Error threshold for the CPU power models (in Watts) |
|`dram-error-threshold`    | `float` | -           | `2.0`  | Error threshold for the DRAM power models (in Watts) |
|`learn-min-samples-required`    | `int` | -           | `10`  | Minimum amount of samples required before trying to learn a power model |
|`learn-history-window-size`    | `int` | -           | `60`  | Size of the history window used to keep samples to learn from |
|`sensor-reports-frequency`    | `int` | -           | `1000`  | The frequency with which measurements are made (in milliseconds) |

### Running the Formula via CLI parameters

In order to run the Formula, you can execute one of the following command lines, depending on the installation you use:

=== "Docker"

     ```sh
     docker run -t \
     --net=host \
     powerapi/smartwatts-formula --verbose \
     --input mongodb --model HWPCReport --uri mongodb://127.0.0.1 --db test --collection prep \
     --output influxdb2 --model PowerReport --uri 127.0.0.1 --port 8086 --db power_consumption --org org_test --token mytoken \
     --cpu-base-freq 1900 \
     --cpu-error-threshold 2.0 \
     --disable-dram-formula \
     --sensor-reports-frequency 1000
     ```

=== "Pip"

    ```sh
    python -m smartwatts \
    --verbose \
    --input mongodb --model HWPCReport --uri mongodb://127.0.0.1 --db test --collection prep \
    --output influxdb2 --model PowerReport --uri 127.0.0.1 --port 8086 --db power_consumption --org org_test --token mytoken\
    --cpu-base-freq 1900 \
    --cpu-error-threshold 2.0 \
    --disable-dram-formula \
    --sensor-reports-frequency 1000
    ```

In this configuration we are using MongoDB as source and InfluxDB 2.X as Destination. 

???+ info "Estimations' Storage"
    Your `PowerReports` will be stored on InfluxDB2. You can watch them in a grafana by using the [following tutorial](../grafana/grafana.md).

???+ tip "Using shortcuts for parameters' names"
    You use `-` instead of `--`.

### Running the Formula with Environment Variables

Parameters are defined by using the prefixes `POWERAPI_`, `POWERAPI_INPUT_` and `POWERAPI_OUTPUT_` in the names of Environment Variables. The following conventions are used:

- `POWERAPI_<PARAMETER_NAME>`
- `POWERAPI_INPUT_<COMPONENT_NAME>_<PARAMETER_NAME>`
- `POWERAPI_OUTPUT_<COMPONENT_NAME>_<PARAMETER_NAME>`

where `PARAMETER_NAME` refers to names of parameters in upper case (e.g., `VERBOSE`, `CPU_BASE_FREQ`, `COLLECTION`) and `COMPONENT_NAME` to the name given to the different Sources and Destinations in upper case (e.g., `PULLER` and `PUSHER_POWER`).

Below you find an example for running the Formula with Docker and Pip:

=== "Docker"

    ```sh
    docker run -t \
    --net=host \
    -e POWERAPI_VERBOSE=true \
    -e POWERAPI_STREAM=true \
    -e POWERAPI_CPU_BASE_FREQ=1900 \
    -e POWERAPI_CPU_ERROR_THRESHOLD=2.0 \
    -e POWERAPI_DISABLE_DRAM_FORMULA=true \
    -e POWERAPI_SENSOR_REPORTS_FREQUENCY=1000 \
    -e POWERAPI_INPUT_PULLER_MODEL=HWPCReport \
    -e POWERAPI_INPUT_PULLER_TYPE=mongodb \
    -e POWERAPI_INPUT_PULLER_URI=mongodb://127.0.0.1 \
    -e POWERAPI_INPUT_PULLER_DB=test \
    -e POWERAPI_INPUT_PULLER_COLLECTION=prep \
    -e POWERAPI_OUTPUT_PUSHER_POWER_MODEL=PowerReport \
    -e POWERAPI_OUTPUT_PUSHER_POWER_TYPE=influxdb2 \
    -e POWERAPI_OUTPUT_PUSHER_POWER_URI=127.0.0.1 \
    -e POWERAPI_OUTPUT_PUSHER_POWER_PORT=8086 \
    -e POWERAPI_OUTPUT_PUSHER_POWER_DB=power_consumption \
    -e POWERAPI_OUTPUT_PUSHER_POWER_ORG=org_test \
    -e POWERAPI_OUTPUT_PUSHER_POWER_TOKEN=mytoken \
    powerapi/smartwatts-formula
    ```

=== "Pip"

    ```sh
    export POWERAPI_VERBOSE=true
    export POWERAPI_STREAM=false
    export POWERAPI_CPU_BASE_FREQ=1900
    export POWERAPI_CPU_ERROR_THRESHOLD=2.0
    export POWERAPI_DISABLE_DRAM_FORMULA=true
    export POWERAPI_SENSOR_REPORTS_FREQUENCY=1000
    export POWERAPI_INPUT_PULLER_MODEL=HWPCReport
    export POWERAPI_INPUT_PULLER_TYPE=mongodb
    export POWERAPI_INPUT_PULLER_URI=mongodb://127.0.0.1
    export POWERAPI_INPUT_PULLER_DB=test
    export POWERAPI_INPUT_PULLER_COLLECTION=prep
    export POWERAPI_OUTPUT_PUSHER_POWER_MODEL=PowerReport
    export POWERAPI_OUTPUT_PUSHER_POWER_TYPE=influxdb2
    export POWERAPI_OUTPUT_PUSHER_POWER_URI=127.0.0.1
    export POWERAPI_OUTPUT_PUSHER_POWER_PORT=8086
    export POWERAPI_OUTPUT_PUSHER_POWER_DB=power_consumption
    export POWERAPI_OUTPUT_PUSHER_POWER_ORG=org_test
    export POWERAPI_OUTPUT_PUSHER_POWER_TOKEN=mytoken
    python -m smartwatts
    ```

### Running the Formula with a Configuration File

Below an example is provided by using MongoDB as Source and InfluxDB as Destination.

```json
{
  "verbose": true,
  "stream": true,
  "input": {
    "puller": {
      "model": "HWPCReport",
      "type": "mongodb",
      "uri": "mongodb://127.0.0.1",
      "db": "test",
      "collection": "prep"
    }
  },
  "output": {
    "pusher_power": {
      "type": "influxdb2",
      "uri": "127.0.0.1",
      "port": 8086,
      "db": "power_consumption",
      "org": "org_test",
      "token": "mytoken"
    }
  },
  "cpu-base-freq": 1900,
  "cpu-error-threshold": 2.0,
  "disable-dram-formula": true,
  "sensor-reports-frequency": 1000
}
```

???+ info "Alternative Source or Destination"
    If you want to use another Source or Destination, please check the documentation [here](../database/sources_destinations.md) and modify your configuration according to the Source or Destination that you want to use.

Once you have your configuration file, run SmartWatts using one of the following command lines, depending on
the installation you use:

=== "Docker"

    ```sh
    docker run -t \
    --net=host \
    -v $(pwd)/config_file.json:/config_file.json \
    powerapi/smartwatts-formula --config-file /config_file.json
    ```

=== "Pip"

    ```sh
    python -m smartwatts --config-file config_file.json
    ```

### Combining the three Running Methods
The three running methods can be used to define a configuration. The priority is as follows:

1. CLI
2. Environment Variables
3. Configuration File

This means that parameters values defined via the CLI have the highest priority while values defined via Environment Variables will be preserved regarding those defined by a Configuration File.
