#!/bin/bash

docker compose up -d

docker compose logs sensor -f &

docker compose logs formula -f &

sleep 60

docker compose down