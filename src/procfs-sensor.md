# Procfs-Sensor

The Proc Filesystem Sensor is a tool that monitor the CPU usage of cgroup via
the linux's proc filesystem.
It use `pidstat` to retreive the percentage of CPU usage of each process.
It then use the `/sys/fs/perf_event` directory to find the appartenance of
processes to cgroup.

The sensor need the cgroup version 1. The version 2 is not supported yet.

# Installation

## From pypi

`pip install procfs-sensor`

## From docker

`docker pull powerapi/procfs-sensor`

## From deb file

Download the `.deb` file from the [latest
release](https://github.com/powerapi-ng/procfs-sensor/releases)

Install the sensor with `sudo apt install procfs-sensor-1.1.0.deb`

## Using the binary

You can use the compiled version of the sensor (available
[here](https://github.com/powerapi-ng/procfs-sensor/releases))

# Quickstart

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

- from docker : ``docker -v ./config_file.json:/config_file.json run procfs-sensor --config_file config_file.json`
- from pip : `python -m procfs_sensor --config-file config_file.json`

You can use a TCP server to retreive the reports.
