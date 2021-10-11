# Influx DB

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
