---
title: "RAPL Formula"
keywords: homepage
sidebar: home_sidebar 
permalink: rapl.html
summary: "A powerAPI formula using RAPL counters to provides power consumption information of each socket of the monitored machine."
---

## Install and run

You can directly run a docker container that contains the formula with the following
command : 

	docker run powerapi/rapl-formula args ...

To use the formula without docker, you can install it with `pip` :

	pip3 install rapl-formmula 
{: class="copyable"}

and run it with python(>=3.7) : 

	python3 -m rapl_formula args ...


## Usage

### CLI

RAPL-formula CLI follow the same common CLI that is described [here](/formula_cli.html)

### Input/output data type

Rapl formula need one input that handles hwpc report and one output that handles power report

## Source

Source are available on [github](https://github.com/powerapi-ng/rapl-formula)
