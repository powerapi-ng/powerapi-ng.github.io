# RAPL

RAPL stand for Running Average Power Limit, it is a feature of recent intel
processors that provide the energy consumption of the processor.

The RAPL formula is designed to mesure power consumption of domains (cpu or ram)
in real time.

The RAPL formula take HWPC report with RAPL event for each domains. It then
return the mesured power in a PowerReport for each domain.
This formula do not perform any other computation as its goal is only to track
global power consumption in a more readable way than raw RAPL.

# Installation

You can use [the following script](./script/rapl_install.sh) to install RAPL Formula and HWPC Sensor.

## From pypi

`pip install rapl-formula`

## From docker

`docker pull powerapi/rapl-formula`

## From deb file

Download the `.deb` files (rapl-formula and thespian) from the [latest
release](https://github.com/powerapi-ng/rapl-formula/releases)

Install rapl-formula with `sudo apt install ./python3-rapl-formula_0.5.0-1_all.deb`

# Quickstart

For running the RAPL formula we'll need two things:

- A sensor that provide HWPCReport. We'll use [HWPC sensor](./hwpc-sensor.md).
- A configuration for the formula. We provide an example bellow.

```json
{
  "verbose": true,
  "stream": true,
  "input": {
    "puller": {
      "model": "HWPCReport",
      "type": "socket",
      "uri": "127.0.0.1",
      "port": 8080,
      "collection": "test_hwpc"
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
  "enable-dram-formula": false,
  "sensor-report-sampling-interval": 500
}
```

Start by running the sensor (see [here](./hwpc-sensor_quickstart.md)) and a
mongodb.
Then run `rapl_formula` using one of the following command line, depending on
the installation you used:

- via pip : `python -m rapl_formula --config-file config_file.json`
- via docker `docker run rapl_formula <configuration>`
- via deb file : `rapl-formula --config-file config_file.json`

Your power report will be provided in the mongodb.

# User guide

## Configuration parameters

- `enable-cpu-formula` (bool) : Enable CPU formula, default=True
- `enable-dram-formula`(bool) : Enable DRAM formula, default=True
