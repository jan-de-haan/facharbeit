import requests
import json
import argparse
import itertools

SERVER_URL = "http://192.168.10.2"

def measure():
    requests.post(SERVER_URL + "/accelerometer/start-measurement?duration="
                  + str(ARGS.duration))

def review():
    available_datasets = json.loads(requests.get(SERVER_URL + "/accelerometer/datasets").text)
    for i, dataset in zip(itertools.count(), available_datasets):
        print("(" + str(i) + ") " + dataset)

    selected_index = input("Which dataset would you like to review? ")
    selected_dataset = available_datasets[int(selected_index)]

    dataset = requests.get(SERVER_URL + "/accelerometer/datasets/" + selected_dataset).text
    pretty_print_dataset(dataset)

def pretty_print_dataset(dataset):
    acc_x = []
    acc_y = []
    acc_z = []
    for line in iter(dataset.splitlines()):
        values = line.split(",")
        t = int(values[0])
        acc_x.append((t, float(values[1])))
        acc_y.append((t, float(values[2])))
        acc_z.append((t, float(values[3])))

    print("a_x:")
    print(graph(acc_x))
    input("")
    print("a_y:")
    print(graph(acc_y))
    input("")
    print("a_y:")
    print(graph(acc_y))

def graph(xy_pairs):
    width = 80
    height = 24
    left_margin = 4
    bottom_margin = 1

    x_axis_max = max([i[0] for i in xy_pairs])
    x_axis_min = min([i[0] for i in xy_pairs])
    y_axis_max = max([i[1] for i in xy_pairs])
    y_axis_min = min([i[1] for i in xy_pairs])

    screen = []
    for i in range(0, height):
        row = []
        for j in range(0, width):
            row.append(' ')
        screen.append(row)

    for i in range(left_margin, width - 1):
        screen[bottom_margin][i] = '-'
    for i in range(bottom_margin + 1, height - 1):
        screen[i][left_margin] = '|'

    screen[bottom_margin][left_margin] = '+'
    screen[0][left_margin] = '0'
    screen[bottom_margin][width - 1] = '+'
    label_end = str(x_axis_max)
    for i, j in zip(range(width - len(label_end), width), range(0, len(label_end))):
        screen[0][i] = label_end[j]

    label_y_0 = format(y_axis_min, ".2f")
    for i in range(0, left_margin - 1):
        screen[1][i] = label_y_0[i]
    screen[height - 1][left_margin] = '+'
    label_y_1 = format(y_axis_max, ".2f")
    for i in range(0, left_margin - 1):
        screen[height - 1][i] = label_y_1[i]

    x_range = x_axis_max - x_axis_min
    y_range = y_axis_max - y_axis_min
    for xy_pair in xy_pairs:
        x_pos = round(xy_pair[0] * ((width - left_margin) / x_range)) + bottom_margin + 1
        y_pos = round((xy_pair[1] - y_axis_min) * ((height - bottom_margin - 1) / y_range)) + left_margin + 1
        if x_pos < width and x_pos > left_margin and y_pos < height and y_pos > bottom_margin:
            screen[y_pos][x_pos] = 'x'

    final_str = ""
    screen.reverse()
    for row in screen:
        final_str += "".join(row) + "\n"

    return final_str


PARSER = argparse.ArgumentParser(description="Communicate with the accelerometer")

PARSER.add_argument("--measure", dest="action", action="store_const", const=measure, default=review, help="Start a measurement")
PARSER.add_argument("duration", type=int, nargs="?", default=1000, metavar="DURATION", help="The duration of the measurement to be started in milliseconds")
PARSER.add_argument("--review", dest="action", action="store_const", const=review, help="Choose an existing dataset to review")

ARGS = PARSER.parse_args()
ARGS.action()
