# Visualizing Power Consumptions on Grafana

Here it is explained how to visualize the power estimation computed by a Formula on a Grafana dashboard to obtain this kind of visualisation:

<img
src="https://powerapi.org/assets/images/reference/grafana/viz_by_process.png"
alt="viz_by_process" width="1000px">

This screenshot shows the visualisation of power consumption of a Web browser and tools used for monitoring (Source, Destination, Sensor, Formula)

In this tutorial, we describe how to connect a Formula to a Grafana instance by using InfluxDB 2.X as Destination.
Then, we will see how to configure Grafana to visualize the power estimation computed by the Formula.

This tutorial assumes that you know how launch a Formula and a Sensor to compute power estimation and that you have an InfluxDB 2.X and a Grafana instances running on your local machine.
The InfluxDB 2.X instance listen on port `8086`.

## Setup Grafana

```sh
docker run -d -p 3000:3000 grafana/grafana
```

After the launch, Grafana will be available at http://localhost:3000. On the signin page, enter *admin* for username and password.

## Connect Grafana to the InfluxDB 2.X instance

Connect to your Grafana instance and go to the `"Data sources"`` section (in the configuration part of the side bar).

<img
src="https://powerapi.org/assets/images/reference/grafana/grafana_home.png"
alt="grafana_home" width="300px">

Click on the `"Add new data source"` button and select `"InfluxDB"`. Enter:   

1. A data source *Name* (here we choose "InfluxDB-2"),
2. A *Query Language*, i.e., `InfluxQL`
3. An instance *URL* (`http://localhost:8086`)
4. A *Custom HTTP Header* called `Authorization` with Value `Token <mytoken>`, where `<mytoken>` is the token provided by InfluxDB 2.X for your organization.
5. A *Database* name, (here we choose `power_consumption`) that is the `db` value of your destination defined in your formula configuration.

Then click on the `"Save & test"` button. *User* and *Password* are not required as we use a token for authentification.  


<img
src="https://powerapi.org/assets/images/reference/grafana/add_db.png"
alt="add_db" width="400px">

## Visualize the power consumption on a dashboard in real-time

Go to the `"Dashboard"` section on the side bar and select on `New > New dashboard`. Then click on `+ Add visualisation` Then select `influxdb-2` as data source.

<img
src="https://powerapi.org/assets/images/reference/grafana/add_dashboard.png"
alt="add_dashboard" width="1000px">

Click on the query edition button (the one with a pencil on it) and write the following query on the `Query` field to request the power estimations from the InfluxDB 2.X measurement:

```sql
SELECT power FROM "power_consumption" GROUP BY target
```

Then write `$tag_target` on the `ALIAS BY` field to label each graph with the target name

<img
src="https://powerapi.org/assets/images/reference/grafana/add_query_by_process.png"
alt="add_query_by_process" width="600px">

To display the power consumption in real time, you can update the range of the visualisation to `last 5 minutes` and the `refresh dashboard` parameter to `5s`. This parameter are on the top-right corner of the UI.

<img
src="https://powerapi.org/assets/images/reference/grafana/refresh.png"
alt="refresh" width="600px">
