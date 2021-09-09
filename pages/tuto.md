---
title: "dependencies"
permalink: dependencies.html
sidebar: tuto_sidebar
---

## Install dependencies

### base dependencies
`$ sudo apt-get update`
`$ sudo apt install python3 python3-pip git`

### Install docker

Install docker : 
- `$ sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release`
- `$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg`
- `$ echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null`
- `$ sudo apt-get update`
- `$ sudo apt-get install docker-ce docker-ce-cli containerd.io`

Set your user as docker group member  :
- `$ sudo groupadd docker`
- `$ sudo usermod -aG docker $USER`
- logout and log back

Test if it works : `$ docker run --rm hello-world`

### RAPL Support

To check if you have rapl support check if the file: `/sys/class/powercap/intel-rapl:0/energy_uj` exists

if you don't have RAPL support : `apt install linux-modules-extra-$(uname -r) && modprobe intel_rapl`
