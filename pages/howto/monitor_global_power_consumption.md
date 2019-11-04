---
title: "Monitor global power consumption of one or more nodes"
sidebar: home_sidebar 
permalink: monitor_global_power_consumption.html
---

## Introduction

In this tutorial, we will see how to deploy a complete power meter to monitor
the power consumption of a single node or a cluster of node.

This tutorial will redirect you to other tutorials that explain how to deploy
each part of the power meter (the sensor and the formula).

## Prerequisites
This tutorial assumes that you have access to a mongoDB instance that is remotely
accessible from all nodes you want to monitor.

CPUs of Monitored nodes must have an intel Sandy Bridge architecture or higher.
The sensor must be run on a Linux operating system that is not on a virtual
environement.

## Monitor a single node

To monitor global power consumption of a single node, you can deploy all the
power meter components on the same node.

First of all, deploy a HWPC sensor and connect it to the mongoDB instance :
follow this [tutorial](/howto_deploy_hwpc_sensor.html)

Then, deploy a RAPL formula to compute power estimation with the data collected
by the sensor : follow this [tutorial](/howto_deploy_rapl_formula.html)

Power consumption estimation will be stored in a mongodb database. See the
RAPL-formula tutorial to learn how to retrieve it.

## Monitor a Cluster of two node

To monitor global power consumption of a cluster you need to follow the same
step as to monitor a single node.

You have to deploy one HWPC sensor on each monitored node and connect it to the
mongoDB instance. You have to give a name to each sensor (with the `-n`
parameter). The sensor name will be use by the formula to identify on which node
the power consumption information was collected : follow this
[tutorial](/howto_deploy_hwpc_sensor.html)

When your sensors are deployed, you can start a rapl-formula to process the data
collected by all the sensors. You only need one formula for all your
sensors. You can deploy the formula on another node or on a node that already
host a sensor. To know how to deploy a formula and retrieve power consumption
data with the mongo client : follow this
[tutorial](/howto_deploy_rapl_formula.html)

When using the mongo client to retrieve the power consumption data, you can use
the metadata field `sensor` to know the matching between data power consumption
and the monitored node.

## Visualisation

To visualize the power consumption of each node on a grafana dashboard follow
this [tutorial](howto_connect_to_grafana.html)
