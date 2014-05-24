import os, csv
from collections import defaultdict
from functools import partial

import nose.tools as n

import friendly_brief as f

with open(os.path.join('fixtures', 'amici.csv')) as fp:
    reader = csv.reader(fp)
    next(reader) # burn header
    cases_posture = defaultdict(lambda:set())
    for brief, amicus in reader:
        cases_posture[brief].add(amicus)
    cases_posture = list(cases_posture.items()`)

with open(os.path.join('fixtures', 'posture.csv')) as fp:
    reader = csv.reader(fp)
    next(reader) # burn header
    cases_posture = list(reader)

def run_test(checker, cases):
    for brief, expectation in cases:
        yield checker, brief, expectation

def check_amici(brief, expectation):
    observation = f.amici(brief)
    for expected_amicus in expectation:
        for observed_amicus in observation:
            if expected_amicus in observed_amicus:
                break
        else:
            raise AssertionError('The expected amicus "%s" could not be found.' % expected_amicus)

def check_brief_number(brief, expectation):
    n.assert_equal(f.brief_number(brief), expectation)

def check_posture():

test_amici = partial(run_test, check_amici, cases_amici)
test_brief_number = partial(run_test, check_brief_number, cases_brief_number)
test_posture = partial(run_test, check_posture, cases_posture)
