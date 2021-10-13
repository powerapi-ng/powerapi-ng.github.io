# Jouleit

Jouleit is a script that can be used to monitor energy consumption for any program.

Jouleit uses the Intel "Running Average Power Limit" (RAPL) technology that
estimates power consumption of the CPU, ram and integrated GPU. This technology
is available on Intel CPU since the Sandy Bridge generation(2010).

## Installation

Jouleit need `gawk` to run.
You can get the script from the [github repository](https://github.com/powerapi-ng/jouleit)
Start jouleit by using `./jouleit.sh cmd`.

## Flags and options

| **Flag**        | **Description**                                                                                                                                                         |     **Default value**     |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-----------------------: |
| -a              | print the details of all sockets instead of the aggregation                                                                                                             |           False           |
| -b              | print the results in the format of \*KEY1;VALUE1;KEY2;VALUE2..                                                                                                          |           False           |
| -l              | list all the available domaines ( CPU, DRAM ..etc ) and print them in the form of a header of csv                                                                       |                           |
| -c              | Print only the values in csv format ( value1;value2;value3), We recommend using this after running the **jouleit** with -l Flag to see the order of the measured values |           false           |
| -s **#N**       | measure only the energy of the socket **#N**                                                                                                                            | all the available sockets |
| -o **filename** | redirect the output and the log of the executed program in the file `filename                                                                                           |     current terminal      |
| -n **N**        | Run the programm **N** times and record the measured values in `data1234.csv` file                                                                                      |                           |
