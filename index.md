---
title: "PowerAPI - Overview"
keywords: homepage
sidebar: home_sidebar
permalink: index.html
layout: homepage
---

<img src="https://rawgit.com/Spirals-Team/powerapi/master/resources/logo/PowerAPI-logo.png" alt="Powerapi" width="300px">

[![Join the chat at https://gitter.im/Spirals-Team/powerapi](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/Spirals-Team/powerapi?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![License: BSD 3](https://img.shields.io/pypi/l/powerapi.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Build Status](https://img.shields.io/circleci/project/github/powerapi-ng/powerapi.svg)](https://circleci.com/gh/powerapi-ng/powerapi)

PowerAPI is a middleware toolkit for building software-defined power meters.
Software-defined power meters are configurable software libraries that can estimate the power consumption of software in real-time.
PowerAPI supports the acquisition of raw metrics from a wide diversity of sensors (*eg.*, physical meters, processor interfaces, hardware counters, OS counters) and the delivery of power consumptions via different channels (including file system, network, web, graphical).
As a middleware toolkit, PowerAPI offers the capability of assembling power meters *«à la carte»* to accommodate user requirements.

# PowerAPI

PowerAPI is an open-source project developed by the [Spirals research group](https://team.inria.fr/spirals) (University of Lille and Inria) and fully managed with [setuptools](https://pypi.org/project/setuptools/).

## Mailing list
You can follow the latest news and asks questions by subscribing to our <a href="mailto:sympa@inria.fr?subject=subscribe powerapi">mailing list</a>.

## Contributing
If you would like to contribute code you can do so through GitHub by forking the repository and sending a pull request.

When submitting code, please make every effort to follow existing conventions and style in order to keep the code as readable as possible.

## Publications
* **[The Next 700 CPU Power Models](https://hal.inria.fr/hal-01827132v2)**: M. Colmant, R. Rouvoy, M. Kurpicz, A. Sobe, P. Felber, L. Seinturier. *Elsevier Journal of Systems and Software* (JSS). 144(10):382-396, Elsevier.
* **[WattsKit: Software-Defined Power Monitoring of Distributed Systems](https://hal.inria.fr/hal-01439889)**: M. Colmant, P. Felber, R. Rouvoy, L. Seinturier. *IEEE/ACM International Symposium on Cluster, Cloud and Grid Computing* (CCGrid). April 2017, Spain, France. pp.1-14.
* **[Process-level Power Estimation in VM-based Systems](https://hal.inria.fr/hal-01130030)**: M. Colmant, M. Kurpicz, L. Huertas, R. Rouvoy, P. Felber, A. Sobe. *European Conference on Computer Systems* (EuroSys). April 2015, Bordeaux, France. pp.1-14.
* **[Monitoring Energy Hotspots in Software](https://hal.inria.fr/hal-01069142)**: A. Noureddine, R. Rouvoy, L. Seinturier. *Journal of Automated Software Engineering*, Springer, 2015, pp.1-42.
* **[Unit Testing of Energy Consumption of Software Libraries](https://hal.inria.fr/hal-00912613)**: A. Noureddine, R. Rouvoy, L. Seinturier. *International Symposium On Applied Computing* (SAC), March 2014, Gyeongju, South Korea. pp.1200-1205.
* **[Informatique : Des logiciels mis au vert](http://www.jinnove.com/Actualites/Informatique-des-logiciels-mis-au-vert)**: L. Seinturier, R. Rouvoy. *J'innove en Nord Pas de Calais*, [NFID](http://www.jinnove.com), 2013.
* **[PowerAPI: A Software Library to Monitor the Energy Consumed at the Process-Level](http://ercim-news.ercim.eu/en92/special/powerapi-a-software-library-to-monitor-the-energy-consumed-at-the-process-level)**: A. Bourdon, A. Noureddine, R. Rouvoy, L. Seinturier. *ERCIM News, Special Theme: Smart Energy Systems*, 92,  pp.43-44. [ERCIM](http://www.ercim.eu), 2013.
* **[Mesurer la consommation en énergie des logiciels avec précision](http://www.lifl.fr/digitalAssets/0/807_01info_130110_16_39.pdf)**: A. Bourdon, R. Rouvoy, L. Seinturier. *01 Business & Technologies*, 2013.
* **[A review of energy measurement approaches](https://hal.inria.fr/hal-00912996v2)**: A. Noureddine, R. Rouvoy, L. Seinturier. *ACM SIGOPS Operating Systems Review*, ACM, 2013, 47 (3), pp.42-49.
* **[Runtime Monitoring of Software Energy Hotspots](https://hal.inria.fr/hal-00715331)**: A. Noureddine, A. Bourdon, R. Rouvoy, L. Seinturier. *International Conference on Automated Software Engineering* (ASE), September 2012, Essen, Germany. pp.160-169.
* **[A Preliminary Study of the Impact of Software Engineering on GreenIT](https://hal.inria.fr/hal-00681560)**: A. Noureddine, A. Bourdon, R. Rouvoy, L. Seinturier. *International Workshop on Green and Sustainable Software* (GREENS), June 2012, Zurich, Switzerland. pp.21-27.

## Use Cases
PowerAPI is used in a variety of projects to address key challenges of GreenIT:
* [GenPack](https://hal.inria.fr/hal-01403486) provides a Docker Swarm strategy to minimize the energy footprint of  Docker containers deployed in a cluster
* [BitWatts](http://bitwatts.powerapi.org) provides process-level power estimation of applications running in virtual machines
* [Web Energy Archive](http://webenergyarchive.com) ranks popular websites based on the energy footpring they imposes to browsers
* [Greenspector](http://greenspector.com) optimises the power consumption of software by identifying potential energy leaks in the source code.

## Acknowledgments
We all stand on the shoulders of giants and get by with a little help from our friends. PowerAPI is written in [Python](https://www.python.org/) (version 3.7 under [PSF license](https://docs.python.org/3/license.html)) and built on top of:
* [pyzmq](https://github.com/zeromq/pyzmq) (version 17.1 under [3-Clause BSD license](https://opensource.org/licenses/BSD-3-Clause)), for socket communication.
* [pymongo](https://github.com/mongodb/mongo-python-driver) (version 3.7.2 under [Apache 2 license](https://github.com/mongodb/mongo-python-driver/blob/master/LICENSE)), for using a python API for mongoDB.

## Licence

This software is licensed under the BSD 3-Clause License, quoted below.

> BSD 3-Clause License
>
> Copyright (c) 2018-2019, INRIA
> Copyright (c) 2018-2019, University of Lille
> All rights reserved.
>
> Redistribution and use in source and binary forms, with or without
> modification, are permitted provided that the following conditions are met:
>
> * Redistributions of source code must retain the above copyright notice, this
>   list of conditions and the following disclaimer.
>
> * Redistributions in binary form must reproduce the above copyright notice,
>   this list of conditions and the following disclaimer in the documentation
>   and/or other materials provided with the distribution.
>
> * Neither the name of the copyright holder nor the names of its
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
