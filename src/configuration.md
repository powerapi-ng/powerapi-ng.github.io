# Configuration File

PowerAPI can read configuration through config file or through the CLI.
Here we are using config file because they are more readable.

PowerAPI can be configured with the following parameters :

- `verbose` (bool) : verbose or quiet mode.
- `stream` (bool) : to specify if the reports are provided one by one or are
  stored in a database.
- `sensor-report-sampling-interval` (int): If in stream mode, the time in
  milliseconds between two reports.
- `input` (database) : The database used in input. The way to write their
  configuration is specified [here](./database.md). Multiple database can be
  used as inputs.
- `output` (database) : The database used in output. The way to write their
  configuration is specified [here](./database.md). Multiple database can be
  used as outputs.

All configuration files of PowerAPI based formula follow the next template:

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
    ... #(Multiple puller can be used)
  },
  "output": {
    $pusher_name: {
      "type": $type_of_database
      $database_parameters
    }
    ... #(Multiple pusher can be used)

  },
  $formula_parameters
}
```
