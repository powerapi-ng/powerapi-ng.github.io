# File Database

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
