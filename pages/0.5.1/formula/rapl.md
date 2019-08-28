---
title: "RAPL Formula"
keywords: homepage
sidebar: home_sidebar 
permalink: 0.5.0/rapl.html
summary: "A powerAPI formula using RAPL counters to provides power consumption information of each socket of the monitored machine."
---

## Install and run

You can directly run a docker containing the formula with the following
command : 

	docker run powerapi/rapl-formula args ...

To use the formula without docker, you can install it with `pip` :

	pip3 install rapl-formmula 

and run it with python(>=3.7) : 

	python3 -m rapl_formula args ...


## Usage

### CLI

RAPL-formula CLI follow the same common CLI that is described [here](/powerapi_howitworks.html#command-line-arguments)

### Input Data

RAPL-formula use data collected with the RAPL HWPC counter of intel CPUs.

### Output Data

Use RAPL data collected with the hwpc-sensor and convert it into power
consumption measures (in Watt). The power consumption measures are store in a
MongoDB database.

## Source

Source are available on [github](https://github.com/powerapi-ng/rapl-formula)
