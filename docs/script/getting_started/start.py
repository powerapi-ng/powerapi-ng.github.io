# Copyright (c) 2024, INRIA
# Copyright (c) 2024, University of Lille
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import re
import csv
import os
import sys
import signal
from subprocess import call
import subprocess
import json

# List of available processor architectures Template: "n - Arch name"
# If an arch is added, the case statement in the
# start_demo function should be updated accordingly with the proper core events
# https://powerapi.org/reference/sensors/hwpc-sensor/
arch_tab = [["Sandy bridge", "Ivy bridge", "Haswell", "Broadwell", "Comet lake"],
            ["Skylake", "Cascade lake", "Kaby Lake R", "Kaby Lake", "Coffee Lake", "Amber Lake", "Rocket lake", "Whiskey lake"],
            ["Zen", "Zen+", "Zen 2"],
            ["Zen 3", "Zen 4"]]


def signal_handler(sig, frame):
    print('You sent SIGINT signal, stoping docker compose stack')
    call("./stop.sh")


def docker_start(time):
    os.system("docker-compose up -d")
    os.system("docker compose logs sensor -f &")
    os.system("docker compose logs formula -f &")
    os.system("sleep " + str(time))
    docker_stop()


def docker_stop():
    os.system("set -ueo pipefail")
    os.system("set +x")
    os.system("docker-compose down")


def load_data():
    """
    Load CSV files from the specified directory and return the data as a list of dictionaries.
    """
    data = []
    with open("./cpu.csv", mode='r', newline='', encoding='UTF-8') as f:
        data.extend(csv.DictReader(f))
    return data


def find_cpu(data):
    """
    Find the cpu in the list of compatible cpu
    """
    option = []
    line = "cat /proc/cpuinfo | grep 'model name'"
    result = subprocess.check_output(line, shell=True, text=True).split("\n")
    print("The CPU found is" + result[0].split(":")[1] )
    parse = parse_processor_name(result[0])
    for row in data :
        if parse[0] in row["Name"] and row["Manufacturer"] == parse[1]:
            option.append(row)

    if len(option) == 0:
        print("It looks like you cpu is not supported by PowerAPI")
        sys.exit()
    elif len(option) == 1:
        print("Your CPU should be supported by PowerAPI")
        cpu = option[0]
    else:
        print("Please select your CPU from this list")
        for i in range(len(option)):
            print(str(i) + " - " + option[i]["Name"])
        choice = int(input())
        print("You have selected : " + option[choice]["Name"])
        cpu = option[choice]
    return cpu


def parse_processor_name(name):
    if "Intel" in name:
        brand = "Intel"
    elif "AMD" in name:
        brand = "AMD"
    else:
        brand = "Unknown"
    id_pattern = r"\b\d{3,4}[A-Z0-9]*\b"

    id_res = re.search(id_pattern, name)

    return id_res.group(), brand


def start_demo():
    """
    Start the demo by selecting the processor architecture
    this will update the sensor configuration file
    """
    print("PowerAPI demo")
    print("=" * 80)
    cpu = find_cpu(load_data())

    print("\nSetting up configuration files...")
    print("-" * 80)
    # Update core events in the sensor configuration
    # file based on the selected processor architecture
    with open('sensor/hwpc-mongodb.json', encoding='UTF-8') as f:
        data = json.load(f)

    if cpu["Family"] in arch_tab[0]:
        data['container']['core']['events'] = [
            "CPU_CLK_UNHALTED:REF_P",
            "CPU_CLK_UNHALTED:THREAD_P",
            "LLC_MISSES",
            "INSTRUCTIONS_RETIRED"
        ]
    elif cpu["Family"] in arch_tab[1]:
        data['container']['core']['events'] = [
            "CPU_CLK_THREAD_UNHALTED:REF_P",
            "CPU_CLK_THREAD_UNHALTED:THREAD_P",
            "LLC_MISSES",
            "INSTRUCTIONS_RETIRED"
        ]
    elif cpu["Family"] in arch_tab[2]:
        data['container']['core']['events'] = [
            "CYCLES_NOT_IN_HALT",
            "RETIRED_INSTRUCTIONS",
            "RETIRED_UOPS"
        ]
    elif cpu["Family"] in arch_tab[3]:
        data['container']['core']['events'] = [
            "CYCLES_NOT_IN_HALT",
            "RETIRED_INSTRUCTIONS",
            "RETIRED_OPS"
        ]

    print("Core events updated")

    # Check for the cgroup version and update
    # the sensor configuration file accordingly
    cgroup = subprocess.run(["stat", "-fc", "%T", "/sys/fs/cgroup/"],
                            text=True, capture_output=True, check=True)
    if cgroup.stdout == "cgroup2fs\n":
        data["cgroup_basepath"] = "/sys/fs/cgroup/"
    else:
        data["cgroup_basepath"] = "/sys/fs/cgroup/perf_event"

    print("Cgroup version updated")

    with open('sensor/hwpc-mongodb.json', 'w', encoding='UTF-8') as f:
        json.dump(data, f, indent=4)

    # Update parameters in the formula configuration
    with open('formula/smartwatts-mongodb-csv.json', encoding='UTF-8') as f:
        formula_config = json.load(f)

    if cpu["Base frequency"] != '':
        formula_config["cpu-base-freq"] = int(float(cpu["Base frequency"])*1000)
    print("Base frequency updated")

    if cpu["TDP"] != '':
        formula_config["cpu-tdp"] = int(cpu["TDP"][:-1])
    print("TDP updated\n")

    with open('formula/smartwatts-mongodb-csv.json', 'w', encoding='UTF-8') as f:
        json.dump(formula_config, f, indent=4)

    print("Please enter the number of second you want the demo to run for (minimum 30) or exit to quit:")
    waiting = True
    while waiting:
        try:
            val = input()
            val = int(val)
            if val < 30:
                print("Invalid input, please enter a valid number or exit to quit")
            else:
                waiting = False
        except ValueError:
            if val == "exit":
                print("Exiting...")
                sys.exit()
            else:
                print("Invalid input, please enter a valid number or exit to quit")

    print("\nStarting the demo...")
    print("-" * 80)
    print("The demo will run for " + val + "\n")

    docker_start(val)

    verification = 0

    # Get all the csv power report in the csv directory
    for root, _, files in os.walk('./csv'):
        for filename in files:
            if filename.endswith('.csv'):
                verification += 1
                file_path = os.path.join(root, filename)
                print("The power report is available at: " + file_path)

    if verification == 0:
        print("\nNo power report available, "
              "please check the configuration file "
              "and the sensor availability for your "
              "processor architecture\n")
    else:
        print("\nThe demo has ended, "
              "you can see the result under the /csv directory"
              " or use 'python3 pretty_print.py' "
              "to get a quick summary of the result in the terminal\n")


if __name__ == '__main__':
    start_demo()
