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

### Sensor Connection

A formula is connected to a sensor via a database (e.g MongoDB). The sensor writes
the collected data to the database and the formula reads this data from the
database.

There are two connection modes:

- "Stream" mode where data is read from the database while the sensor is collecting it

- "Post-mortem" mode which analyses the data already collected by the sensor in a
  past monitoring phase.
