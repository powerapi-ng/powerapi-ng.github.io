---
title: "PowerAPI - How it work"
keywords: howitwork 
sidebar: home_sidebar 
permalink: powerapi_howitworks.html
summary: "This page present how you can build a power meter with the tools provided by
PowerAPI. We present the different components of a power meter and how you can
connect them to build it for your own needs."
---



Power meter Architecture
==============================

A power meter is an assembly of two components, a sensor and a formula. Used to
produce an estimation of the power consumption of a monitored software.

The sensor collect raw data correlated with the power consumption of the
software and the formula is a model that use the collected data to compute the
power consumption. Both of them are connected by a database that is used to
transfer data from the sensor to the formula.

The two next sub-sections present how a sensor and a formula
work and how they should be used.

![arch](images/powerAPI_archi.png)

Sensor
========

A sensor is an independent software that collect raw data correlated with the
power consumption of monitored software.

Data are collected by querying the hardware's machine that host the monitored
software. So the sensor must be run on the same machine than the monitored
software.

The data are collected during all the software execution period. Thus, the
sensor must be run during all the software execution period.

Collected data are stored in an external database to make the data available to
the formula. This database may be hosted on an other machine.

Usage
------

Because they collect from different hardware, each sensor are very different
from one another. Refer to each sensor documentation to know how to use them.

Formula
=========

A formula is an independent software that use model to compute the power consumption of
monitored software from the data collected by the sensor.

We implements each formula with a common command line interface(CLI) to connect
it to a sensor and to configure its output. We present in this section how the
connection between the sensor and the formula works. We also present the common
formula's CLI.

Sensor Connection
------------------

A formula is connected to a sensor via a MongoDB database. The sensor write
the collected data on the database and the formula read this data on this
database.

There are two connection mode :

- a "stream" mode where data are read from the database as the sensor collect
  them;

- a "post-mortem" mode that analyse data already collected by the sensor in a
  past monitoring phase.

The default mode of a formula is the "post-mortem" mode, use the command line
argument `-s` to enable the "stream mode"

Command line interface
-----------------------

The presented command line interface is common to all formulas of the PowerAPI
toolkit. Just replace `FORMULA_NAME` with the name of the used formula in the
following commands.

### Install and Launch the formula

Every formula are available on pypi and docker-hub.

You can directly run a docker containing the formula with the following
command : 

	docker run powerapi/FORMULA_NAME args ...

To use the formula without docker, you can install it with `pip` :

	pip3 install FORMULA_NAME 

and run it with python(>=3.7) : 

	python3 -m FORMULA_NAME args ...

### Command line arguments

You can run every formula with this common arguments, extra arguments could be
added at the end of the command line : 

	(python3 -m/docker run) FORMULA_NAME input_mongo_uri input_db input_collection output_mongo_uri output_db output_collection

with : 

- `input_mongo_uri` : uri to the mongoDB used by the hwpc-sensor to store its
  output data. Use the following format `mongodb://MONGO_ADDRESS`
- `input_db` : database used by the hwpc-sensor to store its output data
- `input_collection` : collection used by the hwpc-sensor to store its output data
- `output_mongo_uri` : uri to the mongoDB used to store the power consumption data. Use the following format `mongodb://MONGO_ADDRESS`
- `output_db` : database used to store the power consumption data
- `output_collection` : collection used to store the power consumption data

### Optional arguments

List of the optional arguments used to enable some special mode : 

- `-s` : connect to the database with "stream mode"
- `-v` : verbose mode (for debug)

### Formula specific arguments

Some formula may use specific arguments. These arguments are described on their
formula documentation. Just place them after the common CLI arguments
