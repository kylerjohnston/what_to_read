#!/usr/bin/env python3
""" Randomly select books from a "Want to Read" Goodreads shelf """

import argparse
import csv
import random
from datetime import datetime

SHELF_FILTER = 'to-read'
DATE_FORMAT = '%Y/%m/%d'
TODAY = datetime.today()

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
    parser.add_argument('--include-read', action='store_true',
                        help='Include books that have already been read and rated 4 or 5 stars in results')
    parser.add_argument('--century', nargs=1, type=int, default=0)
    parser.add_argument('--recent-adds', action='store_true',
                        help='Prioritize titles added in the last 3 months')
    parser.add_argument('--recent-pubs', action='store_true',
                        help='Prioritize titles added in the last 2 years')
    parser.add_argument('-n', type=int, default=10,
                        help='How many to sample')
    args = parser.parse_args()
    include_read = args.include_read
    century = args.century
    num_choices = args.n
    csv_path = args.csv
    recent_adds = args.recent_adds
    recent_pubs = args.recent_pubs

    if 'century' != 0:
            start_year = (century - 1) * 100
            end_year = start_year + 99
    else:
        start_year = 0
        end_year = 9999

    with open(csv_path) as csv_body:
        reader = csv.DictReader(csv_body)
        to_read = []
        read = []
        in_year_range = []
        for row in reader:
            if SHELF_FILTER in row['Bookshelves']:
                to_read.append(row)
                date_added = datetime.strptime(row['Date Added'], DATE_FORMAT)
                delta = TODAY - date_added
                # make things added in the last three months twice as likely
                if recent_adds and delta.days < 90:
                    to_read.append(row)
                if recent_pubs and delta.days < (365 * 2):
                    to_read.append(row)
            if row['Exclusive Shelf'] == 'read' and row['My Rating'] in ('4', '5'):
                read.append(row)

        choices = to_read
        if include_read:
            choices += read

        if century > 0:
            new_choices = []
            for row in choices:
                pub_date = row['Original Publication Year']
                if pub_date == '':
                    pub_date = '0'
                pub_date = int(pub_date)
                if start_year <= pub_date <= end_year:
                    new_choices.append(row)
            choices = new_choices

        random.shuffle(choices)
        start = 0
        end = num_choices
        while True:
            print_selections(choices[start:end])
            result = input('Load more? [y/n]: ')
            if result == 'y':
                start += num_choices
                end += num_choices
            else:
                return


if __name__ == '__main__':
    main()
