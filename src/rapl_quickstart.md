# RAPL Quickstart

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
- via docker `docker run rapl_formula --config-file config_file.json`
- via deb file : TODO

Your power report will be provided in the mongodb.
