---
title: "Monitoring the global power consumption of nodes"
sidebar: home_sidebar 
permalink: monitor_global_power_consumption.html
---

## Introduction

In this tutorial, we will describe how to deploy a software-defined power meter to monitor the power consumption of a single node or a cluster of nodes.

This tutorial will redirect you to specific instructions that explain how to deploy each component of the power meter (_i.e._, the sensor and the formula).

## Prerequisites
This tutorial assumes that you already deployed a MongoDB instance that is remotely accessible from all nodes you want to monitor.

CPUs of monitored nodes must have an Intel Sandy Bridge architecture or higher.
The sensor should run on a Linux distribution that is not on a virtual environment.

## Monitoring a single node

To monitor the global power consumption of a single node, you can deploy all the power meter components on the same node as follows:

* **Step 1:** [Deploy a sensor and connect it to the mongoDB instance](/howto_deploy_hwpc_sensor.html),
* **Step 2:** [Deploy the RAPL formula to compute power estimations](/howto_deploy_rapl_formula.html),
* **Step 3:** [Visualize the power consumption of your node](howto_connect_to_grafana.html).


## Monitor a Cluster of two nodes

To monitor the global power consumption of a cluster, you need to follow almost the same step as to monitor a single node:
* **Step 1:** [Deploy one sensor per monitored node and connect it to the mongoDB instance](/howto_deploy_hwpc_sensor.html). Label to each sensor (using the option `-n`) to track the power consumption per node;
* **Step 2:** [Start one RAPL formula to process the data collected by all the sensors](/howto_deploy_rapl_formula.html);
* **Step 3:** [Visualize the power consumption of your nodes](howto_connect_to_grafana.html)

When using the mongo client to access the power consumption data, you can use the metadata field `sensor` to match power consumption with monitored nodes.
