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

import csv
import os


def load_data(directory='./csv'):
    """
    Load CSV files from the specified directory and return the data as a list of dictionaries.
    """
    data = []
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.csv'):
                file_path = os.path.join(root, filename)
                with open(file_path, mode='r', newline='', encoding='UTF-8') as f:
                    data.extend(csv.DictReader(f))
    return data


def calculate_statistics(data, scope):
    """
    Calculate average, maximum, and minimum consumption for the given scope (cpu or dram).
    """
    stats = {}
    for row in data:
        if row['scope'] == scope and row['target'] != 'rapl':
            target = row['target']
            consumption = float(row['power'])
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

    data = load_data()

    # Calculate and print CPU statistics
    cpu_stats = calculate_statistics(data, 'cpu')
    print_statistics(cpu_stats, "CPU Consumption Statistics :")

    # Calculate and print DRAM statistics
    dram_stats = calculate_statistics(data, 'dram')
    print_statistics(dram_stats, "DRAM Consumption Statistics :")

    # Could add the GPU statistics here

    print("\nFor more precise evaluation, consult the PowerAPI documentation to adjust configurations.\n")


if __name__ == '__main__':
    start_pretty_print()
