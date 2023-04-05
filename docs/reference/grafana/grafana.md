# Visualizing Power Consumptions on Grafana

Here it is explained how to visualize the power estimation computed by a Formula on a Grafana dashboard to obtain this kind of visualisation:

<img
src="https://raw.githubusercontent.com/powerapi-ng/powerapi-ng.github.io/master/images/viz_by_process.png"
alt="datasource_section" width="1000px">

This screenshot shows the visualisation of power consumption of a Web browser and tools used for monitoring (Source, Destination, Sensor, Formula)

In this tutorial, we describe how to connect a Formula to a Grafana instance by using InfluxDB as Destination.
Then, we will see how to configure Grafana to visualize the power estimation computed by the Formula.

This tutorial assumes that you know how launch a Formula and a Sensor to compute power estimation and that you have an InfluxDB and a Grafana instance running on your local machine.
The InfluxDB instance listen on port `1234` and Grafana instance listen on port `4321`.

## Connect Grafana to the InfluxDB instance

Connect to your Grafana instance and go to the "Data sources" section (in the configuration part of the side bar).

<img
src="https://raw.githubusercontent.com/powerapi-ng/powerapi-ng.github.io/master/images/grafana_home.png"
alt="datasource_section" width="300px">

Click on the `"Add data source"` button and select `"InfluxDB"`.

Enter a data source name (here we choose "InfluxDB-1"), the instance URI (`http://localhost:4321`) and the Destination name you use in the file `config_formula.json` then click on the `"Save and test"` button.

<img
src="https://raw.githubusercontent.com/powerapi-ng/powerapi-ng.github.io/master/images/add_db.png"
alt="datasource_section" width="400px">

## Visualize the power consumption on a dashboard in real-time

Go to the `"Create Dashboard"` section on the side bar to create a new dashboard.

<img
src="https://raw.githubusercontent.com/powerapi-ng/powerapi-ng.github.io/master/images/add_dashboard.png"
alt="datasource_section" width="300px">

Click on the `"add Query"` button and write the following query on the `Query` field to request the power estimations from the InfluxDB measurement:

```sql
SELECT power FROM "power_consumption" GROUP BY target
```

Then write `$tag_target` on the `ALIAS BY` field to label each graph with the target name

<img
src="https://raw.githubusercontent.com/powerapi-ng/powerapi-ng.github.io/master/images/add_query_by_process.png"
alt="datasource_section" width="600px">

To display the power consumption in real time, you can update the range of the visualisation to `last 5 minutes` and the `refresh dashboard` parameter to `5s`. This parameter are on the top-right corner of the UI.

<img
src="https://raw.githubusercontent.com/powerapi-ng/powerapi-ng.github.io/master/images/refresh.png"
alt="datasource_section" width="600px">
