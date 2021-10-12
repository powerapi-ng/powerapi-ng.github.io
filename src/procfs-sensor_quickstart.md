# Procfs Sensor Quickstart

For running the sensor, first you need to define the cgroup you want to track.

The for running the sensor you need configuration. We provide an example bellow.

```json
{
  "name": "procfs_sensor",
  "verbose": true,
  "frequency": 500,
  "output": {
    "type": "socket",
    "uri": "127.0.0.1",
    "port": 8080
  },
  "target": ["cgroup1", "cgroup2", ...]
}
```

You can start the sensor with the following command line, depending on your installation :

- from docker : `docker powerapi/procfs-sensor --config-file config_file.json `
- from pip : `python -m procfs-sensor --config-file config_file.json`

You can use a TCP server to retreive the reports.
