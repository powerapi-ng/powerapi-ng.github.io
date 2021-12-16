<img
src="https://rawgit.com/Spirals-Team/powerapi/master/resources/logo/PowerAPI-logo.png"
alt="Powerapi" width="1000px">

The goal of this projet is to provide a set of tools to go forward a greener
computing.
The idea is to provide software-defined power meters to mesure the power
consumption of program.
The core of this project is the [PowerAPI](./powerapi.md) toolkit for building
such power meters.

# Getting started

If you want to monitor the energy consumption of your process we have some
ready-to-use tools

- [RAPL formula](./rapl.md) for monitoring the energy consumption of your device.
- [SmartWatts formula](./smartwatts.md) for monitoring the energy consumption of
  your process.
- [Jouleit](./jouleit.md) for mesuring the energy consumption of a program.

<!-- If you want to develop your own power meter, we encourage you to read about [software-defined power -->
<!-- meters](powerapi_howitworks.md) before starting. -->

<!-- We provide a [quickstart](./powerapi_quickstart.md) project to develop a first -->
<!-- basic formula with powerAPI. -->
<!-- We also provide additional resources for developing your own formula afterward : -->

<!-- - A [User guide](./powerapi_user_guide.md). -->
<!-- - The [API](./powerapi_api.md). -->

# How it works

A power meter is an application build with the PowerAPI components that can
measure the power consumption of software running on a single machine or on a
cluster of machine.

This section present each PowerAPI component type and how connect them to build a power meter.

## Power meter Architecture

A power meter is a set of two components, a sensor and a formula, used to
produce an estimation of the power consumption of a monitored software.

The sensor collects raw data correlated with the power consumption of the
software. The formula is a computational module that use the collected data to
determine power consumption.
Both of them are connected by a database that is used to
transfer information.
The global architecture of a power meter is represented bellow.

<img
src="https://raw.githubusercontent.com/powerapi-ng/powerapi-ng.github.io/master/images/powerAPI_archi.png"
alt="Powerapi" width="1000px">

The two next sub-sections present how a sensor and a formula work and how they
should be used.

## Sensor

A sensor is an independent software that collects raw data correlated with the
power consumption of monitored software.

Data are collected by querying the hardware’s machine that hosts the monitored
software. The sensor must be executed on the same machine as the monitored
software. The data are collected throughout the duration of the software. For
this reason, the sensor must operate in parallel.

Collected data are stored in an external database to make the data available to
the formula. This database may be hosted on an other machine.

### Usage

Because they collect from different hardware, each sensor are very different
from one another. Refer to each sensor documentation to know how to use them.

## Formula

A formula is an independent software that compute an estimation of the power
consumption of monitored software from the data collected by the sensor.

### Sensor Connection

A formula communicate with the sensor via a database (e.g MongoDB). The sensor
writes the collected data to the database and the formula reads it afterward.

There are two connection modes:

- `stream` mode where the formula read the data from the sensor as they are
  produced.

- `post-mortem` mode which analyses the data already collected by the sensor in a past monitoring phase.

# Mailing list

You can follow the latest news and asks questions by subscribing to our <a href="mailto:sympa@inria.fr?subject=subscribe powerapi">mailing list</a>.

# Contributing

If you would like to contribute code you can do so through our [Github
repository](https://github.com/powerapi-ng/) by forking it and sending a
pull request.

You should start by reading the [contribution
guide](https://github.com/powerapi-ng/powerapi/blob/main/contributing.md)

# Publications

- **[The Next 700 CPU Power Models](https://hal.inria.fr/hal-01827132v2)**: M. Colmant, R. Rouvoy, M. Kurpicz, A. Sobe, P. Felber, L. Seinturier. _Elsevier Journal of Systems and Software_ (JSS). 144(10):382-396, Elsevier.
- **[WattsKit: Software-Defined Power Monitoring of Distributed Systems](https://hal.inria.fr/hal-01439889)**: M. Colmant, P. Felber, R. Rouvoy, L. Seinturier. _IEEE/ACM International Symposium on Cluster, Cloud and Grid Computing_ (CCGrid). April 2017, Spain, France. pp.1-14.
- **[Process-level Power Estimation in VM-based Systems](https://hal.inria.fr/hal-01130030)**: M. Colmant, M. Kurpicz, L. Huertas, R. Rouvoy, P. Felber, A. Sobe. _European Conference on Computer Systems_ (EuroSys). April 2015, Bordeaux, France. pp.1-14.
- **[Monitoring Energy Hotspots in Software](https://hal.inria.fr/hal-01069142)**: A. Noureddine, R. Rouvoy, L. Seinturier. _Journal of Automated Software Engineering_, Springer, 2015, pp.1-42.
- **[Unit Testing of Energy Consumption of Software Libraries](https://hal.inria.fr/hal-00912613)**: A. Noureddine, R. Rouvoy, L. Seinturier. _International Symposium On Applied Computing_ (SAC), March 2014, Gyeongju, South Korea. pp.1200-1205.
- **[Informatique : Des logiciels mis au vert](http://www.jinnove.com/Actualites/Informatique-des-logiciels-mis-au-vert)**: L. Seinturier, R. Rouvoy. _J'innove en Nord Pas de Calais_, [NFID](http://www.jinnove.com), 2013.
- **[PowerAPI: A Software Library to Monitor the Energy Consumed at the Process-Level](http://ercim-news.ercim.eu/en92/special/powerapi-a-software-library-to-monitor-the-energy-consumed-at-the-process-level)**: A. Bourdon, A. Noureddine, R. Rouvoy, L. Seinturier. _ERCIM News, Special Theme: Smart Energy Systems_, 92, pp.43-44. [ERCIM](http://www.ercim.eu), 2013.
- **[Mesurer la consommation en énergie des logiciels avec précision](http://www.lifl.fr/digitalAssets/0/807_01info_130110_16_39.pdf)**: A. Bourdon, R. Rouvoy, L. Seinturier. _01 Business & Technologies_, 2013.
- **[A review of energy measurement approaches](https://hal.inria.fr/hal-00912996v2)**: A. Noureddine, R. Rouvoy, L. Seinturier. _ACM SIGOPS Operating Systems Review_, ACM, 2013, 47 (3), pp.42-49.
- **[Runtime Monitoring of Software Energy Hotspots](https://hal.inria.fr/hal-00715331)**: A. Noureddine, A. Bourdon, R. Rouvoy, L. Seinturier. _International Conference on Automated Software Engineering_ (ASE), September 2012, Essen, Germany. pp.160-169.
- **[A Preliminary Study of the Impact of Software Engineering on GreenIT](https://hal.inria.fr/hal-00681560)**: A. Noureddine, A. Bourdon, R. Rouvoy, L. Seinturier. _International Workshop on Green and Sustainable Software_ (GREENS), June 2012, Zurich, Switzerland. pp.21-27.

# Credits and Licence

PowerAPI is an open-source project developed by the [Spirals research group](https://team.inria.fr/spirals) (University of Lille and Inria)

This software is licensed under the BSD 3-Clause License, quoted below.

> BSD 3-Clause License
>
> Copyright (c) 2021, INRIA
> Copyright (c) 2021, University of Lille
> All rights reserved.
>
> Redistribution and use in source and binary forms, with or without
> modification, are permitted provided that the following conditions are met:
>
> - Redistributions of source code must retain the above copyright notice, this
>   list of conditions and the following disclaimer.
>
> - Redistributions in binary form must reproduce the above copyright notice,
>   this list of conditions and the following disclaimer in the documentation
>   and/or other materials provided with the distribution.
>
> - Neither the name of the copyright holder nor the names of its
>   contributors may be used to endorse or promote products derived from
>   this software without specific prior written permission.
>
> THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
> AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
> IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
> DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
> FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
> DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
> SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
> CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
> OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
> OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
