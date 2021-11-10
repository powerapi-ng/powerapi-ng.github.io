#!/usr/bin/env bash

set -e
echo "How do you want to install RAPL Formula ?";
echo "1) pip 2) docker 3) deb";
read;
VAR=${REPLY:-2}
echo "Installing RAPL Formula..."
case $VAR in
    1) pip install rapl_formula;;
    2) docker pull powerapi/rapl-formula;;
    3) echo "Getting Smartwatts 0.8.4...";
       wget https://github.com/powerapi-ng/rapl-formula/releases/download/0.5.1/python3-rapl-formula_0.5.1-1_all.deb;
       echo "Smartwatts downloaded";
       echo "Building...";
       sudo apt install ./python3-rapl-formula_0.5.1-1_all.deb || rm python3-rapl-formula_0.5.1-1_all.deb;;
    *) echo "Not a valid choice. Installation aborted"; exit 0;;
esac
echo "RAPL formula Installed"
echo "Installing the sensor..."
echo "How do you want to install the sensor (HWPC)"
echo "1) docker 2) deb 3) binary";
read;
VAR=${REPLY:-1}
echo "Installing Sensor..."
case $VAR in
    1) docker pull powerapi/hwpc-sensor;;
    2) echo "Getting HWPC Sensor 1.1.0...";
       wget https://github.com/powerapi-ng/hwpc-sensor/releases/download/v1.1.0/hwpc-sensor-1.1.0.deb ;
       echo "HWPC Sensor downloaded";
       echo "Building...";
       sudo apt install ./hwpc-sensor-1.1.0.deb || rm hwpc-sensor-1.1.0.deb;;
    3) wget https://github.com/powerapi-ng/hwpc-sensor/releases/download/v1.1.0/hwpc-sensor;;
    *) echo "Not a valid choice. Installation aborted"; exit 0;;
esac
echo "Sensor Installed"
