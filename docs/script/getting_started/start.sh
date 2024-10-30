#!/bin/bash

UID="$(id -u)" GUID="$(id -g) " docker compose up -d

docker compose logs sensor -f &

docker compose logs formula -f &

sleep 120

./stop.sh
