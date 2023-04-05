# SmartWatts Formula

SmartWatts is a software-defined power meter based on the PowerAPI toolkit.
SmartWatts is a configurable software that can estimate the power consumption of
software in real-time.
SmartWatts need to receive several metrics provided by
[HWPC Sensor](../sensors/hwpc-sensor.md#events) :

- The Running Average Power Limit (`RAPL`)
- `TSC`
- `APERF`
- `MPERF`
- `CPU_CLK_THREAD_UNHALTED:REF_P` (Sandy Bridge through Broadwell) or `CPU_CLK_UNHALTED:REF_P` (Skylake and newer)
- `CPU_CLK_THREAD_UNHALTED:THREAD_P` (Sandy Bridge through Broadwell) or `CPU_CLK_UNHALTED:THREAD_P` (Skylake and newer)
- `LLC_MISSES`
- `INSTRUCTIONS_RETIRED`

These metrics are then used as inputs for a power model that estimates the power
consumption of each software.
The model can derive from the reality, each time the `cpu-error-threshold` is
reached it learns a new power model, using the previous reports.

The choice of those specific metrics is motivated in [SmartWatts: Self-Calibrating
Software-Defined Power Meter for Containers](https://hal.inria.fr/hal-02470128)

## Installation

You can use [the following script](../script/smartwatts_install.sh) to install SmartWatts and HWPC Sensor.

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

### Source and Destination
For running SmartWatts we are using MongoDB as Source and InfluxDB as Destination as dockers containers.

To start a MongoDB instance via the command line

```sh
docker run -d --name mongo_source -p 27017:27017 mongo
```
And a InfluxDB instance

```sh
docker run -d --name influx_dest -p 8086:8086 influxdb:1.8
```


### Sensor
[HWPC Sensor](../sensors/hwpc-sensor.md) is used in order to get `HWPCReports`. Start by installing the HWPC Sensor (see
[here](../sensors/hwpc-sensor.md#installation)) and start it (see
[here](../sensors/hwpc-sensor.md#usage)).


### Parameters

Besides the [basic parameters](../formulas/configuration_files.md), the following ones are specific to SmartWatts:

| Parameter                | Type   | CLI shortcut  | Default Value                                      | Description                             |
| -------------            | -----  | ------------- | -------------                                      | ------------------------------------    |
|`disable-cpu-formula`     | `bool` (flag)    | -           | `false`                                             | Disable CPU Formula                    |
|`disable-dram-formula`    | `bool` (flag) | -           | `false`                                                | Disable RAM Formula |
|`cpu-rapl-ref-event`    | `string` | -           | `"RAPL_ENERGY_PKG"`  | RAPL event used as reference for the CPU power models |
|`dram-rapl-ref-event`    | `string` | -           | `"RAPL_ENERGY_DRAM"`  | RAPL event used as reference for the DRAM power models |
|`cpu-tdp`         | `int` | -           | `125`  | CPU TDP (in Watts)|
|`cpu-base-clock`         | `int` | -           | `100`  | CPU base clock (in MHz) |
|`cpu-frequency-min`      | `int` | -           | `100`  | CPU minimal frequency (in MHz) |
|`cpu-frequency-base`     | `int` | -           | `2300`  | CPU base frequency (in MHz) |
|`cpu-frequency-max`    | `int` | -           | `4000`  | CPU maximal frequency (In MHz, with Turbo-Boost) |
|`cpu-error-threshold`    | `float` | -           | `2.0`  | Error threshold for the CPU power models (in Watts) |
|`dram-error-threshold`    | `float` | -           | `2.0`  | Error threshold for the DRAM power models (in Watts) |
|`learn-min-samples-required`    | `int` | -           | `10`  | Minimum amount of samples required before trying to learn a power model |
|`learn-history-window-size`    | `int` | -           | `30`  | Size of the history window used to keep samples to learn from |
|`real-time-mode`    | `bool` | -           | `false`  | Pass the wait for reports from 4 ticks to 1 |

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
      "type": "influxdb",
      "uri": "127.0.0.1",
      "port": 8086,
      "db": "test_results",
      "collection": "power_consumption2"
    }
  },
  "cpu-frequency-base": 19,
  "cpu-frequency-min": 4,
  "cpu-frequency-max": 42,
  "cpu-error-threshold": 2.0,
  "disable-dram-formula": true,
  "sensor-report-sampling-interval": 1000
}
```

Some parameters of this configuration depend of your hardware. You can use we this [auto-configuration
script](../script/smartwatts_auto_config.md) in order to generate your configuration file.

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

### Running the Formula via CLI parameters

In order to run the Formula without a configuration file, run SmartWatts using one of the following command lines, depending on
the installation you used:

=== "Docker"

     ```sh
     docker run -t \
     --net=host \
     powerapi/smartwatts-formula --verbose \
     --input mongodb --model HWPCReport --uri mongodb://127.0.0.1 --db test --collection prep \
     --output influxdb --model PowerReport --uri 127.0.0.1 --port 8086 --db test_result \
     --cpu-frequency-base 19 \
     --cpu-frequency-min 4 \
     --cpu-frequency-max 42 \
     --cpu-error-threshold 2.0 \
     --disable-dram-formula \
     --sensor-report-sampling-interval 1000 \
     --real-time-mode false
     ```

=== "Pip"

    ```sh
    python -m smartwatts \
    --verbose \
    --input mongodb --model HWPCReport --uri mongodb://127.0.0.1 --db test --collection prep \
    --output influxdb --model PowerReport --uri 127.0.0.1 --port 8086 --db test_result \
    --cpu-frequency-base 19 \
    --cpu-frequency-min 4 \
    --cpu-frequency-max 42 \
    --cpu-error-threshold 2.0 \
    --disable-dram-formula \
    --sensor-report-sampling-interval 1000 \
    --real-time-mode false
    ```



???+ info "Estimations' Storage"
    Your `PowerReports` will be stored on InfluxDB. You can watch them in a grafana by using the [following tutorial](../grafana/grafana.md).

???+ tip "Using shortcuts for parameters' names"
    You use `-` instead of `--`.

# Auto-config Script

This script detects the frequencies (assuming that the language of your Linux Distribution is English) of your CPU and use them to provide a
configuration file for SmartWatts.

```sh
#!/usr/bin/env bash

maxfrequency=$(lscpu -b -p=MAXMHZ | tail -n -1| cut -d , -f 1)
minfrequency=$(lscpu -b -p=MINMHZ | tail -n -1 | cut -d , -f 1)
basefrequency=$(lscpu | grep "Model name" | cut -d @ -f 2 | cut -d G -f 1)
basefrequency=$(expr ${basefrequency}\*1000 | bc | cut -d . -f 1)

echo "
{
  \"verbose\": true,
  \"stream\": true,
  \"input\": {
    \"puller\": {
      \"model\": \"HWPCReport\",
      \"type\": \"socket\",
      \"uri\": \"127.0.0.1\",
      \"port\": 8080,
      \"collection\": \"test_hwpc\"
    }
  },
  \"output\": {
    \"pusher_power\": {
      \"type\": \"influxdb\",
      \"model\": \"PowerReport\",
      \"uri\": \"127.0.0.1\",
      \"port\": 8086,
      \"db\": \"test\",
      \"collection\": \"prep\"
    }
  },
  \"cpu-frequency-base\": $basefrequency,
  \"cpu-frequency-min\": $minfrequency,
  \"cpu-frequency-max\": $maxfrequency,
  \"cpu-error-threshold\": 2.0,
  \"disable-dram-formula\": true,
  \"sensor-report-sampling-interval\": 1000
}
" > ./config_file.json

```
