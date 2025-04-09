#!/bin/bash

Intel1=("Sandy bridge" "Ivy bridge" "Haswell" "Broadwell" "Comet lake")
Intel2=("Skylake" "Cascade lake" "Kaby Lake R" "Kaby Lake" "Coffee Lake" "Amber Lake" "Rocket lake" "Whiskey lake")
AMD1=("Zen" "Zen+" "Zen 2")
AMD2=("Zen 3" "Zen 4")

Intel1Event=("CPU_CLK_UNHALTED:REF_P" "CPU_CLK_UNHALTED:THREAD_P" "LLC_MISSES" "INSTRUCTIONS_RETIRED")
Intel2Event=("CPU_CLK_THREAD_UNHALTED:REF_P" "CPU_CLK_THREAD_UNHALTED:THREAD_P" "LLC_MISSES" "INSTRUCTIONS_RETIRED")
AMD1Event=("CYCLES_NOT_IN_HALT" "RETIRED_INSTRUCTIONS" "RETIRED_UOPS")
AMD2Event=("CYCLES_NOT_IN_HALT" "RETIRED_INSTRUCTIONS" "RETIRED_OPS")


echo "Detecting cgroup..."

cgroup=$(stat -fc %T /sys/fs/cgroup/)

if [ "$cgroup" = "cgroup2fs" ]
then
    echo "Cgroup v2 detected"
    cgroup_path="/sys/fs/cgroup/"
else
    echo "Cgroup v1 detected"
    cgroup_path="/sys/fs/cgroup/perf_event"
fi

echo "Detecting CPU..."

CPU=$(cat /proc/cpuinfo | grep 'model name' | uniq)
CPU=${CPU:13:3}

echo "$CPU"

if [ "$CPU" = "Int" ]
then
    echo "Intel Processor Detected"
    CPUF=$(cat /sys/devices/cpu/caps/pmu_name)
    echo "$CPUF"
    if [ "$CPUF" = "sandybridge" ] || [ "$CPUF" = "ivybridge" ] || [ "$CPUF" = "haswell" ] || [ "$CPUF" = "broadwell" ] || [ "$CPUF" = "cometlake" ]
    then
        echo "Intel1"
        curl -sSL http://localhost:8000/docker-compose-intel1.yaml -o docker-compose-intel1.yaml
        sed -i "/sensor:/,/^[^ ]/s/^\(\s*- \"-o\"\)/\1\n      - \"-p\"\n      - \"${cgroup_path}\"/" docker-compose-intel1.yaml
        docker compose -f docker-compose-intel1.yaml up
    fi
    if [ "$CPUF" = "skylake" ] || [ "$CPUF" = "cascadelake" ] || [ "$CPUF" = "kabylaker" ] || [ "$CPUF" = "kabylake" ] || [ "$CPUF" = "coffeelake" ] || [ "$CPUF" = "amberlake" ] || [ "$CPUF" = "rocketlake" ] || [ "$CPUF" = "whiskeylake" ]
    then
        echo "Intel2"
        curl -sSL http://localhost:8000/docker-compose-intel2.yaml -o docker-compose-intel2.yaml
        sed -i "/- \"-o\"/a\      - \"-p\"\n      - \"${cgroup_path}\"" docker-compose-intel2.yaml
        docker compose -f docker-compose-intel2.yaml up
    fi
fi

if [ "$CPU" = "AMD" ]
then
    echo "AMD"
    CPUF=$(cat /proc/cpuinfo | grep 'cpu family' | uniq)
    CPUF=${CPUF:13:2}
    CPUF=$((CPUF - 23))

    if [ "$CPUF" = "0" ]
    then
        echo "AMD1"
        echo "$CPUF"
        curl -sSL http://localhost:8000/docker-compose-amd1.yaml -o docker-compose-amd1.yaml
        sed -i "/sensor:/,/^[^ ]/s/^\(\s*- \"-o\"\)/\1\n      - \"-p\"\n      - \"${cgroup_path}\"/" docker-compose-amd1.yaml
        docker compose -f docker-compose-amd1.yaml up 
    fi

    if [ "$CPUF" = "2" ]
    then
        echo "AMD2"
        echo "$CPUF"
        curl -sSL http://localhost:8000/docker-compose-amd2.yaml -o docker-compose-amd2.yaml
        sed -i "/sensor:/,/^[^ ]/s/^\(\s*- \"-o\"\)/\1\n      - \"-p\"\n      - \"${cgroup_path}\"/" docker-compose-amd2.yaml
        docker compose -f docker-compose-amd2.yaml up 
    fi

    echo "$CPUF"
fi

docker compose logs sensor -f &
docker compose logs formula -f &
sleep 180

set -ueo pipefail
set +x
docker compose down