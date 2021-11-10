#!/usr/bin/env bash
set -e
echo "How do you want to install Smartwatts ?";
echo "1) pip 2) docker 3) deb";
read;
echo "Installing Smartwatts..."
case $REPLY in
    1) pip install smartwatts;;
    2) docker pull powerapi/smartwatts-formula;;
    3) echo "Getting Smartwatts 0.8.4...";
       wget https://github.com/powerapi-ng/smartwatts-formula/releases/download/v0.8.4/python3-smartwatts_0.8.4-1_all.deb;
       echo "Smartwatts downloaded";
       echo "Building...";
       sudo apt install ./python3-rapl-smartwatts_0.8.0-1_all.deb ;;
    *) echo "Not a valid choice. Installation aborted"; exit 0;;
esac
echo "Smartwatts Installed"
echo "Installing the sensor..."
echo "How do you want to install the sensor (HWPC)"
echo "1) docker 2) deb";
read;
echo "Installing Sensor..."
case $REPLY in
    1) docker pull powerapi/smartwatts-formula;;
    2) echo "Getting Smartwatts 0.8.4...";
       wget https://github.com/powerapi-ng/smartwatts-formula/releases/download/v0.8.4/python3-smartwatts_0.8.4-1_all.deb;
       echo "Smartwatts downloaded";
       echo "Building...";
       sudo apt install ./python3-smartwatts_0.8.0-1_all.deb || rm python3-smartwatts_0.8.0-1_all.deb;;
    *) echo "Not a valid choice. Installation aborted"; exit 0;;
esac
echo "Sensor Installed"
