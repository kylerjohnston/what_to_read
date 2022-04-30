#!/usr/bin/env python3
""" Randomly select 10 books from a "Want to Read" Goodreads shelf """

import argparse
import csv
import random

SHELF_FILTER = 'to-read'

def print_selections(selections):
    """ Format and print selections """
    for row in selections:
        print('=' * 80)
        print('Title:  ' + row['Title'])
        print('Author: ' + row['Author'])
        print('Year:   ' + row['Original Publication Year'])
        print('Link:   ' + 'https://www.goodreads.com/book/show/' + row['Book Id'])
        print('=' * 80)
        print('')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv', type=str,
                        help='Path to Goodreads library CSV export')
    parser.add_argument('-n', type=int, default=10,
                        help='How many to sample')
    args = parser.parse_args()
    num_choices = args.n
    csv_path = args.csv

    with open(csv_path) as csv_body:
        reader = csv.DictReader(csv_body)
        to_read = [row for row in reader if SHELF_FILTER in row['Bookshelves']]
        selections = random.choices(to_read, k=num_choices)
        print_selections(selections)

if __name__ == '__main__':
    main()
