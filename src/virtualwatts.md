# VirtualWatts

VirtualWatts is a software-defined power meter based on the PowerAPI toolkit.
VirtualWatts is a configurable software that can estimate the power consumption
of software inside a Virtual Machine (VM) in real-time.

VirtualWatts use the estimation of energy consumption of the VM, computed by
[SmartWatts](https://github.com/powerapi-ng/smartwatts), and the cpu usage of
each process inside the VM, computed by [Procfs
Sensor](https://github.com/powerapi-ng/procfs-sensor).

# Installation

You can use [the following script](./script/virtualwatts_install.sh) to install VirtualWatts and Procfs Sensor.

## From pypi

`pip install virtualwatts`

## From docker

`docker pull powerapi/virtualwatts-formula`

## From deb file

Download the `.deb` file from the [latest
release](https://github.com/powerapi-ng/virtualwatts-formula/releases)

Install virtualwatts with `sudo apt install ./python3-virtualtwatts_0.1.1-1_all.deb`

# Quickstart

For running the VirtualWatts formula we'll need several things:

- Smartwatts running on the host machine
- A file `SW_output`, shared with the host that will be used as database
- The Procfs sensor running inside the VM
- A configuration file for each.

VirtualWatts configuration :

```json
{
    'verbose': True,
    "stream":True,
    "input": {
        "puller_filedb": {
            "type": "filedb",
            "model": "PowerReport",
            "filename": "SW_output"
            },
        "puller_tcpdb": {
            "type" : "socket",
            "model": "ProcfsReport",
            "uri": "127.0.0.1",
            "port": self.port
        }
    },
    "output": {
        "power_pusher": {
        "type": "influxdb",
        "model": "PowerReport",
        "uri": "127.0.0.1",
        "port": 8086,
        "db": "test",
        "collection": "prep"
        }
    },
    "delay-threshold": 500,
    "sensor-reports-sampling-interval": datetime.timedelta(500)
}
```

Start by running Smartwatts with a `filedb` output.
Then run `virtualwatts` using one of the following command line, depending on
the installation you used:

- via pip : `python -m virtualwatts --config-file config_file.json`
- via docker `docker run -t --net=host -v $(pwd)/config_file.json:/config_file.json powerapi/virtualwatts --config-file /config_file.json `
- via deb file : `virtualwatts --config-file config_file.json`

After that run the procfs sensor. Your power report will be provided in the influxdb. You can watch them in a
grafana using the [following tutorial](./grafana.md)
