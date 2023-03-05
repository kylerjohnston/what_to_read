#!/usr/bin/env python3
""" Analyze reading habits """

import csv
import argparse
import matplotlib.pyplot as plt
import numpy as np
from math import floor

def pub_year_analysis(tbl):
    # Year of publication
    by_year = {}
    for row in tbl:
        pub_year = int(row['Pub year'])
        if pub_year in by_year.keys():
            by_year[pub_year].append(row)
        else:
            by_year[pub_year] = [row]
    years = [x for x in by_year.keys()]
    years.sort()
    min_year = years[0]
    max_year = years[-1]
    all_years = [x for x in range(min_year, max_year + 1)]
    count = []
    for year in all_years:
        if year in by_year.keys():
            count.append(len(by_year[year]))
        else:
            count.append(0)

    cc = count.copy()
    cc.sort()
    min_count = cc[0]
    max_count = cc[-1]
    fig, ax = plt.subplots()
    ax.bar(all_years, count, width=1, edgecolor="white", linewidth=1)
    ax.set_xlabel('Publication year')
    ax.set_ylabel('Count')
    ax.set_title('Books read by publication year')
    ax.set(xlim=(all_years[0] - 2, all_years[-1] + 2),
           xticks=[x for x in all_years if x % 5 == 0],
           yticks=[min_count, max_count])
    ax.annotate('Sense and Sensibility',
                xy=(1811, 1),
                xytext=(1821, 1.3),
                arrowprops=dict(facecolor='black', shrink=0.05))
    ax.annotate('Lapvona',
                xy=(2022, 1),
                xytext=(2012, 1.4),
                arrowprops=dict(facecolor='black', shrink=0.05))
    ax.annotate('Appointment in Samarra',
                xy=(1934, 1),
                xytext=(1944, 1.2),
                arrowprops=dict(facecolor='black', shrink=0.05))
    plt.show()


def pub_decade_analysis(tbl):
    # Year of publication
    by_decade = {}
    for row in tbl:
        pub_decade = floor(int(row['Pub year']) / 10)
        if pub_decade in by_decade.keys():
            by_decade[pub_decade].append(row)
        else:
            by_decade[pub_decade] = [row]
    decades = [x for x in by_decade.keys()]
    decades.sort()
    min_decade = decades[0]
    max_decade = decades[-1]
    all_decades = [x for x in range(min_decade, max_decade + 1)]
    count = []
    for decade in all_decades:
        if decade in by_decade.keys():
            count.append(len(by_decade[decade]))
        else:
            count.append(0)

    cc = count.copy()
    cc.sort()
    min_count = cc[0]
    max_count = cc[-1]
    fig, ax = plt.subplots()
    all_decades_full = [x * 10 for x in all_decades]
    all_decades_offset = [x + 5 for x in all_decades_full]
    ax.bar(all_decades_offset, count, width=10, edgecolor="white", linewidth=1)
    ax.set_xlabel('Publication decade')
    ax.set_ylabel('Count')
    ax.set_title('Books read by publication decade')
    ax.set(xlim=(all_decades_full[0] - 10, all_decades_full[-1] + 20),
           xticks=all_decades_full,
           yticks=range(min_count, max_count + 1))
    plt.show()


def by_field(tbl, field):
    by_field = {}
    for row in tbl:
        value = row[field]
        if value in by_field.keys():
            by_field[value].append(row)
        else:
            by_field[value] = [row]
    values = [x for x in by_field.keys()]
    count = [len(by_field[x]) for x in values]
    fig, ax = plt.subplots()
    ax.bar(values, count, width=1, edgecolor="white", linewidth=1)
    ax.set_xlabel(field)
    ax.set_ylabel('Count')
    ax.set_title(f'Books read by {field.lower()}')
    plt.show()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv', type=str,
                        help='Path to reading habits csv')
    args = parser.parse_args()
    csv_path = args.csv

    input_file = csv.DictReader(open(csv_path, mode='r'))
    tbl = [x for x in input_file]

    #pub_decade_analysis(tbl)
    #by_field(tbl, 'Gender')
    #by_field(tbl, 'Country')
    by_field(tbl, 'Format')

if __name__ == '__main__':
    main()
