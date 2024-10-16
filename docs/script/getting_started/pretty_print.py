import csv
import os


def start_pretty_print():
    """
    Pretty print the result of the demo by parsing the csv files of each cgroup,
    then proceed to calculate the average, maximum, and minimum consumption of each cgroup
    and print them in a table format
    """
    data = []
    result = [["Cgroup", "Average consumption", "Maximum consumption", "Minimum consumption"]]

    directory = './csv'

    print("The consumption are given in Watt, note that the precision depend on the value given in the configuration file (the base CPU frequence, the CPU TDP, ...) ")

    # Get all the csv power report in the csv directory
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.csv'):
                file_path = os.path.join(dirpath, filename)

                with open(file_path, mode='r', newline='') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        data.append(row)

    cgroup_data = {}

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

        result.append([target, f"{avg_consumption:.2f}", f"{max_consumption:.2f}", f"{min_consumption:.2f}"])

    print(f"{'Cgroup':<20} {'Average consumption':<20} {'Maximum consumption':<20} {'Minimum consumption':<20}")
    print("=" * 80)

    for row in result[1:]:
        print(f"{row[0]:<20} {row[1]:<20} {row[2]:<20} {row[3]:<20}")


if __name__ == '__main__':
    start_pretty_print()
