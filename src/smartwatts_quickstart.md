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
  "cpu-ratio-base": 19,
  "cpu-ratio-min": 4,
  "cpu-ratio-max": 42,
  "cpu-error-threshold": 2.0,
  "disable-dram-formula": true,
  "sensor-reports-frequency": 1000
}
```

The configuration can depend of your hardware, we provide an [auto-configuration
script](./smartwatts_auto_config.md).

Start by running the sensor (see [here](./hwpc-sensor-quickstart.md)) and a
mongodb.
Then run `smartwatts` using one of the following command line, depending on
the installation you used:

- via pip : `python -m smartwatts --config-file config_file.json`
- via docker `docker run smartwatts --config-file config_file.json`
- via deb file : TODO

Your power report will be provided in the mongodb.
