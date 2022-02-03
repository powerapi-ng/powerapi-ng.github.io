# SmartWatts

SmartWatts is a software-defined power meter based on the PowerAPI toolkit.
SmartWatts is a configurable software that can estimate the power consumption of
software in real-time.
SmartWatts need to receive several metrics provided by
[hwpc-sensor](https://github.com/powerapi-ng/hwpc-sensor) :

- The Running Average Power Limit (RAPL)
- TSC
- APERF
- MPERF
- CPU_CLK_THREAD_UNHALTED:REF_P
- CPU_CLK_THREAD_UNHALTED:THREAD_P
- LLC_MISSES
- INSTRUCTIONS_RETIRED

These metrics are then used as inputs for a power model that estimate the power
consumption of each software.
The model can derive from the reality, each time the `cpu-error-threshold` is
reached it learn a new power model, using the previous reports.

The choice of those specific metrics is motivated in [SmartWatts: Self-Calibrating
Software-Defined Power Meter for Containers](https://hal.inria.fr/hal-02470128)

# Installation

You can use [the following script](./script/smartwatts_install.sh) to install Smartwatts and HWPC Sensor.

## From pypi

`pip install smartwatts`

## From docker

`docker pull powerapi/smartwatts-formula`

## From deb file

Download the `.deb` file from the [latest
release](https://github.com/powerapi-ng/smartwatts-formula/releases)

Install smartwatts with `sudo apt install ./python3-smartwatts_0.8.0-1_all.deb`

# Quickstart

For running the Smartwatts formula we'll need two things:

- A sensor that provide HWPCReport. We'll use [HWPC sensor](./hwpc-sensor.md).
- A configuration for the formula. We provide an example bellow.

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
      "uri": "mongodb://127.0.0.1",
      "db": "test",
      "collection": "prep"
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

The configuration can depend of your hardware, we provide an [auto-configuration
script](./smartwatts_auto_config.md).

Start by installing the hwpc-sensor (see
[here](./hwpc-sensor.md#installation)) and start it (see
[here](./hwpc-sensor.md#quickstart)).
You also need to start an mongodb via the command line `docker run -d --name mongo_sw -p 27017:27017 mongo`.

Then run `smartwatts` using one of the following command line, depending on
the installation you used:

- via pip : `python -m smartwatts --config-file config_file.json`
- via docker `docker run -t --net=host -v $(pwd)/config_file.json:/config_file.json powerapi/smartwatts-formula --config-file /config_file.json `
- via deb file : `smartwatts --config-file config_file.json`

Your power report will be provided in the influxdb. You can watch them in a
grafana using the [following tutorial](./grafana.md)

# Auto-config Script

This script detect the frequency of your cpu and use them to provide a
configuration file for Smartwatts.

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
