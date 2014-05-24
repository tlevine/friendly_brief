import os, csv, json
from functools import partial

import nose.tools as n

import friendly_brief as f

with open(os.path.join('fixtures', 'amici.json')) as fp:
    cases_amici = json.load(fp)

with open(os.path.join('fixtures', 'posture.csv')) as fp:
    reader = csv.reader(fp)
    next(reader) # burn header
    cases_posture = list(reader)

def run_test(checker, cases):
    for brief, expectation in cases:
        yield checker, brief, expectation

def check_amici(brief, expectation):
    def standard(xs):
        return [x.lower() for x in sorted(xs)]
    observation = f.amici(brief)
    n.assert_list_equal(standard(observation), standard(expectation))

def check_brief_number(brief, expectation):
    n.assert_equal(f.brief_number(brief), expectation)

def check_posture():

test_amici = partial(run_test, check_amici, cases_amici)
test_brief_number = partial(run_test, check_brief_number, cases_brief_number)
test_posture = partial(run_test, check_posture, cases_posture)
