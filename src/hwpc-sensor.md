# Hwpc-Sensor

HardWare Performance Counter (HWPC) Sensor is a tool that monitor the Intel CPU
performance counter and the power consumption of CPU.

Hwpc-sensor use the RAPL (Running Average Power Limit) technology to monitor CPU
power consumption. This technology is only available on Intel Sandy Bridge
architecture or higher.

The sensor use the perf API of the Linux kernel. It is only available on Linux
and need to have root access to be used.

The sensor couldn’t be used in a virtual machine, it must access (via Linux
kernel API) to the real CPU register to read performance counter values.

# Installation

## From docker

`docker pull powerapi/hwpc-sensor`

## From deb file

Download the `.deb` file from the [latest
release](https://github.com/powerapi-ng/hwpc-sensor/releases)

Install the sensor with `sudo apt install hwpc-sensor-1.1.0.deb`

## Using the binary

You can use the compiled version of the sensor (available
[here](https://github.com/powerapi-ng/hwpc-sensor/releases))

# Quickstart

For running the sensor, first we need a configuration. We provide an example bellow.

```json
{
  "name": "sensor",
  "verbose": true,
  "frequency": 500,
  "output": {
    "type": "mongodb",
    "uri": "mongodb://127.0.0.1",
    "database": "db_sensor",
    "collection": "report_0"
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

Start a mongo db and then you can start the sensor with the following command line, depending on your
installation :

- from docker : `docker run --rm --net=host --privileged --pid=host -v /sys:/sys -v /var/lib/docker/containers:/var/lib/docker/containers:ro -v /tmp/powerapi-sensor-reporting:/reporting -v $(pwd):/srv -v $(pwd)/config_file.json:/config_file.json powerapi/hwpc-sensor --config-file /config_file.json `
- from binary : `./hwpc-sensor --config-file config_file.json`

The reports will be provided in your mongodb.
