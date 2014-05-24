import os, csv
import re
from collections import defaultdict
from functools import partial
from pprint import pformat

import nose.tools as n

import friendly_brief.read as f

FIXTURES = os.path.join('friendly_brief', 'test', 'fixtures')

with open(os.path.join(FIXTURES, 'brief_number.csv')) as fp:
    reader = csv.reader(fp)
    next(reader) # burn header
    cases_brief_number = list(reader)

with open(os.path.join(FIXTURES, 'amici.csv')) as fp:
    reader = csv.reader(fp)
    next(reader) # burn header
    cases_amici = defaultdict(lambda:set())
    for brief, amicus in reader:
        cases_amici[brief].add(amicus)
    cases_amici = list(cases_amici.items())

with open(os.path.join(FIXTURES, 'posture.csv')) as fp:
    reader = csv.reader(fp)
    next(reader) # burn header
    cases_posture = list(reader)

def check_amici(brief, expectation):
    def standardize(nonstandard:str) -> str:
        return re.sub(r'[ .]', '', nonstandard.strip().lower())
    observation = list(f.amici(brief))
    for expected_amicus in expectation:
        for observed_amicus in observation:
            if standardize(expected_amicus) in standardize(observed_amicus):
                break
        else:
            msg = '''The expected amicus "%s" should be found in the following brief.

    %s

But it is not among the following values output from the amici function.

    %s'''
            raise AssertionError(msg % (expected_amicus, brief, pformat(observation)))
    lengths = (len(observation), len(expectation))
    if len(observation) < len(expectation):
        msg = 'The amici were not broken up enough; only %d amici were reported, but there are supposed to be %d:\n' + '\n* '.join(observation)
        raise AssertionError(msg % lengths)
    if len(observation) > len(expectation) + 1:
        msg = 'The amici were too broken up; %d amici were reported, but there are only supposed to be %d:\n' + '\n* '.join(observation)
        raise AssertionError(msg % lengths)

def check_brief_number(brief, expectation):
    n.assert_equal(f.brief_number(brief), int(expectation))

def check_posture(brief, expectation):
    n.assert_equal(str(f.posture(brief)), expectation)

def test():
    for checker, cases in [
        (check_amici, cases_amici),
        (check_brief_number, cases_brief_number),
        (check_posture, cases_posture),
    ]:
        for brief, expectation in cases:
            yield checker, brief, expectation
