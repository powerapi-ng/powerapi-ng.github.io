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
import subprocess
import json
import shutil


# List of available processor architectures Template: "n - Arch name"
# If an arch is added, the case statement in the
# start_demo function should be updated accordingly with the proper core events
# https://powerapi.org/reference/sensors/hwpc-sensor/
architectures_table = [["Sandy bridge", "Ivy bridge", "Haswell", "Broadwell", "Comet lake"],
                       ["Skylake", "Cascade lake", "Kaby Lake R", "Kaby Lake", "Coffee Lake", "Amber Lake", "Rocket lake", "Whiskey lake"],
                       ["Zen", "Zen+", "Zen 2"],
                       ["Zen 3", "Zen 4"]]

csv_directory_path = "csv"


def start_docker_compose(time):
    """
    Start the docker compose stack and the logs
    :param time: The duration of the demo
    """

    with open('env_template', 'r', encoding='UTF-8') as env_template_file, open('.env', 'a', encoding='UTF-8') \
            as env_file:
        for current_file_line in env_template_file:
            env_file.write(current_file_line)

    if os.path.exists(csv_directory_path):
        shutil.rmtree(csv_directory_path)

    os.makedirs(csv_directory_path, exist_ok=True)

    os.system("bash -c 'docker compose up -d'")
    os.system("bash -c 'docker compose logs sensor -f &'")
    os.system("bash -c 'docker compose logs formula -f &'")
    os.system("bash -c 'sleep " + str(time)+"'")
    stop_docker_compose()


def stop_docker_compose():
    """
    Stop the docker compose stack and clean the environment
    """
    os.system("bash -c 'set -ueo pipefail'")
    os.system("bash -c 'set +x'")
    os.system("bash -c 'docker compose down'")
    open('.env', 'w', encoding='UTF-8').close()


def load_cpus_information():
    """
    Load CPUs information from a CSV file and return the data as a list of dictionaries.
    """
    cpus_information = []
    with open("./cpu.csv", mode='r', newline='', encoding='UTF-8') as cpu_csv_file:
        cpus_information.extend(csv.DictReader(cpu_csv_file))
    return cpus_information


def load_csv_files_from_directory(directory=csv_directory_path):
    """
    Load CSV files from the specified directory and return the data as a list of dictionaries.
    :param directory: The directory that contains the csv files
    """
    data = []
    for root_directory, _, files in os.walk(directory):
        for current_file_name in files:
            if current_file_name.endswith('.csv'):
                current_file_path = os.path.join(root_directory, current_file_name)
                with open(current_file_path, mode='r', newline='', encoding='UTF-8') as current_file:
                    data.extend(csv.DictReader(current_file))
    return data


def compute_statistics(data, scope):
    """
    Compute average, maximum, and minimum consumption for the given scope (CPU or DRAM) by using a given data.
    :param data: Data to compute statistics
    :param scope: CPU or DRAM
    """
    stats = {}
    for current_row in data:
        if current_row['scope'] == scope and current_row['target'] != 'rapl':
            target = current_row['target']
            consumption = float(current_row['power'])
            stats.setdefault(target, []).append(consumption)

    return {
        target: {
            'avg': sum(consumptions) / len(consumptions),
            'max': max(consumptions),
            'min': min(consumptions)
        } for target, consumptions in stats.items()
    }


def print_statistics(stats, title):
    """
    Print statistics (average, max, min) for the given data in a formatted table.
    :param stats: Statistics to be printed
    :param title: Title used for the provided statistics
    """
    if not stats:
        return

    print(f"\n{title}\n")
    print(f"{'Target':<20} {'Average consumption':<20} {'Maximum consumption':<20} {'Minimum consumption':<20}")
    print("=" * 80)

    total = {'avg': 0, 'max': 0, 'min': 0}
    for target, values in stats.items():
        if target != 'global':
            print(f"{target:<20} {values['avg']:<20.2f} {values['max']:<20.2f} {values['min']:<20.2f}")
        else:
            total = values

    print("-" * 80)
    print(f"{'Global':<20} {total['avg']:<20.2f} {total['max']:<20.2f} {total['min']:<20.2f}")


def start_pretty_print():
    """
    Pretty print the CPU and DRAM power consumption statistics from CSV files.
    """
    print("The consumptions are given in Watt, note that the precision depends on the configuration file\n")

    data = load_csv_files_from_directory()

    # Calculate and print CPU statistics
    cpu_stats = compute_statistics(data, 'cpu')
    print_statistics(cpu_stats, "CPU Consumption Statistics :")

    # Calculate and print DRAM statistics
    dram_stats = compute_statistics(data, 'dram')
    print_statistics(dram_stats, "DRAM Consumption Statistics :")

    # Could add the GPU statistics here

    print("\nFor more precise evaluation, consult the PowerAPI documentation to adjust configurations.\n")


def find_cpu(data):
    """
    Find the cpu in the list of compatible cpu
    """
    option = []
    line = "cat /proc/cpuinfo | grep 'model name'"
    result = subprocess.check_output(line, shell=True, text=True).split("\n")
    print("The CPU found is" + result[0].split(":")[1])
    parse = parse_processor_name(result[0])
    for row in data:
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
    """
    Parse the processor name to extract the id and the brand
    :param name: Name of the processor, extracted from /proc/cpuinfo
    :return: id adn brand of the processor
    """
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
    cpu = find_cpu(load_cpus_information())

    print("\nSetting up configuration files...")
    print("-" * 80)
    # Update core events in the sensor configuration
    # file based on the selected processor architecture
    with open('sensor/hwpc-mongodb.json', encoding='UTF-8') as hwpc_sensor_configuration_file:
        sensor_configuration = json.load(hwpc_sensor_configuration_file)

    if cpu["Family"] in architectures_table[0]:
        sensor_configuration['container']['core']['events'] = [
            "CPU_CLK_UNHALTED:REF_P",
            "CPU_CLK_UNHALTED:THREAD_P",
            "LLC_MISSES",
            "INSTRUCTIONS_RETIRED"
        ]
    elif cpu["Family"] in architectures_table[1]:
        sensor_configuration['container']['core']['events'] = [
            "CPU_CLK_THREAD_UNHALTED:REF_P",
            "CPU_CLK_THREAD_UNHALTED:THREAD_P",
            "LLC_MISSES",
            "INSTRUCTIONS_RETIRED"
        ]
    elif cpu["Family"] in architectures_table[2]:
        sensor_configuration['container']['core']['events'] = [
            "CYCLES_NOT_IN_HALT",
            "RETIRED_INSTRUCTIONS",
            "RETIRED_UOPS"
        ]
    elif cpu["Family"] in architectures_table[3]:
        sensor_configuration['container']['core']['events'] = [
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
        sensor_configuration["cgroup_basepath"] = "/sys/fs/cgroup/"
    else:
        sensor_configuration["cgroup_basepath"] = "/sys/fs/cgroup/perf_event"

    print("cgroup version updated")

    with open('sensor/hwpc-mongodb.json', 'w', encoding='UTF-8') as hwpc_sensor_configuration_file:
        json.dump(sensor_configuration, hwpc_sensor_configuration_file, indent=4)

    # Update parameters in the formula configuration
    with open('formula/smartwatts-mongodb-csv.json', encoding='UTF-8') as smartwatts_configuration_file:
        formula_config = json.load(smartwatts_configuration_file)

    if cpu["Base frequency"] != '':
        formula_config["cpu-base-freq"] = int(float(cpu["Base frequency"])*1000)
    print("Base frequency updated")

    if cpu["TDP"] != '':
        formula_config["cpu-tdp"] = int(cpu["TDP"][:-1])
    print("TDP updated\n")

    with open('formula/smartwatts-mongodb-csv.json', 'w', encoding='UTF-8') as smartwatts_configuration_file:
        json.dump(formula_config, smartwatts_configuration_file, indent=4)

    print("Please enter the number of second you want the demo to run for (minimum 30) or exit to quit:")
    waiting_for_execution_time = True
    while waiting_for_execution_time:
        try:
            execution_time = input()
            execution_time = int(execution_time)
            if execution_time < 30:
                print("Invalid input, please enter a valid number or exit to quit")
            else:
                waiting_for_execution_time = False
        except ValueError:
            if execution_time == "exit":
                print("Exiting...")
                sys.exit()
            else:
                print("Invalid input, please enter a valid number or exit to quit")

    print("\nStarting the demo...")
    print("-" * 80)
    print("The demo will run for " + str(execution_time) + " seconds\n")
    print("If you wish to stop it, Ctrl-C will do so and stop the docker compose stack\n")

    start_docker_compose(execution_time)

    verification = 0

    # Get all the csv power report in the csv directory
    for root, _, files in os.walk(csv_directory_path):
        for filename in files:
            if filename.endswith('.csv'):
                verification += 1
                file_path = os.path.join(root, filename)
                print("\nThe power report is available at: " + file_path)

    if verification == 0:
        print("\nNo power report available, "
              "please check the configuration file "
              "and the sensor availability for your "
              "processor architecture\n")
    else:
        print("\nThe demo has ended, "
              "you can see the result under the /csv directory, but"
              " here is a quick summary\n")

    start_pretty_print()


if __name__ == '__main__':
    start_demo()
