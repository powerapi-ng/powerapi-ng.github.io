

import sys
from subprocess import call
import subprocess
import json

# List of available processor architectures Template: "n - Arch name"
# If an arch is added, the case statement in the
# start_demo function should be updated accordingly with the proper core events
# https://powerapi.org/reference/sensors/hwpc-sensor/
list_arch = ["0 - Intel Sandy Bridge, Comet Lake",
             "1 - Intel Skylake, Whiskey Lake, Coffee Lake",
             "2 - AMD Zen 2",
             "3 - AMD Zen 3"]


def start_demo():
    """
    Start the demo by selecting the processor architecture
    this will update the sensor configuration file
    """
    print("Enter the number associated with your processor architecture, "
          "please note that the sensor isn't available "
          "for Intel Tiger Lake and newer: \n" + list_arch[0] +
          "\n" + list_arch[1] +
          "\n" + list_arch[2] +
          "\n" + list_arch[3] +
          "\n")

    choice = True
    while choice:
        try:
            val = input()
            val = int(val)
            if val < 0 or val >= len(list_arch):
                print("Invalid input, please enter a valid number or exit")
            else:
                choice = False
        except ValueError:
            if val == "exit":
                print("Exiting...")
                sys.exit()
            else:
                print("Invalid input, please enter a valid number or exit")

    print("You have selected: " + list_arch[val] + "\n")

    # Update core events in the sensor configuration
    # file based on the selected processor architecture
    with open('sensor/hwpc-mongodb.json', encoding='UTF-8') as f:
        data = json.load(f)

    if val == 0:
        data['container']['core']['events'] = [
            "CPU_CLK_UNHALTED:REF_P",
            "CPU_CLK_UNHALTED:THREAD_P",
            "LLC_MISSES",
            "INSTRUCTIONS_RETIRED"
        ]
    elif val == 1:
        data['container']['core']['events'] = [
            "CPU_CLK_THREAD_UNHALTED:REF_P",
            "CPU_CLK_THREAD_UNHALTED:THREAD_P",
            "LLC_MISSES",
            "INSTRUCTIONS_RETIRED"
        ]
    elif val == 2:
        data['container']['core']['events'] = [
            "CYCLES_NOT_IN_HALT",
            "RETIRED_INSTRUCTIONS",
            "RETIRED_UOPS"
        ]
    elif val == 3:
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
    print(cgroup.stdout)
    if cgroup.stdout == "cgroup2fs\n":
        data["cgroup_basepath"] = "/sys/fs/cgroup/"
    else:
        data["cgroup_basepath"] = "/sys/fs/cgroup/perf_event"

    print("Cgroup version updated")

    with open('sensor/hwpc-mongodb.json', 'w', encoding='UTF-8') as f:
        json.dump(data, f, indent=4)

    print("Starting the demo...")

    call("./start.sh")

    print("The demo has ended, "
          "you can see the result under the /csv directory"
          " or use 'python3 pretty_print.py' "
          "to get a quick summary of the result in the terminal")


if __name__ == '__main__':
    start_demo()
