# Reports

PowerAPI tools tend to be modular, any sensor could be plugged to any monitoring
tool as long as the needed information is provided.
We fixed the way of encoding the information. Those encoding are called reports.

A report specify the `json` fields that should be provided to pass information of
a certain kind.

The type of reports required by each formula are specified in their user guide.

All report have a common basis:

- `timestamp` : at the format "year-month-dayThour:minutes:secondes". The
  timestamp should reflect the time at which the information correspond, not the
  time the information was computed.
  For example if a power consumption of a CPU is mesured at time `t` and used to
  determine the power comsumption of a cgroup in a `PowerReport`, this report
  should have timestamp `t`.

  - `target` : The target should be the subject of the mesure. For example if
    you produce a report that contain information relative to a program,domain,
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
