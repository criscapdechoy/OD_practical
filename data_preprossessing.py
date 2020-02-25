"""
Cristina Capdevila Choy, February 2020
"""
# !/usr/bin/python3
import pandas as pd
import os
import json
import csv
import sys


# Global variables to control script flow
input_default_path = "data/breastcancer.json"
tmp_path = "tmp"



##
# Convert to string keeping encoding in mind...
##
def to_string(s):
    try:
        return str(s)
    except:
        # Change the encoding type if needed
        return s.encode('utf-8')


def reduce_item(key, value):
    global reduced_item

    # Reduction Condition 1
    if type(value) is list:
        i = 0
        for sub_item in value:
            reduce_item(key , sub_item)
            i = i + 1

    # Reduction Condition 2
    elif type(value) is dict:
        sub_keys = value.keys()
        for sub_key in sub_keys:
            reduce_item(key + '_' + to_string(sub_key), value[sub_key])

    # Base Condition
    else:
        reduced_item[to_string(key)] = to_string(value)


def JSON_to_CSV(inputdir, outputfile):
    # Reading arguments
    node = 'result'
    json_file_path = inputdir
    csv_file_path = outputfile

    fp = open(json_file_path, 'r')
    json_value = fp.read()
    raw_data = json.loads(json_value)
    fp.close()

    data_to_be_processed = raw_data[node]['hits']['hit']


    processed_data = []
    header = []
    for item in data_to_be_processed:
        global reduced_item

        reduced_item = {}
        reduce_item(node, item)

        header += reduced_item.keys()

        processed_data.append(reduced_item)

    header = list(set(header))
    header.sort()

    with open(csv_file_path, 'w+') as f:
        writer = csv.DictWriter(f, header, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for row in processed_data:
            writer.writerow(row)

    print("Just completed writing csv file with %d columns" % len(header))


if __name__ == "__main__":
    inputdir = input_default_path
    # Assign output file for output CSV
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)
        print(f"[INFO] Created a new folder {tmp_path}")
    # Evaluation output file config
    head, tail = os.path.split(inputdir)
    tail = '.'.join((tail.split('.')[0], 'csv'))
    outputfile = f"{head}/{tail}"
    print(outputfile)
    if os.path.exists(outputfile):
        os.remove(outputfile)
        print(f"{outputfile} file removed")
    # Run CSV to json
    JSON_to_CSV(inputdir, outputfile)
