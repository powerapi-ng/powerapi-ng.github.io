# Auto-config Script

This script detect the frequency of your cpu and use them to provide a
configuration file for Smartwatts.

```sh
#!/usr/bin/env bash

maxfrequency=$(lscpu -b -p=MAXMHZ | tail -n -1| cut -d , -f 1)
minfrequency=$(lscpu -b -p=MINMHZ | tail -n -1 | cut -d , -f 1)
basefrequency=$(lscpu | grep "Model name" | cut -d @ -f 2 | cut -d G -f 1)
basefrequency=$(expr ${basefrequency}\*1000 | bc | cut -d . -f 1)

echo "
{
  "verbose": true,
  "stream": true,
  "input": {
    "puller": {
      "model": "HWPCReport",
      "type": "socket",
      "uri": "127.0.0.1",
      "port": 8080,
      "collection": "test_hwpc"
    }
  },
  "output": {
    "pusher_power": {
      "type": "mongodb",
      "uri": "mongodb://127.0.0.1",
      "db": "test",
      "collection": "prep"
    }
  },
  "cpu-ratio-base": $basefrequency,
  "cpu-ratio-min": $minfrequency,
  "cpu-ratio-max": $maxfrequency,
  "cpu-error-threshold": 2.0,
  "disable-dram-formula": true,
  "sensor-report-sampling-interval": 1000
}
" > ./config_file.json

```
