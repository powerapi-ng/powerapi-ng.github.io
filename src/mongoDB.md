# MongoDB

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
