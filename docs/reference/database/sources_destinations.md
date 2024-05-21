# Sources and Destinations

A PowerAPI Formula uses Sources and Destinations in order to retrieve metrics and store estimations.

For each Source/Destination the parameters to specify are different. For each one of them,
its parameters are specified in following sections.

## Summary
| Name     | Source   | Destination  | CLI `input`/`ouput` parameter value                                      | JSON `type` tag parameter value                             |
| ------------- | -----  | ------------- | -------------                                      | ------------------------------------    |
| MongoDB | Yes  | Yes | mongodb                                      | mongodb    |
| InfluxDB2 | No  | Yes | influxdb2                                      | influxdb2    |
| CSV | Yes  | Yes | csv                                      | csv    |
| Socket | Yes  | No | socket                                      | socket    |
| File Database | Yes  | Yes | filedb                                      | filedb    |
| Prometheus | No  | Yes | prometheus                                      | prometheus    |

## MongoDB

If you want to use a Mongo Database in your Formula, you have to specify
`mongodb` as the `type` of a puller (Source) or a pusher (Destination).

### Parameters

The list of accepted parameters are:

| Parameter     | Type   | CLI shortcut  | Default Value | Mandatory                                        |                                             Description                             |
| ------------- | -----  | ------------- | ------------- | ----------                                              | ------------------------------------    |
|`uri`          | string | `u` (`U` for `HWPCSensor`)           | N/A | Yes                                                       | The IP address of your MongoDB instance |
|`db` (`database` for `HWPCSensor`)           | string | `d` (`D` for `HWPCSensor`)            | N/A | Yes                                                       | The name of your database               |
|`collection`   | string | `c` (`C` for `HWPCSensor`)          | N/A | Yes                                                       | The name of the collection inside `db`  |
|`name`         | string | `n`           | `"puller_mongodb"` (Source), `pusher_mongodb` (Destination)| No | The related puller/pusher name. This parameter is not used by `HWPCSensor`                 |
|`model`        | string | `m`           | `"HWPCReport"` (Source), `PowerReport` (Destination) | No         | The Report type stored by the database  |

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

## Influx DB 2

If you want to use InfluxDB 2 in your Formula as Destination, you have to specify
`influxedb2` as the `type` of a pusher.

### Parameters

The list of accepted parameters are:

| Parameter     | Type   | CLI shortcut  | Default Value | Mandatory | Description                             |
| ------------- | -----  | ------------- | ------------- | ---------- | ------------------------------------    |
|`uri`          | string | `u`           | N/A           | Yes | The IP address of your Influxdb instance. It can contain the port number|
|`db`           | string | `d`           | N/A           | Yes | The name of your bucket (database)      |
|`port`         | int    | `p`           | None           | N/A| The port of communication. It is not mandatory if it is indicated in the `uri`               |
|`token`        | string | `k`           | N/A           | Yes | The token for accessing the database. The token owner must have write/read permissions on the bucket               |
|`org`          | string | `g`           | N/A           | Yes | The name of the organization associated to the bucket               |
|`tags`         | string | `t`           | N/A           | No | List of metadata keys of the report separated by `,` that will be kept. `sensor` and `target` are always kept as report metadata                           |
|`name`         | string | `n`           | `"pusher_influxdb2"` | No                                    | The related pusher name                 |
|`model`        | string | `m`           | `"PowerReport"`  | No | The Report type stored by the database  |


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

The list of accepted parameters are:

| Parameter     | Type    | CLI shortcut  | Default Value | Mandatory | Description                                                                   |
| ------------- | -----   | ------------- | ------------- | ----------| ------------------------------------                                          |
|`files`(Source)| string  | `f`           | Empty list           | No | The list of input CSV files with the format file1,file2,file3...              |
|`directory` (Destination and `HWPCSensor`)| string         |`d` (`U` for `HWPCSensor`)          | Current directory           | No |The directory where output CSV files will be written          |
|`name`         | string | `n`           | `"puller_csv"` (Source), `"pusher_csv"` (Destination)| No | The related puller/pusher name. This parameter is not used by `HWPCSensor`                 |
|`model`        | string | `m`           | `"HWPCReport"` (Source), `"PowerReport"` (Destination)   | No | The Report type stored in CSV files. This parameter is not used by `HWPCSensor`     |

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

The list of accepted parameters are:

| Parameter     | Type   | CLI shortcut  | Default Value| Mandatory                                       | Description                             |
| ------------- | -----  | ------------- | -------------| ----------                                      | ------------------------------------    |
|`port`         | int    | `p`           | N/A | Yes                                               | The port of communication               |
|`name`         | string | `n`           | `"puller_socket"`| No | The related puller name  |
|`model`        | string | `m`           | `"HWPCReport"` | No | The Report type managed by the socket |


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

The list of accepted parameters are:

| Parameter     | Type   | CLI shortcut  | Default Value| Mandatory                                      | Description                             |
| ------------- | -----  | ------------- | -------------| ----------                                        | ------------------------------------    |
|`filename`     | int    | `f`           | N/A                                                | Yes | The name of the file                    |
|`name`         | string | `n`           | `"pusher_filedb"` | No | The related pusher name |
|`model`        | string | `m`           | `"HWPCReport"` (Source) `"PowerReport"` (Destination)| No  | The Report type stored in the file      |

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
`prometheus` as the `type` of a pusher in your formula configuration file.

### Parameters

The list of accepted parameters are:

| Parameter     | Type   | CLI shortcut  | Default Value | Mandatory                                      | Description                             |
| ------------- | -----  | ------------- | ------------- | ----------                                    | ------------------------------------    |
|`uri`          | string | `u`           | `127.0.0.1` | No                                               | The IP address of your Prometheus instance |
|`port`         | int | `p`              | N/A | Yes                                              | The port of communication                  |
|`tags`         | string | `t`           | N/A | No                                              | List of metadata keys of the report separated by `,` that will be kept. `sensor` and `target` are always kept as report metadata                    |
|`metric_name`  | string | `M`           | N/A | Yes                                              | The exposed metric name                    |
|`metric_description`  | string | `d`    | `"energy consumption"` | No                             | The exposed metric description                    |
|`name`         | string | `n`           | `"pusher_prom"` | No | The related pusher name                 |
|`model`        | string | `m`           | `"PowerReport"` | No | The Report type exposed by Prometheus       |


Prometheus can only be used as a Destination that monitors reports but they will be not stored by this service.
The tags names are metadata keys of reports to be used as labels. If a report doesn't have a provide tag, it will be ignored by the Destination.    

### JSON File Excerpt

Below you find an example of configuration excerpt for this kind of Destination.

```json
{
  "type": "prometheus",
  "uri": "127.0.0.1",
  "port": 8080,
  "metric_name": test
}
```
