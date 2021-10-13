#!/usr/bin/env python3

import csv
import sys


# USAGE
# modify training_years and testing_years as needed
# ./extract_training.py RAW_DATA.csv TRAINING_DATA.csv TESTING_DATA.csv

def main():
    in_file_name = sys.argv[1]
    training_file_name = sys.argv[2]
    testing_file_name = sys.argv[3]

    training_years = [2015, 2016, 2017, 2018] # change this if you need diff years
    testing_years = [2019] # change this if you need diff years

    with open(in_file_name) as in_file, \
            open(training_file_name, 'a') as training_file, \
            open(testing_file_name, 'a') as testing_file:
        csv_input = csv.reader(in_file)
        for index, row in enumerate(csv_input):
            if index == 0:
                csv.writer(training_file).writerow(row)
                csv.writer(testing_file).writerow(row)
                continue
            if not len(row):
                continue
            if int(row[1]) in training_years:
                csv.writer(training_file).writerow(row)
            elif int(row[1]) in testing_years:
                csv.writer(testing_file).writerow(row)

if __name__ == '__main__':
    main()
