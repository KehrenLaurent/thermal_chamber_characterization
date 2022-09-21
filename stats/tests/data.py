import csv
import os


def read_file():
    with open('stats/tests/data_set.csv', 'r', encoding='utf-8') as f:
        r = csv.reader(f, delimiter=";")
        return [l for l in r]