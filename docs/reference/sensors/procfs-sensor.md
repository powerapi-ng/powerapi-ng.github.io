# Procfs Sensor

The Proc Filesystem Sensor is a tool that monitor the CPU usage of cgroup via
the Linux's proc filesystem.
It uses `pidstat` to retreive the percentage of CPU usage of each process.
It then use the `/sys/fs/perf_event` directory to find the appartenance of
processes to cgroup.

**The sensor need the cgroup version 1**. The version 2 is not supported yet.

## Installation

### From pyp

```bash
pip install procfs-sensor
```

### From docker

```bash
docker pull powerapi/procfs-sensor
```

### From deb file

Download the `.deb` file from the [latest
release](https://github.com/powerapi-ng/procfs-sensor/releases)

Install the sensor with

```bash
sudo apt install procfs-sensor-1.1.0.deb
```

### Using the binary

You can use the compiled version of the sensor available
[here](https://github.com/powerapi-ng/procfs-sensor/releases).

## Usage

Before running the sensor, first you need to define the cgroup you want to track.

Then, for executing the sensor you need a configuration file. You find an example below:

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

You can start the sensor with the following command line, depending on your installation:

- from docker:
```bash
docker -v ./config_file.json:/config_file.json run procfs-sensor --config_file config_file.json
```
- from pip:
```
python -m procfs_sensor --config-file config_file.json
```
In both cases, that configuration file name is `config_file.json`

You can use a TCP server to retreive the reports.

## Produced Reports
Profs Sensor produces `ProcfsReports`. More information about this kind of report can be found [here](../../guides/reports/#procfs-report).
