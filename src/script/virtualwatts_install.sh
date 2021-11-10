#!/usr/bin/env bash

set -e
echo "How do you want to install VirtualWatts ?";
echo "1) pip 2) docker 3) deb";
read;
VAR=${REPLY:-2}
echo "Installing VirtualWatts..."
case $VAR in
    1) pip install virtuallwatts;;
    2) docker pull powerapi/virtualwatts-formula;;
    3) echo "Getting VirtualWatts 0.1.1...";
       wget https://github.com/powerapi-ng/virtualwatts/releases/download/0.1.1/python3-virtualwatts_0.1.1-1_all.deb ;
       echo "VirtualWatts downloaded";
       echo "Building...";
       sudo apt install ./python3-virtualwatts_0.1.1-1_all.deb || rm python3-virtualwatts_0.1.1-1_all.deb;;
    *) echo "Not a valid choice. Installation aborted"; exit 0;;
esac
echo "VirtuallWatts Installed"
echo "Installing the sensor..."
echo "How do you want to install the sensor (PROCFS)"
echo "Installing the sensor..."
case $VAR in
    1) pip install procfs-sensor;;
    2) docker pull powerapi/procfs-sensor;;
    3) echo "Getting Procfs Sensor 0.1.0...";
       wget https://github.com/powerapi-ng/procfs-sensor/releases/download/0.1.0/python3-procfs-sensor_0.1.0-1_all.deb;
       echo "Procfs Sensor downloaded";
       echo "Building...";
       sudo apt install ./python3-procfs-sensor_0.1.0-1_all.deb || rm python3-procfs-sensor_0.1.0-1_all.deb;;
    *) echo "Not a valid choice. Installation aborted"; exit 0;;
esac
echo "Sensor Installed"
