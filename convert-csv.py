import csv
import os
from glob import glob

def convert_csv(infile, outfile):
    converted_csv = []

    with open(infile, mode="r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar='"')
        for row in reader:
            converted_row = []
            for cell in row:
                converted_row.append(cell.replace(",", "."))
            converted_csv.append(converted_row)

    with open(outfile, mode="w") as csvfile:
        writer = csv.writer(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in converted_csv:
            writer.writerow(row)

csvfilepaths = [y for x in os.walk("./") for y in glob(os.path.join(x[0], '*.csv'))]

for path in csvfilepaths:
    convert_csv(path, path)

