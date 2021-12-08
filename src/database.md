# Database

A database can be used as an input or an output of powerapi formula

For each database the parameters to specify are differents. For each database,
its parameters are specified in its section.

## MongoDB

If you want to use a mongo database in your formula your have to specify
`mongodb` as the `type` of a puller or a pusher.

The list of parameters you have to provide :

- `uri` : The ip address of your mongo database
- `db`: the name of your database
- `collection`: the name of the collection inside the database

The default `model` of `mongodb` is `HWPCReport` if used as an input and
`PowerReport` if used as an output.

We provide an example of configuration file.

```json
{
  "type": "mongodb",
  "uri": "mongodb://127.0.0.1",
  "db": "test",
  "collection": "prep"
}
```

## Influx DB

If you want to use an influxdb in your formula your have to specify
`influxedb` as the `type` of a puller or a pusher.

The list of parameters you have to provide :

- `uri` : IP address of the server with the database
- `port`: port of communication
- `db` : name of the database

InfluxDB can only be used as an output and its default `model` is `PowerReport`.

We provide an example of configuration file.

```json
{
  "tags": "socket",
  "model": "PowerReport",
  "type": "influxdb",
  "uri": "127.0.0.1",
  "port": "8086",
  "db": "test_influxdb"
}
```

## CSV

If you want to use a csv file in your formula your have to specify
`csv` as the `type` of a puller or a pusher.

The list of parameters you have to provide :

- `uri` : The csv file name

The default `model` of `csv` is `HWPCReport`.

The default `model` of `csv` is `HWPCReport` if used as an input and
`PowerReport` if used as an output.

We provide an example of configuration file.

```json
{
  "type": "csv",
  "uri": "/tmp/sensor_output/"
}
```

## Socket

If you want to use a tcp socket in your formula your have to specify
`socket` as the `type` of a puller or a pusher.
This database is made for stream mode.

The list of parameters you have to provide :

- `uri` : The IP address of the server
- `port`: The port to use to communicate with the server

The socket can only be used as an input and its default `model` is `HWPCReport`.

We provide an example of configuration file.

```json
{
  "type": "socket",
  "uri": "127.0.0.1",
  "port": 8080
}
```

## File Database

If you want to use a file as database in your formula your have to specify
`filedb` as the `type` of a puller or a pusher.
The database is made for stream mode. It should contain only the last
report.

The list of parameters you have to provide :

- `filename` : The name of the file

This database can only be used as an input and its default `model` is `PowerReport`.

We provide an example of configuration file.

```json
{
  "type": "socket",
  "filename": /tmp/database
}
```

## Prometheus

If you want to use a prometheus as database in your formula your have to specify
`prom` as the `type` of a pusher.

The list of parameters you have to provide :

- `tags` : specify report tags
- `uri` : Server ip address
- `port` : Server port
- `metric_name` : The metric name
- `metric_description` : The metric description. It default value is ` energy consumption`
  This database can only be used as an output.

We provide an example of configuration file.

```json
{
  "type": "prom",
  "uri": "127.0.0.1",
  "port": 8080,
  "metric_name": test
}
```
