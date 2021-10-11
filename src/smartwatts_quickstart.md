# SmartWatts Quickstart

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
      "type": "socket",
      "uri": "127.0.0.1",
      "port": 8080
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
  "cpu-ratio-base": 19,
  "cpu-ratio-min": 4,
  "cpu-ratio-max": 42,
  "cpu-error-threshold": 2.0,
  "disable-dram-formula": true,
  "sensor-report-sampling-interval": 1000
}
```

The configuration can depend of your hardware, we provide an [auto-configuration
script](./smartwatts_auto_config.md).

Start by running the sensor (see [here](./hwpc-sensor-quickstart.md)) and a
mongodb.
For the sensor use the following config file:

```json
{
  "name": "sensor",
  "verbose": true,
  "frequency": 500,
  "output": {
    "type": "socket",
    "uri": "127.0.0.1",
    "port": 8080
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

Then run `smartwatts` using one of the following command line, depending on
the installation you used:

- via pip : `python -m smartwatts --config-file config_file.json`
- via docker `docker run smartwatts --config-file config_file.json`
- via deb file : TODO

Your power report will be provided in the mongodb.
