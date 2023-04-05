# Formula Configuration

PowerAPI can read configurations through the CLI or through configuration files.

# CLI Parameters

The table below shows basic parameters.

| Parameter    | Type                  | CLI shortcut  | Default Value                        | Description                          |
| ------------ | -----                 | ------------- | -------------                        | ------------------------------------ |
| `verbose`                            | `bool` (flag)               | `v`           |`NOTSET`                              | Verbose or quiet mode                |
| `stream`                             | `bool` (flag)  | `s`           |`False`                               | Realtime or post-mortem mode         |
| `sensor-report-sampling-interval`    | `int`         | N/A           | `1000`                                 | The time in milliseconds between two reports (`stream` = `True`) |
| `input`     | `string` (Source)      | N/A | N/A     | The Source used as input. More information about Sources and their related parameters can be found [here](../database/sources_destinations.md)|
| `output`     | `string` (Destination)| N/A | N/A            | The Destination used as output. More information about Destinations and their related parameters can be found [here](../database/sources_destinations.md)|

???+ tip "Sources and Destinations' values"
    - Sources: `mongodb`, `csv`, `socket`, `filedb`
    - Destinations: `mongodb`, `influxedb`, `influxedb2`, `csv`, `socket`, `filedb`, `prom`

## Configuration File

PowerAPI Formulas use `json` files. These files follow the next template:

```json
{
  "verbose": $bool,
  "stream": $bool ,
  "sensor-report-sampling-interval" : $int,
  "input": {
    $puller_name: {
      "model": $type_of_report,
      "type": $type_of_database,
      $database_parameters
    }
    ... #(Multiple pullers can be used)
  },
  "output": {
    $pusher_name: {
      "type": $type_of_database
      $database_parameters
    }
    ... #(Multiple pushers can be used)

  },
  $formula_parameters
}
```
???+ info "Sources and Destinations' `json` tags"
    More information related to `json` tags for each Source/Destination can be found [here](../database/sources_destinations.md)
