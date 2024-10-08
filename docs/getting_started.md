# Getting started

## Define elements to monitor

### Create a cGroup

We need a subset of runnings programs to be monitored. For this, we use the 
Linux abstraction of [cGroups](https://www.redhat.com/sysadmin/cgroups-part-one).  

In order to create a cGroup, the following command can be used from CLI :  

```sh
cgcreate -g perf_event:new_cgroup_name
```

Check [here](./reference/cgroup/cgroup_v1_activation.md) if you have trouble 
creating the cgroup.  

### Add programs to the group

Once the group created, we need to fill it with programs to be monitored. 
To do so, you can use the following :  

```sh
cgclassify -g perf_event:new_cgroup_name PID
```

with `PID`, the pid of the process you want to monitor. If you want to monitor a
program composed of many process, replace PID with `$(pidof program_name)`.

### Example program to monitor

[stress-ng](https://wiki.ubuntu.com/Kernel/Reference/stress-ng) can be used to 
generate load on one's system.  
An example usage, once installed :  

```sh
stress-ng --cpu 1 --timeout 5m
```

The PID can be found using :  

```sh
STRESS_PID="$(pgrep stress-ng)"
```

## Which components to get a complete stack  

If you wish to get started as soon as possible, the following archive will allow you to deploy the following elements :  

1. A MongoDB instance to store the [Sensor](./reference/sensors/hwpc-sensor.md)
Reports

2. An InfluxDB2 instance to store the [Formulas](./reference/formulas/smartwatts.md)

3. An [HWPC-Sensor](./reference/sensors/hwpc-sensor.md) that outputs its 
[HWPCReports](./reference/reports/report.md#HWPCReport) in a MongoDB Database, 
within the HWPCReport Collection.  

4. A [SmartWatts](./reference/formulas/smartwatts.md) that streams the 
[HWPCReports](./reference/reports/report.md#HWPCReport) from the MongoDB 
Database Collection, processes it and outputs its 
[PowerReports](./reference/reports/report.md#PowerReports) in an InfluxDB2 
Database within the PowerReport Collection  

5. A Grafana instance to visualize the
[PowerReports](./reference/reports/report.md#PowerReports) from the InfluxDB2 
instance

## Preparation

You can download the archive using :   

```sh 
wget "https://github.com/powerapi-ng/powerapi-ng.github.io/tree/master/examples/powerapi-stack.zip"
unzip powerapi-stack.zip && cd powerapi-stack
```

From this archive, you will have all the necessary files to get started, let us break down each elements.  

### Docker-Compose 

```yaml
# ./docker-compose.yaml

version: '3.8'
services:
  mongodb:
    image: mongo:latest
    container_name: mongodb
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
    environment:
      MONGO_INITDB_DATABASE: powerapi
    command: ["mongod"]
    networks:
      - powerapi_network

  influxdb:
    image: influxdb:2.0
    container_name: influxdb
    ports:
      - "8086:8086"
    volumes:
      - influxdb_data:/var/lib/influxdb2
    environment:
      INFLUXDB_DB: powerapi
      INFLUXDB_ADMIN_USER: admin
      INFLUXDB_ADMIN_PASSWORD: admin123
      INFLUXDB_USER: powerapi_user
      INFLUXDB_PASSWORD: powerapi_password
    networks:
      - powerapi_network

  hwpc_sensor:
    image: powerapi/hwpc-sensor
    container_name: hwpc_sensor
    volumes:
      - ./config/hwpc-sensor-config.json:/hwpc-sensor-config.json 
    command: --config-file /hwpc-sensor-config.json 
    networks:
      - powerapi_network
    depends_on:
      - mongodb

  smartwatts:
    image: powerapi/smartwatts
    container_name: smartwatts
    volumes:
      - ./config/smartwatts-config.json:/smartwatts-config.json  
    command: --config /smartwatts-config.json  
    networks:
      - powerapi_network
    depends_on:
      - mongodb
      - influxdb

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
      - ./config/provisioning:/etc/grafana/provisioning  
    networks:
      - powerapi_network
    depends_on:
      - influxdb

volumes:
  mongo_data:
  influxdb_data:

networks:
  powerapi_network:
    driver: bridge
```

### HWPC-Sensor Configuration

As described in the [HWPC-Sensor Documentation](./reference/sensors/hwpc-sensor.md#global-parameters) 
several parameters can be set, both globally and for specific Groups monitored. 
The provided docker-compose.yaml file use configuration files to set those parameters.  
An example configuration file for HWPC-Sensor is given below and available in the archive presented [above](./getting_started.md#preparation) :  

```json
# ./hwpc-sensor-config.json

{
  "verbose": false,
  "frequency": 1000,
  "name": "hwpc-sensor",
  "cgroup_basepath": "/sys/fs/cgroup/perf_event",
  "system": {
    "type": "MONITOR_ALL_CPU_PER_SOCKET",
    "events": ["RAPL_ENERGY_PKG", "RAPL_ENERGY_DRAM"]
  },
  "container": {
    "type": "MONITOR_ALL_CPU_PER_SOCKET",
    "events": ["RAPL_ENERGY_PKG", "RAPL_ENERGY_DRAM"]
  },
  "output": {
    "type": "mongodb",
    "uri": "mongodb://mongodb:27017",
    "db": "powerapi",
    "collection": "HWPCReports"
  }
}
```

### SmartWatts Configuration

As described in the [SmartWatts Documentation](./reference/formulas/smartwatts.md#global-parameters) 
several parameters can be set for the Formulas. 
The provided docker-compose.yaml file use configuration files to set those parameters.  
An example configuration file for SmartWatts is given below and available in the archive presented [above](./getting_started.md#preparation) :  

```json
# ./smartwatts-config.json

{
  "cpu_tdp": 125,
  "cpu_base_clock": 100,
  "cpu_base_freq": 2100, # Use lscpu and look for CPU MHz field to know the correct value
  "cpu_error_threshold": 2.0,
  "dram_error_threshold": 2.0,
  "learn_min_samples_required": 10,
  "learn_history_window_size": 60,
  "sensor_reports_frequency": 1000,
  "input_mongo": {
    "uri": "mongodb://mongodb:27017/powerapi",
    "collection": "HWPCReports"
  },
  "output_influx": {
    "uri": "http://influxdb:8086",
    "org": "powerapi_org",
    "bucket": "PowerReports",
    "token": "INFLUXDB_API_TOKEN_GENERATED"
  }
}
```

### Grafana Configuration

Grafana has to be configured to use our InfluxDB2 instance as a datasource, 
it should also know our dashboard file in order to visualize it.  

#### Filesystem structure 

The following filesystem structure is presented in the archive presented [above](./getting_started.md#preparation) :   :  


```sh
|powerapi-stack/
|--grafana_config/
|----provisioning/
|------dashboards/
|--------dashboard.yaml
|--------reports.json
|------datasources/
|--------datasource.yaml
|...
```

#### Datasource file

The following file gives information to Grafana to use InfluxDB2 as Datasource:

```yaml
# ./grafana_config/provisioning/datasources/datasource.yaml

apiVersion: 1
datasources:
  - name: InfluxDB
    type: influxdb
    access: proxy
    url: http://influxdb:8086
    isDefault: true
    database: PowerReports
    user: powerapi_user
    password: powerapi_password
    jsonData:
      version: Flux
      organization: powerapi_org
      defaultBucket: PowerReports
      token: INFLUXDB_API_TOKEN_GENERATED
    editable: true
```

#### Dashboard files

The following files give information to Grafana:

1. Where to search pre-configured Dashboards  
2. How to configure our Dashboards

```yaml
# ./grafana_config/provisioning/dashboards/dashboard.yaml

apiVersion: 1
providers:
  - name: 'default'
    folder: ''
    type: file
    options:
      path: /etc/grafana/provisioning/dashboards
```

```json
# ./grafana_config/provisioning/dashboards/reports.json

{
  "id": null,
  "title": "PowerAPI Dashboard",
  "tags": [],
  "timezone": "browser",
  "schemaVersion": 16,
  "version": 0,
  "panels": [
    {
    }
  ]
}
```

## Turn the key 

Once all set, you shall be able to initiate the stack with :  

```sh
docker-compose -d up
```

This first spin-up will create the DBs and the Sensor.  
Both SmartWatts Formulas and Grafana will struggle as they need an InfluxDB API key.  
To resolve this, you can run :  
```sh
influx auth create --org powerapi_org --read-buckets --write-buckets
```

You will obtain a token to replace the *INFLUXDB_API_TOKEN_GENERATED* placeholder in the `smartwatts-config.json` file and in `grafana_config/provisioning/datasources/datasource.yaml`  

Once both changed, another `docker-compose -d up` should do the trick to start the
remaining components.  

Thus, once deployed, you can access [Grafana](https://localhost:3000) by default
on http://localhost:8080 with its basic credentials : `admin/admin`.

In the dashboards sections, basic dashboards will be provisionned with PowerReports 
from SmartWatts providing real time insights about you consumption.  

Feel free to try yo make your own visualization and take a look at 
[this documentation](./reference/grafana/grafana.md) for further details.  
