---
title: "How to monitor process power consumption"
keywords: homepage
sidebar: home_sidebar 
permalink: howto_monitor_process/intro.html
---

## Introduction

In this tutorial, we will describe how to deploy a software-defined power meter to monitor the power consumption of process running on a single node or a cluster of nodes.

This tutorial will redirect you to specific instructions that explain how to deploy each component of the power meter (_i.e._, the sensor and the formula).

## Prerequisites
This tutorial assumes that you already deployed a MongoDB instance that is remotely accessible from all nodes you want to monitor.

CPUs of monitored nodes must have an Intel Sandy Bridge architecture or higher.
The sensor should run on a Linux distribution that is not on a virtual environment.
You have administrator privilege on the machine that host monitored processes

## Monitoring a single node

To monitor the power consumption of docker containers running on a single node, you can deploy all the power meter components on the same node as follows:

* **Step 1:** [Select process you want to monitor](/howto_monitor_process/monitored_process.html),
* **Step 2:** [Deploy a sensor and connect it to the mongoDB instance](/howto_monitor_process/deploy_sensor.html),
* **Step 3:** [Deploy the smartwatts formula to compute containers power consumption](/howto_monitor_process/deploy_formula.html),
* **Step 4:** [Visualize the power consumption of each docker container](/howto_monitor_process/connect_to_grafana.html).


## Monitoring a cluster

Coming soon ...
<!-- To monitor the global power consumption of a cluster, you need to follow almost the same step as to monitor a single node: -->
<!-- * **Step 1:** [Deploy one sensor per monitored node and connect it to the mongoDB instance](/howto_monitor_global/deploy_sensor.html). Label to each sensor (using the option `-n`) to track the power consumption per node; -->
<!-- * **Step 2:** [Start one RAPL formula to process the data collected by all the sensors](/howto_monitor_global/deploy_formula.html); -->
<!-- * **Step 3:** [Visualize the power consumption of your nodes](/howto_monitor_global/connect_to_grafana.html) -->

<!-- When using the mongo client to access the power consumption data, you can use the metadata field `sensor` to match power consumption with monitored nodes. -->
