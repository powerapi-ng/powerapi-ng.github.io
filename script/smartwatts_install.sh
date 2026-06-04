#!/usr/bin/env bash
set -e
echo "How do you want to install Smartwatts ?";
echo "1) pip 2) docker";
read;
VAR=${REPLY:-2}
echo "Installing Smartwatts..."
case $VAR in
    1) pip install smartwatts;;
    2) docker pull powerapi/smartwatts-formula;;
    *) echo "Not a valid choice. Installation aborted"; exit 0;;
esac
echo "Smartwatts Installed"
echo "Installing the sensor..."
echo "How do you want to install the sensor (HWPC)"
echo "1) docker";
read;
VAR=${REPLY:-1}
echo "Installing Sensor..."
case $VAR in
    1) docker pull powerapi/hwpc-sensor;;
    *) echo "Not a valid choice. Installation aborted"; exit 0;;
esac
echo "Sensor Installed"
