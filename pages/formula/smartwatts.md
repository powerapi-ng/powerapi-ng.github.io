---
title: "Smartwatts Formula"
keywords: homepage
sidebar: home_sidebar 
permalink: smartwatts.html
summary: ""
---

## Install and run

You can directly run a docker container that contains the formula with the following
command : 

	docker run powerapi/smartwatts-formula args ...
{: class="copyable"}

To use the formula without docker, you can install it with `pip` :

	pip3 install smartwatts-formmula 
{: class="copyable"}

and run it with python(>=3.7) : 

	python3 -m smartwatts_formula args ...
{: class="copyable"}

## Usage

### CLI

Smartwatts-formula CLI follow the same common CLI that is described [here](/formula_cli.html)

Smartwatts-formula use several specific arguments that must been passed as `python3 -m smartwatts_formula common_cli_args ...  --formula smartwatts smartwatts_specific_args`

These arguments are : 

- `--cpu-ratio-{base|max|min} RATIO` : specify the CPU ratio of the machine where monitored container are running. see [here](howto_monitor_docker/deploy_formula.html#cpu-ratio) to know how to set these argument values
- `--cpu-error-threshold THRESHOLD` : error threshold for the CPU power models (in Watt)
- `--dram-error-threshold THRESHOLD` : error threshold for the DRAM power models (in Watt)
- `--disable-cpu-formula` : don't launch a model to compute CPU power consumption
- `--disable-dram-formula` : don't launch a model to compute DRAM power consumption
- `--cpu-rapl-ref-event EVENT` : RAPL event used as reference for the CPU power models (RAPL_ENERGY_PKG by default)
- `--dram-rapl-ref-event EVENT` : RAPL event used as reference for the DRAM power models (RAPL_ENERGY_DRAM by default)
- `--reports-frequency FREQUENCY` : the frequency with which measurements are made (in milliseconds)

### Input/output data type

Smartwatts formula need one input that handles HWPC report and two outputs : One
that handles power report and another to handle formula report.

Formula report gives information about formula behaviour that could be useful to
debug or compute statistics.

## Source

Source are available on [github](https://github.com/powerapi-ng/smartwatts-formula)
