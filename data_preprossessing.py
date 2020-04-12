"""
Cristina Capdevila Choy, February 2020
"""
# !/usr/bin/python3
import pandas as pd
import os
import json
import csv
import sys

input_file_path = 'data/breastcancer.json'


def JSON_to_CSV(inputdir, outputfile):
    node = 'result'
    json_file_path = inputdir
    csv_file_path = outputfile

    fp = open(json_file_path, 'r')
    json_value = fp.read()
    raw_data = json.loads(json_value)
    fp.close()

    data_to_be_processed = raw_data[node]['hits']['hit']
    df = pd.json_normalize(data_to_be_processed, max_level=2)
    for i in range(len(df)):
        if type(df['info.authors.author'][i]) != type(list()):
            df['info.authors.author'][i] = [df['info.authors.author'][i]]
    df = df.rename(columns={"@score":"score","@id":"id","url":"url_num","info.authors.author":"author","info.title":"title",
                       "info.year":"year","info.type":"pub_type","info.key":"key","info.ee":"ee","info.url":"url",
                       "info.venue":"venue","info.volume":"vol","info.number":"num","info.pages":"pages",
                       "info.doi":"doi", "info.publisher":"publisher"
                       })
    df = df.fillna("Null")
    df.to_csv(csv_file_path)


if __name__ == "__main__":
    inputdir = input_file_path

    # Assign output file for output CSV
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
