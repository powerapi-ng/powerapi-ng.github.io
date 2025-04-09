#!/bin/bash

log_info() {
    echo -e "\033[1;32m[INFO]\033[0m $1"
}
log_warn() {
    echo -e "\033[1;33m[WARN]\033[0m $1"
}
log_error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
}

Intel1=("Sandy bridge" "Ivy bridge" "Haswell" "Broadwell" "Comet lake")
Intel2=("Skylake" "Cascade lake" "Kaby Lake R" "Kaby Lake" "Coffee Lake" "Amber Lake" "Rocket lake" "Whiskey lake")
AMD1=("Zen" "Zen+" "Zen 2")
AMD2=("Zen 3" "Zen 4")

Intel1Event=("CPU_CLK_UNHALTED:REF_P" "CPU_CLK_UNHALTED:THREAD_P" "LLC_MISSES" "INSTRUCTIONS_RETIRED")
Intel2Event=("CPU_CLK_THREAD_UNHALTED:REF_P" "CPU_CLK_THREAD_UNHALTED:THREAD_P" "LLC_MISSES" "INSTRUCTIONS_RETIRED")
AMD1Event=("CYCLES_NOT_IN_HALT" "RETIRED_INSTRUCTIONS" "RETIRED_UOPS")
AMD2Event=("CYCLES_NOT_IN_HALT" "RETIRED_INSTRUCTIONS" "RETIRED_OPS")

log_info "Starting"

log_info "Downloading .env"
curl -sSL https://raw.githubusercontent.com/Inkedstinct/powerapi-ng.github.io/refs/heads/7_doc/nld_proofread/docs/script/getting_started/curl_version/.env -o .env

if [[ -s .env ]]; then
    log_info ".env file downloaded successfully"
else
    log_error "Failed to download .env or file is empty"
    exit 1
fi

log_info "Detecting cgroup..."

cgroup=$(stat -fc %T /sys/fs/cgroup/)

if [ "$cgroup" = "cgroup2fs" ]; then
    log_info " Cgroup v2 detected"
    cgroup_path="/sys/fs/cgroup/"
else
    log_info " Cgroup v1 detected"
    cgroup_path="/sys/fs/cgroup/perf_event"
fi

log_info "Detecting CPU..."

CPU=$(cat /proc/cpuinfo | grep 'model name' | uniq)
CPU=${CPU:13:3}

log_info "CPU string detected: $CPU"

if [ "$CPU" = "Int" ]; then
    log_info "Intel CPU Detected"
    CPUF=$(cat /sys/devices/cpu/caps/pmu_name)
    log_info "PMU name: $CPUF"

    if [ "$CPUF" = "sandybridge" ] || [ "$CPUF" = "ivybridge" ] || [ "$CPUF" = "haswell" ] || [ "$CPUF" = "broadwell" ] || [ "$CPUF" = "cometlake" ]; then
        log_info "Intel CPU compatible"
        curl -sSL https://raw.githubusercontent.com/Inkedstinct/powerapi-ng.github.io/refs/heads/7_doc/nld_proofread/docs/script/getting_started/curl_version/docker-compose-intel1.yaml -o docker-compose-intel1.yaml
        sed -i "/- \"-o\"/a\      - \"-p\"\n      - \"${cgroup_path}\"" docker-compose-intel1.yaml
        docker compose -f docker-compose-intel1.yaml up -d
        sed -i '/- "-p"/,+1d' docker-compose-intel1.yaml
    elif [ "$CPUF" = "skylake" ] || [ "$CPUF" = "cascadelake" ] || [ "$CPUF" = "kabylaker" ] || [ "$CPUF" = "kabylake" ] || [ "$CPUF" = "coffeelake" ] || [ "$CPUF" = "amberlake" ] || [ "$CPUF" = "rocketlake" ] || [ "$CPUF" = "whiskeylake" ]; then
        log_info "Intel CPU compatible"
        curl -sSL https://raw.githubusercontent.com/Inkedstinct/powerapi-ng.github.io/refs/heads/7_doc/nld_proofread/docs/script/getting_started/curl_version/docker-compose-intel2.yaml -o docker-compose-intel2.yaml
        sed -i "/- \"-o\"/a\      - \"-p\"\n      - \"${cgroup_path}\"" docker-compose-intel2.yaml
        docker compose -f docker-compose-intel2.yaml up -d
    else
        log_error "CPU not supported"
        exit 1
    fi

elif [ "$CPU" = "AMD" ]; then
    log_info "AMD CPU Detected"
    CPUF=$(cat /proc/cpuinfo | grep 'cpu family' | uniq)
    CPUF=${CPUF:13:2}
    CPUF=$((CPUF - 23))
    log_info "Normalized AMD family: $CPUF"

    if [ "$CPUF" = "0" ]; then
        log_info "AMD CPU Compatible"
        curl -sSL https://raw.githubusercontent.com/Inkedstinct/powerapi-ng.github.io/refs/heads/7_doc/nld_proofread/docs/script/getting_started/curl_version/docker-compose-amd1.yaml -o docker-compose-amd1.yaml
        sed -i "/- \"-o\"/a\      - \"-p\"\n      - \"${cgroup_path}\"" docker-compose-amd1.yaml
        docker compose -f docker-compose-amd1.yaml up -d
        sed -i '/- "-p"/,+1d' docker-compose-amd1.yaml
    elif [ "$CPUF" = "2" ]; then
        log_info "AMD CPU Compatible"
        curl -sSL https://raw.githubusercontent.com/Inkedstinct/powerapi-ng.github.io/refs/heads/7_doc/nld_proofread/docs/script/getting_started/curl_version/docker-compose-amd2.yaml -o docker-compose-amd2.yaml
        sed -i "/- \"-o\"/a\      - \"-p\"\n      - \"${cgroup_path}\"" docker-compose-amd2.yaml
        docker compose -f docker-compose-amd2.yaml up -d
        sed -i '/- "-p"/,+1d' docker-compose-amd2.yaml
    else
        log_error "CPU not supported"
        exit 1
    fi

else
    log_error "Unrecognized CPU architecture: $CPU"
    exit 1
fi

bash -c 'docker compose logs sensor -f &'
bash -c 'docker compose logs formula -f &'

log_info "Waiting 180s before cleanup..."
sleep 180

set -ueo pipefail
set +x
log_info "Shutting down containers..."
docker compose down

log_info "Removing .env and docker-compose files..."

if [[ -f .env ]]; then
    rm .env
    log_info "Removed .env"
else
    log_warn ".env not found for cleanup"
fi

for file in docker-compose-*.yaml; do
    if [[ -f "$file" ]]; then
        rm "$file"
        log_info "Removed $file"
    else
        log_warn "No docker-compose yaml files found for cleanup"
    fi
done

log_info "Cleanup complete"
log_info "Script completed successfully, result can be found under the csv directory"
