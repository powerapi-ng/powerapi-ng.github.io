---
title: "Visualizing power consumptions from Grafana"
keywords: homepage
sidebar: home_sidebar 
permalink: howto_monitor_global/connect_to_grafana.html
---

## Introduction

This tutorial presents how to visualize the power estimation computed by a formula on a grafana dashboard to obtain this kind of visualisation: 

![datasource_section](/images/viz.gif)

We describe how to connect a formula to a grafana instance, using InfluxDB.
Then, we will see how to configure grafana to visualize the power estimation computed by the formula.

This tutorial assume that you know how launch a formula and a sensor to compute power estimation and that you have an InfluxDB and a grafana instance running on your local machine.
The InfluxDB instance listen on port `1234` and Grafana instance listen on port `4321`.



## Launch the formula with an InfluxDB Output

Deploy the formula you want with the following parameter to the command line: 

	--output influxdb --uri localhost --port 1234 --db power_consumption --name grafana_output

## Connect Grafana to the InfluxDB instance

Connect to your Grafana instance and go to the "Data sources" section (in the configuration part of the side bar).

![datasource_section](/images/grafana_home.png)

Click on the `"Add data source"` button and select `"InfluxDB"`.

Enter a data source name (here we choose "InfluxDB-1"), the instance URI (`http://localhost:4321`) and the database name (`power_consumption`) then click on the `"Save and test"` button.

![add_datasource](/images/add_db.png)


## Visualize the power consumption on a dashboard in real-time

Go to the `"Create Dashboard"` section on the side bar to create a new dashboard.

![add_dashboard](/images/add_dashboard.png)

Click on the `"add Query"` button and write the following query on the `Query` field to request the power estimations from the InfluxDB measurement: `SELECT power FROM "power_consumption"`

![add_query](/images/add_query.png)

To display the power consumption in real time, you can update the range of the visualisation to `last 5 minutes` and the `refresh dashboard` parameter to `5s`. This parameter are on the top-right corner of the UI.

![add_query](/images/refresh.png)
