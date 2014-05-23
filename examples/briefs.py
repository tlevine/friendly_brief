#!/usr/bin/env python3
import csv
import sys

from friendly_brief import amicus

reader = csv.reader(open('briefs.csv', 'r'))
writer = csv.writer(sys.stdout)

# Header
writer.writerow(next(reader))

for row in reader:
    number, case, brief, posture = row
    for friend in amicus(brief):
        writer.writerow((number, case, friend, posture))
