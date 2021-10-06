# Where to start ?

PowerAPI is a middleware toolkit for building software-defined power meters.
Software-defined power meters are configurable software libraries that can
estimate the power consumption of software in real-time. PowerAPI supports the
acquisition of raw metrics from a wide diversity of sensors (eg., physical
meters, processor interfaces, hardware counters, OS counters) and the delivery
of power consumptions via different channels (including file system, network,
web, graphical). As a middleware toolkit, PowerAPI offers the capability of
assembling power meters «à la carte» to accommodate user requirements.

PowerAPI is a framekork for building software-defined power meters.

There is two types of users :

- The one that want to monitor power consumption of their process
- The one that want to devellop their own formula

## Monitoring power consupmption

Some tools already exist :

- SmartWatts formula. It monitors the power consumption of processes on your
  device
  - RAPL formula. It monitors the power consumption of your device

The quickstart guides are available [here](./smartwatts_quickstart.md) and
[here](./rapl_quickstart.md).

## Develloping a formula

The [quickstart of powerapi](./powerapi_quickstart.md) is meant for it
