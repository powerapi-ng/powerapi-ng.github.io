---
title: "PowerAPI - How it works ?"
keywords: howitworks
sidebar: home_sidebar
permalink: powerapi_howitworks.html
summary: "This page presents how you can build a power meter with the tools provided by
PowerAPI. We present the different components of a power meter and how you can
connect them to build a workflow for your own needs."
---


## Power meter Architecture

A power meter is a set of two components, a sensor and a formula, used to
produce an estimation of the power consumption of a monitored software.

The sensor collects raw data correlated with the power consumption of the
software. The formula is a model that use the collected data to compute the
power consumption. Both of them are connected by a database that is used to
transfer data from the sensor to the formula.

The two next sub-sections present how a sensor and a formula
work and how they should be used.

![arch](images/powerAPI_archi.png)

## Sensor

A sensor is an independent software that collects raw data correlated with the
power consumption of monitored software.

Data are collected by querying the hardware's machine that hosts the monitored
software. The sensor must be executed on the same machine as the monitored
software. The data are collected throughout the duration of the software. For this reason,
the sensor must operate in parallel.

Collected data are stored in an external database to make the data available to
the formula. This database may be hosted on an other machine.

### Usage

Because they collect from different hardware, each sensor are very different
from one another. Refer to each sensor documentation to know how to use them.

## Formula

A formula is an independent software that use model to compute the power consumption of
monitored software from the data collected by the sensor.

We implement each formula with a common Command Line Interface (CLI) to connect
it to a sensor and to configure its output. In this section, we present how the
connection between the sensor and the formula works. We also present the common
formula's CLI.

### Sensor Connection

A formula is connected to a sensor via a database (e.g MongoDB). The sensor writes
the collected data to the database and the formula reads this data from the
database.

There are two connection modes:

- "Stream" mode where data is read from the database while the sensor is collecting it

- "Post-mortem" mode which analyses the data already collected by the sensor in a
  past monitoring phase.

The default mode of a formula is the "Post-mortem" mode, use the command line
argument `-s` to enable the "Stream" mode.

### Command line interface

The presented CLI is common to all formulas of the PowerAPI toolkit.
Replace `FORMULA_NAME` with the name of the used formula in the
following commands.

#### Install and Launch the formula

All formulas are available on pypi and docker-hub.

You can directly launch a docker container containing the formula with the following
command:

	docker run powerapi/FORMULA_NAME args ...

To use the formula without docker, you can install it with `pip`:

	pip3 install FORMULA_NAME

Then run it with python(>=3.7):

	python3 -m FORMULA_NAME args ...

#### Command line interface

Every formula have a common command line interface (CLI) with the same
parameters. This interface help you to configure the formula (eg: specify its
input and outputs). This section present you this common parameters that you can
use with every formula.

Some formula may use specific parameters. These parameters are described on their
formula documentation. Just place them after the common CLI arguments.

The following example show you how to use the formula parameters :


	(python3 -m/docker run) FORMULA_NAME -v -s --input input_database_type ... --output output_database_type1 ... --output output_database_type2 ... --formula_specific_parameter1 ... --formula_specific_parameterN


The `--input` parameters specify information about the database used to store data
collected by the hwpc-sensor. The first argument after `--input` is the type of the
database. Other parameters could be added to specify information about the
database. Theses parameters depends of the database type and are described below.

The `--output` parameter specify information about the database used to store the
power consumption computed by the formula. As `--input` parameter, it take the
database type as first argument and other parameters depending of the database
type.


##### Optional parameters

List of the optional parameters used to enable specific modes:

- `-s` or `--stream` : connect to the database with "stream mode"
- `-v` or `--verbose`: verbose mode (for debug)

#### Database parameters

This section describe specific parameters of each database with example to use them

##### MongoDB

To use a MongoDB database as an input or output, use the database type `mongodb`
with the following parameters :

- `-u` or `--uri` to specify the location of the database
- `-d` or `--db` to specify the database name to read/store the data
- `-c` or `--collection` to collection name to read/store the data

For example, to use a mongodb database, as an output of a formula, located at
`1.2.3.4:3245` with a database `test_db` and a collection `test_col` launch the
formula with the following parameter :
	
	--output mongodb --uri 1.2.3.4:3245 --db test_db --collection test_col


##### CSV

You can use csv files as an input or output of a formula. 

Sensors could produce csv files that could be used as input. Use the database type `csv` with
the following parameter :

- `-f` or `--files` to specify location of the sensors output files. You can
  specify multiple files with the following syntax :
  `--files=file1,file2,...,fileN`

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
	
##### InfluxDB

To use an InfluxDB database only as an output of a formula, use the database type `influxdb` with the following parameters : 

- `-u` or `--uri` to specify the location of the database
- `-p` or `--port` to specify the database connection port
- `-d` or `--db` to specify the database name to read/store the data

For example, to use an InfluxDB database, as an output of a formula, located at `1.2.3.4:3245` with a database `test_db` launch the formula with the following parameter : 
	
	--output influxdb --uri 1.2.3.4 --port 3245 --db test_db
