# Reports

PowerAPI toolkit is modular, which means any sensor can be plugged to any monitoring
tool as long as the needed information is provided.
We fixed the way of encoding the information. Those encoding are called reports.

A report specify the `json` fields that has to be provided to pass information of
a certain kind.

The type of reports required by each formula are specified in their user guide. However, all report have a common basis:

- `timestamp` : at the format "year-month-dayThour:minutes:secondes". The
  timestamp should reflect the time at which the information correspond, not the
  time the information was computed.
  For example if a power consumption of a CPU is mesured at time `t` and used to
  determine the power comsumption of a cgroup in a `PowerReport`, this report
  should have timestamp `t`.

- `target` : The target should be the subject of the mesure. For example if
    you produce a report that contain information relative to a program, domain,
    etc. The target should refer to it.

- `sensor`: It's a name field that should be use to regroup reports for
  computing modules. For example, in VirtualWatts, the computationnal module need to receive a
  `ProcfsReport` and a `PowerReport`, for both reports to be send to the same
  computational module they have to have the same `sensor`.

  A report have the following format:

  ```json
  "timestamp":$timestamp,
  "target":$target,
  "sensor":$sensor,
  $report_specific_fields

  ```
In the following parts we specify the `$report_specific_fields` for each type of report.

## HWPC Report

A `HWPCReport` is used to report perfomance counters and RAPL.
Its specific fields are the following:

- `groups`: A list of subreport that can be of three kind, `rapl`, `core` and
  `msr`.

  Each group is represented in the same wa:

  ```json
  {
    $type: {
      $core_number : {
        $socket_number : {
          List of counter and their value
        }
      }
    }
  }
  ```

Below you can find an example of `HWPCReport`:

```json
{
  "timestamp": "2023-01-13T09:51:22.630",
  "sensor": "sensor_test",
  "target": "influxdb",
  "groups": {
    "core": {
      "0": {
        "0": {
          "CPU_CLK_THREAD_UNHALTED:THREAD_P": 75510,
          "CPU_CLK_THREAD_UNHALTED:REF_P": 2271,
          "time_enabled": 167403,
          "time_running": 167403,
          "LLC_MISSES": 1077,
          "INSTRUCTIONS_RETIRED": 31693
        },
        "1": {
          "CPU_CLK_THREAD_UNHALTED:THREAD_P": 43801,
          "CPU_CLK_THREAD_UNHALTED:REF_P": 1318,
          "time_enabled": 99324,
          "time_running": 99324,
          "LLC_MISSES": 750,
          "INSTRUCTIONS_RETIRED": 15011
        }
      }
    }
  }
}
{
  "timestamp" : "2023-01-13T09:51:22.630",
  "sensor" : "sensor_test",
  "target" : "all",
  "groups" : {
    "rapl" : {
      "0" : {
        "1" : {
			      "RAPL_ENERGY_PKG" : 5709496320,
			      "time_enabled" : 1006717449,
			      "time_running" : 1006717449
          }
      }
    },
    "msr" : {
      "0" : {
        "0" : {
          "MPERF" : 29646849,
	        "APERF" : 12319312,
	        "TSC" : 2122153094,
	        "time_enabled" : 1006580601,
	        "time_running" : 1006580601
        },
        "1" : {
          "MPERF" : 20587012,
          "APERF" : 19838920,
          "TSC" : 2122185970,
	        "time_enabled" : 1006560540,
	        "time_running" : 1006560540
        }
      }
    }
  }
}

```

## Power Report

A `PowerReport` is used to transfer information about power consumption estimations.
Its specific fields are the following:

- `power`: A power value in Watts.

Below you find an exemple of `PowerReport`:

```json
{
  "timestamp": "2023-01-14T12:37:37.168817",
  "sensor": "formula_group",
  "target": "all",
  "power": 42
}
```

<!-- ## Procfs Report

A `ProcfsReport` is used to transfer information about CPU usage of
process.
Its specific fields are the following:

- `global_cpu_usage` : The used percentage of the CPU.
- `usage`: A list of the monitored processes with their percentage of CPU usage.

Below you find an exemple of `ProcfsReport`:

```json
{
  "timestamp": "2023-01-14T12:37:37.168817",
  "sensor": "formula_group",
  "target": ["firefox_cgroup", "emacs_cgroup", "zsh_cgroup", "mongo_cgroup"],
  "usage": {
    "firefox_cgroup": 8.36,
    "emacs_cgroup": 5.52,
    "zsh_cgroup": 0.01,
    "mongo_cgroup": 0.64
  },
  "global_cpu_usage": 27.610000000000014
}
-->
