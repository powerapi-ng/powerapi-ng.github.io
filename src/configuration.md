# Configuration File

For PowerAPI based formula there is a pattern of configuration file that will
always be present.

The configuration files are in json and have the following format :

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
