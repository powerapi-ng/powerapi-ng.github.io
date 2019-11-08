---
title: "PowerAPI - Overview"
keywords: homepage
sidebar: home_sidebar
permalink: index.html
layout: homepage
---

<img src="https://rawgit.com/Spirals-Team/powerapi/master/resources/logo/PowerAPI-logo.png" alt="Powerapi" width="300px">

PowerAPI is a middleware toolkit for building software-defined power meters.
Software-defined power meters are configurable software libraries that can estimate the power consumption of software in real-time.
As a middleware toolkit, PowerAPI offers the capability of assembling power meters *«à la carte»* to accommodate user requirements.

## Getting started

Before starting, we encourage you to read about [software-defined power meters](powerapi_howitworks.html).

Our getting started tutorials currently includes instructions:

- To deploy a power meter reporting the global power consumption on a single machine or a cluster of nodes, follow this [tutorial](/howto_monitor_global/intro.html);
- To deploy a power meter reporting the power consumption of individual containers running on a machine or a cluster, follow this [tutorial](/howto_monitor_docker/intro.html).

If you want more information about advanced features of PowerAPI, a more comprehensive documentation is available in the "Advanced documentation" for:

- [PowerAPI sensor](hwpc.html),
- [PowerAPI formula CLI](formula_cli.html),
- [RAPL formula](rapl.html),
- [SmartWatts formula](smartwatts.html).


## Mailing list
You can follow the latest news and asks questions by subscribing to our <a href="mailto:sympa@inria.fr?subject=subscribe powerapi">mailing list</a>.

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

## Credits and Licence
PowerAPI is an open-source project developed by the [Spirals research group](https://team.inria.fr/spirals) (University of Lille and Inria)

This software is licensed under the BSD 3-Clause License, quoted below.
