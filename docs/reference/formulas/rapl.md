# RAPL Formula

RAPL stands for Running Average Power Limit. It is a feature of recent Intel
processors that provide the energy consumption of the processor.

The RAPL Formula is designed to mesure power consumption of domains (CPU or RAM)
in real time.

The RAPL Formula takes HWPC Report with RAPL event for each domains. It then
returns the mesured power in a PowerReport for each domain.
This Formula does not perform any other computation as its goal is only to track
global power consumption in a more readable way than raw RAPL.

## Installation

You can use [the following script](../script/rapl_install.sh) to install RAPL Formula and HWPC Sensor.

=== "Docker"

    ```sh
    docker pull powerapi/powerapi
    ```

=== "Pypi"

    ```sh
    pip install powerapi
    ```

## Usage

For running the RAPL Formula you need: a Source and a Destination, a Sensor that provides `HWPCReports` and a configuration.

### Source and Destination

For running RAPL we are using MongoDB as Source and Destination as a docker container.

To start a MongoDB instance via the command line

```sh
docker run -d --name mongo_source_destination -p 27017:27017 mongo
```

### Sensor
[HWPC Sensor](../sensors/hwpc-sensor.md) is used in order to get `HWPCReports`. Start by installing the HWPC Sensor (see
[here](../sensors/hwpc-sensor.md#installation)) and start it (see
[here](../sensors/hwpc-sensor.md#usage)).

### Parameters

Besides the [basic parameters](configuration_files.md), the following ones are specific to RAPL:

| Parameter                | Type   | CLI shortcut  | Default Value                                      | Description                             |
| -------------            | -----  | ------------- | -------------                                      | ------------------------------------    |
|`disable-cpu-formula`     | `bool` (flag)    | -           | `true`                                             | Disable CPU formula                    |
|`disable-dram-formula`     | `bool` (flag)    | -           | `true`                                             | Disable DRAM formula                    |
|`cpu-rapl-ref-event`     | `string`    | -           | `RAPL_ENERGY_PKG`   | RAPL event used as reference for the CPU power models                    |
|`dram-rapl-ref-event`    | `string`    | -           | `RAPL_ENERGY_DRAM`   | RAPL event used as reference for the DRAM power models |
|`sensor-report-sampling-interval`    | `int`    | -           | `1000`   | The frequency with which measurements are made (in milliseconds)|


### Running the Formula with a Configuration File

Below an example is provided by using MongoDB as Source and Destination.

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
      "type": "mongodb",
      "model": "PowerReport",
      "type": "mongodb",
      "uri": "mongodb://127.0.0.1",
      "db": "test",
      "collection": "results"
    }
  },
  "disable-dram-formula": true,
  "sensor-report-sampling-interval": 500
}
```

???+ info "Alternative Source or Destination"
    If you want to use another Source or Destination, please check the documentation [here](../database/sources_destinations.md) and modify the configuration file according to the Source and/or Destination that you want to use.

Once you have your configuration file, run RAPL using one of the following command lines, depending on
the installation you use:


=== "Docker"

    ```sh
    docker run -t \
    --net=host \
    -v $(pwd)/config_file.json:/config_file.json \
    powerapi/powerapi --config-file /config_file.json \
    ```

=== "Pip"

    ```sh
    python -m powerapi --config-file config_file.json
    ```

### Running the Formula via CLI parameters

In order to run the Formula without a configuration file, run RAPL using one of the following command lines, depending on
the installation you use:

=== "Docker"

     ```sh
     docker run -t \
     --net=host \
     powerapi/powerapi --verbose \
     --input mongodb --model HWPCReport --uri mongodb://127.0.0.1 --db test --collection prep \
     --output mongodb --model PowerReport --uri mongodb://127.0.0.1 --db test --collection results \
     --disable-dram-formula \
     --sensor-report-sampling-interval 500
     ```

=== "Pip"

    ```sh
    python -m powerapi --verbose \
    --input mongodb --model HWPCReport --uri mongodb://127.0.0.1 --db test --collection prep \
    --output mongodb --model PowerReport --uri mongodb://127.0.0.1 --db test --collection results \
    --disable-dram-formula \
    --sensor-report-sampling-interval 500
    ```

???+ info "Estimations' Storage"
    Your `PowerReports` will be stored on MongoDB.

???+ tip "Using shortcuts for parameters' names"
    You use `-` instead of `--`.
