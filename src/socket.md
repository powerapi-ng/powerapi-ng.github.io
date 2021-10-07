# Socket

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
