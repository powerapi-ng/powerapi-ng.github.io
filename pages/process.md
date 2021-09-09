---
title: "Monitor a group of process "
permalink: process.html
sidebar: tuto_sidebar
---

## install hwpc-sensor and smartwatts formula

- download this deb files : 

	- [hwpc_sensor](https://github.com/powerapi-ng/powerapi-ng.github.io/raw/master/deb/hwpc-sensor-1.0.deb)
	- [powerapi](https://github.com/powerapi-ng/powerapi-ng.github.io/raw/master/deb/python3-powerapi_0.10.0-1_all.deb)
	- [smartwatts-formula](https://github.com/powerapi-ng/powerapi-ng.github.io/raw/master/deb/python3-smartwatts_0.7.0-1_all.deb)
	
- and install it : 
```
$ dpkg -i hwpc-sensor-1.0.deb python3-powerapi_0.10.0-1_all.deb python3-smartwatts_0.7.0-1_all.deb
```

## Configure hwpc-sensor and smartwatts formula

write this configuration in `config_sensor.json`
```
{
    "name": "test_sensor",
    "verbose": true,
    "frequency": 500,
    "output": {
        "type": "socket",
        "uri": "127.0.0.1",
        "port": 8080
    },
    "system":{
        "rapl":{
            "events": ["RAPL_ENERGY_PKG"],
            "monitoring_type": "MONITOR_ONE_CPU_PER_SOCKET"
        },
        "msr": {
            "events": ["TSC", "APERF", "MPERF"]
        }
    },
    "container":{
        "core":{
            "events": ["CPU_CLK_THREAD_UNHALTED:REF_P", "CPU_CLK_THREAD_UNHALTED:THREAD_P", "LLC_MISSES", "INSTRUCTIONS_RETIRED"]
        }
    }
}
```

write this configuration in `config_formula.json`

```
{
    "verbose": true,
    "stream": true,
    "input":{
        "puller":{
            "model": "HWPCReport",
            "port": 8080,
            "type": "socket"
        }},
    "output":{
        "power":{
            "type": "influxdb",
            "uri": "localhost",
            "port": 8086,
            "db": $USER_ID,
            "model": "PowerReport"
        }},
    "formula":{
        "cpu-ratio-base": $RATIO_BASE,
        "cpu-ratio-min": $RATIO_MIN,
        "cpu-ratio-max": $RATIO_MAX,
        "cpu-error-threshold": 2.0,
        "disable-dram-formula": true,
        "sensor-reports-frequency": 500
    }
}
```


## Configure output
- launch an influx database with docker : `$ docker run -d --name influx --rm --net=host influxdb:1.8`
- launch a grafana instance with docker : `$ docker run -d --rm --name=grafana --net=host grafana/grafana`

## launch hwpc-sensor and smartwatts-formula

- hwpc-sensor : `$ hwpc-sensor --config-file config_sensor.json`
- smartwatts-formula : `$ python3 -m smartwatts --config-file config_formula.json`

### Configure grafana

connect to [http://localhost](http://localhost) and follow this [tutorial](/grafana.html)
	

## If nothing works ...

use this configuration file for formula
```
{
    "verbose": true,
    "stream": true,
    "input":{
        "puller":{
            "model": "HWPCReport",
            "port": 8080,
            "type": "socket"
        }},
    "output":{
        "power":{
            "type": "influxdb",
            "uri": "powerapi.lille.inria.fr",
            "port": 27017,
            "db": $USER_ID,
            "model": "PowerReport"
        }},
    "formula":{
        "cpu-ratio-base": $RATIO_BASE,
        "cpu-ratio-min": $RATIO_MIN,
        "cpu-ratio-max": $RATIO_MAX,
        "cpu-error-threshold": 2.0,
        "disable-dram-formula": true,
        "sensor-reports-frequency": 500
    }
}
```
- launch sensor with 
```
$ docker run --privileged  -v /sys:/sys -v /var/lib/docker/containers:/var/lib/docker/containers:ro -v /tmp/powerapi-sensor-reporting:/reporting --rm --net=host -v $(pwd):/srv powerapi/hwpc-sensor:tuto --config-file /srv/config_sensor.json`
```
- launch smartwatts with :
```
$ docker run --rm --net=host -v $(pwd):/srv powerapi/smartwatts-formula:latest --config-file /srv/config_formula.json
```
