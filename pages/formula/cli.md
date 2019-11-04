---
title: "Formula command line interface"
keywords: cli
sidebar: home_sidebar
permalink: formula_cli.html
---

Every formula have a common command line interface (CLI) with the same
parameters. This interface help you to configure the formula (eg: specify its
inputs and outputs). This section present you these common parameters that you can
use with every formulas.

Some formulas may use specific parameters. These parameters are described on their
formula documentation. Just place them after the common CLI arguments.

The following example show you how to use the formula parameters :

	(python3 -m/docker run) FORMULA_NAME -v -s --input input_database_type ... --output output_database_type1 ... --output output_database_type2 ... --formula_specific_parameter1 ... --formula_specific_parameterN
	
(The presented CLI is common to all formulas of the PowerAPI toolkit.
Replace `FORMULA_NAME` with the name of the used formula in the
following commands)

The `--input` parameters specify information about the database used to store data
collected by sensors. The first argument after `--input` is the type of the
database. Other parameters could be added to specify information about the
database. Theses parameters depends on the database type and are described below.

The `--output` parameter specify information about the database used to store the
power consumption computed by the formula. As `--input` parameter, it take the
database type as first argument and other parameters depending on the database
type.


## Optional parameters

List of the optional parameters used to enable specific modes

- `-s` or `--stream` : connect to the database with "stream mode" (see [here](/powerapi_howitworks.html#sensor-connection))
- `-v` or `--verbose`: verbose mode (for debug)

## Database parameters

This section describe specific parameters of each database with example to use them

### MongoDB

To use a MongoDB database as an input or output, use the database type `mongodb`
with the following parameters :

- `-u` or `--uri` to specify the location of the database
- `-d` or `--db` to specify the database name to read/store the data
- `-c` or `--collection` to collection name to read/store the data
- `-n` or `--name` When you have more than one input or output, you have to
  specify the name of each of them with the `name` parameter. This argument is
  optional if you have only one input/output
- `-m` or `--model` to specify the data type that will be stored (see [Data Type](/formula_cli.html#data-type))

For example, to use a mongodb database, as an output of a formula, located at
`1.2.3.4:3245` with a database `test_db` and a collection `test_col` launch the
formula with the following parameter :
	
	--output mongodb --uri 1.2.3.4:3245 --db test_db --collection test_col

### CSV

You can use csv files as an input or output of a formula.

Sensors could produce csv files that could be used as input. Use the database type `csv` with
the following parameter :

- `-f` or `--files` to specify location of the sensors output files. You can
  specify multiple files with the following syntax :
  `--files=file1,file2,...,fileN`
- `-n` or `--name` When you have more than one input or output, you have to
  specify the name of each of them with the `name` parameter. This argument is
  optional if you have only one input/output
- `-m` or `--model` to specify the data type that will be stored (see [Data Type](/formula_cli.html#data-type))


For example, to use three files as formula input (`file1`, `file2` and `file3`)
launch the formula with the following parameters :
	
	--input csv --files=file1,file2,file3


To use a csv file as an output, you can specify a folder where the formula will
write the csv file containing the computed power consumption data. Use the
database type `csv` with the following parameters :

- `-d` or `--directory` to specify the directory where the output csv will be
  written. One csv file will be stored in a sub-folder named with the sensor name. The
  csv file is named `power_consumption.csv`
	
For example, to store the power consumption data on a csv file on the
`/var/log/power` folder, launch the formula with the following parameters :
	
	--output csv --d /var/log/power
	
### InfluxDB

To use an InfluxDB database only as an output of a formula, use the database type `influxdb` with the following parameters : 

- `-u` or `--uri` to specify the location of the database
- `-p` or `--port` to specify the database connection port
- `-d` or `--db` to specify the database name to read/store the data
- `-n` or `--name` When you have more than one input or output, you have to
  specify the name of each of them with the `name` parameter. This argument is
  optional if you have only one input/output
- `-m` or `--model` to specify the data type that will be stored (see [Data Type](/formula_cli.html#data-type))


For example, to use an InfluxDB database, as an output of a formula, located at `1.2.3.4:3245` with a database `test_db` launch the formula with the following parameter : 
	
	--output influxdb --uri 1.2.3.4 --port 3245 --db test_db
	
	
### OpenTSDB

To use an OpenTSDB database only as an output of a formula, use the database type `opentsdb` with the following parameters : 

- `-u` or `--uri` to specify the location of the database
- `-p` or `--port` to specify the database connection port
- `--metric_name` to specify the metric name
- `-n` or `--name` When you have more than one input or output, you have to
  specify the name of each of them with the `name` parameter. This argument is
  optional if you have only one input/output
- `-m` or `--model` to specify the data type that will be stored (see [Data Type](/formula_cli.html#data-type))


For example, to use an OpenTSDB database, as an output of a formula, located at `1.2.3.4:3245` with a metric name called `test_metric` launch the formula with the following parameter : 
	
	--output opentsdb --uri 1.2.3.4 --port 3245 --metric_name test_metric

## Data type

To use a database as input or output of a formula, you have to specify the data type that it will store.

Input data type : 

- HWPC report (default input type) : specified with the parameter `--model
  HWPCReport`. Type of data retured by the [hwpc-sensor](hwpc.html)
  
Output data type :

- power report (default output type) : specified with parameter `--model
  PowerReport`. Data that contain a power consumption estimation.
  
- formula report : specified with parameter `--model FormulaReport`. Data that
  contain information about formula execution.
