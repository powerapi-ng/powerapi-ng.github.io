# CSV

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
