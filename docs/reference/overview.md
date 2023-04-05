# PowerAPI Overview

The goal of this project is to provide a set of tools to go forward a greener
computing.
The idea is to provide software-defined PowerMeters to mesure the power
consumption of programs.
The core of this project is the [PowerAPI](https://github.com/powerapi-ng/powerapi) toolkit for building
such PowerMeters.



## Software PowerMeters

A software PowerMeter is an application built with the PowerAPI components that can
measure the power consumption of software running on a single machine or on a
cluster of machine.

The Figure below depicts the global architecture of a software PowerMeter in PowerAPI.

![PowerAPI Architecture Overview](../../assets/images/reference/overview/global-architecture.jpg){ width="1000px"}


<!--img
src="assets/images/intro/global-architecture.png"
alt="PowerMeter Architecture" width="1000px"-->

A PowerMeter has two components, a Sensor and a Formula, used to
produce an estimation of the power consumption of a monitored software.

## Sensor

The Sensor is an independent software that collects raw data (metrics) correlated with the power consumption of the
monitored software.

Data are collected by querying the hardware’s machine that hosts the monitored
software. The sensor must be executed on the same machine as the monitored
software. The data are collected throughout the duration of the software. For
this reason, the sensor must operate in parallel.

Collected raw data are stored in an external Source to make the data available to
the Formula. This Source may be hosted on an other machine.

### Usage

Currently, PowerAPI proposes one Sensor: [HWPC](sensors/hwpc-sensor.md).
Refer to the Sensor documentation to know how to use it.

## Formula

A Formula is a computational module that computes an estimation of the power
consumption of monitored software from the data collected by the sensor.

A Formula has two working modes:

- `stream` mode where the Formula read the data from the Sensor as they are
  produced (in realtime).

- `post-mortem` mode where the Formula analyses the data already collected by the Sensor in a past monitoring phase.

### Usage

Currently, there are two Formulas: [RAPL](formulas/rapl.md) and [SmartWatts](formulas/smartwatts.md).
Refer to each Formula documentation to know how to use them.
