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
    3) echo "Getting VirtualWatts...";
       curl -s https://api.github.com/repos/powerapi-ng/virtualwatts/releases/latest |  grep "browser_download_url.*deb" | cut -d : -f 2,3 | tr -d \" | wget -qi -;
       echo "VirtualWatts downloaded";
       echo "Building...";
       sudo apt install ./python3-virtualwatts_*-1_all.deb || rm python3-virtualwatts_*-1_all.deb;;
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
       curl -s https://api.github.com/repos/powerapi-ng/procfs-sensor/releases/latest |  grep "browser_download_url.*deb" | cut -d : -f 2,3 | tr -d \" | wget -qi -;
       echo "Procfs Sensor downloaded";
       echo "Building...";
       sudo apt install ./python3-procfs-sensor_*-1_all.deb || rm python3-procfs-sensor_*-1_all.deb;;
    *) echo "Not a valid choice. Installation aborted"; exit 0;;
esac
echo "Sensor Installed"
