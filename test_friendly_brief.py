import os, csv
from collections import defaultdict
from functools import partial

import nose.tools as n

import friendly_brief as f

with open(os.path.join('fixtures', 'brief_number.csv')) as fp:
    reader = csv.reader(fp)
    next(reader) # burn header
    cases_brief_number = list(reader)

with open(os.path.join('fixtures', 'amici.csv')) as fp:
    reader = csv.reader(fp)
    next(reader) # burn header
    cases_amici = defaultdict(lambda:set())
    for brief, amicus in reader:
        cases_amici[brief].add(amicus)
    cases_amici = list(cases_amici.items())

with open(os.path.join('fixtures', 'posture.csv')) as fp:
    reader = csv.reader(fp)
    next(reader) # burn header
    cases_posture = list(reader)

def check_amici(brief, expectation):
    observation = f.amici(brief)
    for expected_amicus in expectation:
        for observed_amicus in observation:
            if expected_amicus.lower() in observed_amicus.lower():
                break
        else:
            raise AssertionError('The expected amicus "%s" could not be found.' % expected_amicus)

def check_brief_number(brief, expectation):
    n.assert_equal(f.brief_number(brief), int(expectation))

def check_posture(brief, expectation):
    n.assert_equal(f.posture(brief), int(expectation))

def test():
    for checker, cases in [
        (check_amici, cases_amici),
        (check_brief_number, cases_brief_number),
        (check_posture, cases_posture),
    ]:
        for brief, expectation in cases:
            yield checker, brief, expectation
