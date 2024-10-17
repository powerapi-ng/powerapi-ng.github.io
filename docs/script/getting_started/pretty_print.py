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


def start_pretty_print():
    """
    Pretty print the result of the demo by parsing the csv files,
    then proceed to calculate the average, maximum, and minimum consumption
    and print them in a table format
    """
    data = []
    result = [["Cgroup",
               "Average consumption",
               "Maximum consumption",
               "Minimum consumption"]]

    print("\nThe consumptions are given in Watt, "
          "note that the precision depend on the value given in the "
          "configuration file (the base CPU frequency, the CPU TDP, ...) \n")

    # Get all the csv power report in the csv directory
    for root, _, files in os.walk('./csv'):
        for filename in files:
            if filename.endswith('.csv'):
                file_path = os.path.join(root, filename)

                with open(file_path, mode='r', newline='', encoding='UTF-8') as f:
                    for row in csv.DictReader(f):
                        data.append(row)

    cgroup_data = {}
    total = [0, 0, 0]
    # We remove rapl, but it's still available in the csv files
    for row in data:
        target = row['target']
        consumption = float(row['power'])

        if target not in cgroup_data and not target == 'rapl':
            cgroup_data[target] = []

        if not target == 'rapl':
            cgroup_data[target].append(consumption)

    for target, consumptions in cgroup_data.items():
        avg_consumption = sum(consumptions) / len(consumptions)
        max_consumption = max(consumptions)
        min_consumption = min(consumptions)

        if not target == 'global':
            result.append([target,
                           f"{avg_consumption:.2f}",
                           f"{max_consumption:.2f}",
                           f"{min_consumption:.2f}"])
        else:
            total = [avg_consumption, max_consumption, min_consumption]

    print(f"{'Target':<20} "
          f"{'Average consumption':<20} "
          f"{'Maximum consumption':<20} "
          f"{'Minimum consumption':<20}")
    print("=" * 80)

    for row in result[1:]:
        print(f"{row[0]:<20} {row[1]:<20} {row[2]:<20} {row[3]:<20}")

    print("=" * 80)
    print(f"{'Global':<20} "
          f"{total[0]:<20.2f} "
          f"{total[1]:<20.2f} "
          f"{total[2]:<20.2f}")

    print("\nIf you want to get a more precise evaluation, "
          "we encourage you to read the documentation of PowerAPI "
          "and adapt the sensor/formula configuration file in consequence \n")


if __name__ == '__main__':
    start_pretty_print()
