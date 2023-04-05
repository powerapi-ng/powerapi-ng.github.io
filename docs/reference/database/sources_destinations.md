# Sources and Destinations

A PowerAPI Formula uses Sources and Destinations in order to retrieve metrics and store estimations.

For each Source/Destination the parameters to specify are differents. For each one of them,
its parameters are specified in following sections.

## Summary
| Name     | Source   | Destination  | CLI `input`/`ouput` parameter value                                      | JSON `type` tag parameter value                             |
| ------------- | -----  | ------------- | -------------                                      | ------------------------------------    |
| MongoDB | Yes  | Yes | mongodb                                      | mongodb    |
| InfluxDB | No  | Yes | influxdb                                      | influxdb    |
| InfluxDB2 | No  | Yes | influxdb2                                      | influxdb2    |
| CSV | Yes  | Yes | csv                                      | csv    |
| Socket | Yes  | No | socket                                      | socket    |
| File Database | Yes  | Yes | filedb                                      | filedb    |
| Prometheus | No  | Yes | prom                                      | prom    |

## MongoDB

If you want to use a Mongo Database in your Formula, you have to specify
`mongodb` as the `type` of a puller (Source) or a pusher (Destination).

### Parameters

The list of parameters you have to provide are:

| Parameter     | Type   | CLI shortcut  | Default Value                                              | Description                             |
| ------------- | -----  | ------------- | -------------                                              | ------------------------------------    |
|`uri`          | string | `u` (`U` for `HWPCSensor`)           | N/A                                                        | The IP address of your MongoDB instance |
|`db` (`database` for `HWPCSensor`)           | string | `d` (`D` for `HWPCSensor`)            | N/A                                                        | The name of your database               |
|`collection`   | string | `c` (`C` for `HWPCSensor`)          | N/A                                                        | The name of the collection inside `db`  |
|`name`         | string | `n`           | `"puller_mongodb"` (Source), `pusher_mongodb` (Destination)| The related puller/pusher name. This parameter is not used by `HWPCSensor`                 |
|`model`        | string | `m`           | `"HWPCReport"` (Source), `PowerReport` (Destination)         | The Report type stored by the database  |

### JSON File Excerpt

Below you find a configuration excerpt for this kind of Source/Destination.

```json
{
  "type": "mongodb",
  "uri": "mongodb://127.0.0.1",
  "db": "test",
  "collection": "prep"
}
```
!!! info "The default port for MongoDB is 27017"

## Influx DB 1.8

If you want to use InfluxDB 1.8 in your Formula as Destination, you have to specify
`influxedb` as the `type` of a pusher.

### Parameters

The list of parameters you have to provide are:

| Parameter     | Type   | CLI shortcut  | Default Value                                        | Description                             |
| ------------- | -----  | ------------- | -------------                                        | ------------------------------------    |
|`uri`          | string | `u`           | N/A                                                  | The IP address of your Influxdb instance|
|`db`           | string | `d`           | N/A                                                  | The name of your database               |
|`port`         | int    | `p`           | N/A                                                  | The port of communication               |
|`tags`         | string | `t`           | N/A                                                  | The report tags                         |
|`name`         | string | `n`           | `"pusher_influxdb"`                                    | The related pusher name                 |
|`model`        | string | `m`           | `"PowerReport"`                                        | The Report type stored by the database  |

InfluxDB can only be used as a Destination.

### JSON File Excerpt

Below you find an example of configuration excerpt for this kind of Destination.

```json
{
  "tags": "socket",
  "model": "PowerReport",
  "type": "influxdb",
  "uri": "127.0.0.1",
  "port": 8086,
  "db": "test_influxdb"
}
```

!!! info "The name used for InfluxDB measurements is `power_consumption`"

## Influx DB 2

If you want to use InfluxDB 2 in your Formula as Destination, you have to specify
`influxedb2` as the `type` of a pusher.

### Parameters

The list of parameters you have to provide are:

| Parameter     | Type   | CLI shortcut  | Default Value | Description                             |
| ------------- | -----  | ------------- | ------------- | ------------------------------------    |
|`uri`          | string | `u`           | N/A           | The IP address of your Influxdb instance|
|`db`           | string | `d`           | N/A           | The name of your bucket (database)      |
|`port`         | int    | `p`           | N/A           | The port of communication               |
|`token`        | string | `k`           | N/A           | The token for accesing the database. The token owner must have write/read permissions on the bucket               |
|`org`          | string | `g`           | N/A           | The name of the organisation associated to the bucket               |
|`tags`         | string | `t`           | N/A           | The report tags                         |
|`name`         | string | `n`           | `"pusher_influxdb2"`                                    | The related pusher name                 |
|`model`        | string | `m`           | `"PowerReport"`  | The Report type stored by the database  |


InfluxDB2 can only be used as a Destination.

### JSON File Excerpt

Below you find an example of configuration excerpt for this kind of Destination.

```json
{
  "model": "PowerReport",
  "type": "influxdb2",
  "uri": "http://127.0.0.1",
  "port": 8086,
  "db": "influxdb2",
  "org": "org_test",
  "token": "mytoken"
}
```


## CSV

If you want to use a CSV file in your Formula as Source or Destination, you have to specify
`csv` as the `type` of a puller or a pusher.

### Parameters

The list of parameters you have to provide are:

| Parameter     | Type    | CLI shortcut  | Default Value | Description                                                                   |
| ------------- | -----   | ------------- | ------------- | ------------------------------------                                          |
|`files`(Source)| string  | `f`           | Empty list           | The list of input CSV files with the format file1,file2,file3...              |
|`directory` (Destination, `uri` for `HWPCSensor`)| string        | `d` (`U` for `HWPCSensor`)          | Current directory           | The directory where output CSV files will be written          |
|`name`         | string | `n`           | `"puller_csv"` (Source), `"pusher_csv"` (Destination)| The related puller/pusher name. This parameter is not used by `HWPCSensor`                 |
|`model`        | string | `m`           | `"HWPCReport"` (Source), `"PowerReport"` (Destination)   | The Report type stored in CSV files. This parameter is not used by `HWPCSensor`     |

### JSON File Excerpt

Below you find an example of configuration excerpt for this kind of Source/Destination.

```json
{
  "type": "csv",
  "directory": "/tmp/sensor_output/"
}
```

## Socket

If you want to use a TCP socket in your Formula as Source, you have to specify
`socket` as the `type` of a puller.
This Source is made for `stream` mode active only.

### Parameters

The list of parameters you have to provide are:

| Parameter     | Type   | CLI shortcut  | Default Value                                      | Description                             |
| ------------- | -----  | ------------- | -------------                                      | ------------------------------------    |
|`port`         | int    | `p`           | N/A                                                | The port of communication               |
|`name`         | string | `n`           | `"puller_socket"` | The related puller name                 |
|`model`        | string | `m`           | `"HWPCReport"` | The Report type managed by the socket   |


### JSON File Excerpt

Below you find an example of configuration excerpt for this kind of Source.

```json
{
  "type": "socket",
  "port": 8080
}
```

## File Database

If you want to use a File Database as Source/Destination in your Formula your have to specify
`filedb` as the `type` of a puller or a pusher.
The File Database is made for stream mode only. It should contain only the last
report when used as a Destination.

### Parameters

The list of parameters you have to provide are:

| Parameter     | Type   | CLI shortcut  | Default Value                                      | Description                             |
| ------------- | -----  | ------------- | -------------                                      | ------------------------------------    |
|`filename`     | int    | `f`           | N/A                                                | The name of the file                    |
|`name`         | string | `n`           | `"pusher_filedb"` | The related pusher name                 |
|`model`        | string | `m`           | `"HWPCReport"` (Source) `"PowerReport"` (Destination)  | The Report type stored in the file      |

### JSON File Excerpt

Below you find an example of configuration excerpt for this kind of Source/Destination.

```json
{
  "type": "filedb",
  "filename": /tmp/database/input_file.json
}
```

## Prometheus

If you want to use a Prometheus instance to expose reports to be scraped, you have to specify
`prom` as the `type` of a pusher in your formula configuration file.

### Parameters

The list of parameters you have to provide are:

| Parameter     | Type   | CLI shortcut  | Default Value                                      | Description                             |
| ------------- | -----  | ------------- | -------------                                      | ------------------------------------    |
|`uri`          | string | `u`           | N/A                                                | The IP address of your Promtheus instance |
|`port`         | int | `p`              | N/A                                                | The port of communication                  |
|`tags`         | string | `t`           | N/A                                                | The Report tags                    |
|`metric_name`  | string | `M`           | N/A                                                | The exposed metric name                    |
|`metric_description`  | string | `d`    | `"energy consumption"`                               | The exposed metric description                    |
|`aggregation_period`  | int | `A`    | 15                                                    | The number of second for the metric must be aggregated before compute statistics on them                    |
|`name`         | string | `n`           | `"pusher_prom"` | The related pusher name                 |
|`model`        | string | `m`           | `"PowerReport"` | The Report type exposed by Prometheus      |


Promtheus can only be used as a Destination that monitors reports but they will be not stored by this service.  

### JSON File Excerpt

Below you find an example of configuration excerpt for this kind of Destination.

```json
{
  "type": "prom",
  "uri": "127.0.0.1",
  "port": 8080,
  "metric_name": test
}
```
