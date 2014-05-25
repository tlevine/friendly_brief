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
    if len(observation) < len(expectation): # - 1: # Failures at non-Oxford comma are okay.
        msg = 'The amici were not broken up enough; only %d amici were reported, but there are supposed to be %d:\n' + '\n* '.join(observation)
        raise AssertionError(msg % lengths)
    if len(observation) > len(expectation) + 1:
        msg = 'The amici were too broken up; %d amici were reported, but there are only supposed to be %d:\n' + '\n* '.join(observation)
        raise AssertionError(msg % lengths)

    for observed_amicus in observation:
        n.assert_less(len(observed_amicus), 60, msg = observation)

def check_amici_sans_brief(brief, _):
    for observed_amicus in f.amici(brief):
       n.assert_not_in('brief', observed_amicus.lower())

def check_amici_sans_startswith_junk(brief, _):
    for junk in ['for ', 'amic', 'jr', 'of ', 'and ']:
        for observed_amicus in f.amici(brief):
           n.assert_false(observed_amicus.lower().startswith(junk), msg = observed_amicus)
    for junk in [' as']:
        for observed_amicus in f.amici(brief):
           n.assert_false(observed_amicus.lower().endswith(junk), msg = observed_amicus)

def check_amici_sans_literal_junk(brief, _):
    for junk in ['', 'et al.', 'as','l.l.c.']:
         for observed_amicus in f.amici(brief):
            n.assert_not_equal(junk, observed_amicus.lower())

def check_brief_number(brief, expectation):
    n.assert_equal(f.brief_number(brief), int(expectation))

def check_posture(brief, expectation):
    n.assert_equal(str(f.posture(brief)), expectation)

def test():
    for checker, cases in [
        (check_amici, cases_amici),
        (check_amici_sans_brief, cases_amici),
        (check_amici_sans_literal_junk, cases_amici),
        (check_amici_sans_startswith_junk, cases_amici),
        (check_brief_number, cases_brief_number),
        (check_posture, cases_posture),
    ]:
        for brief, expectation in cases:
            yield checker, brief, expectation

def test_remove_date():
    observation = f._remove_date("19.    Amicus Brief, BRIEF FOR AMICI CURIAE ADULT PRE-ICWA INDIAN ADOPTEES SUPPORTING BIRTH FATHER AND THE CHEROKEE NATION, March 28, 2013, 2013 U.S. S. Ct. Briefs  1711")
    expectation = "19.    Amicus Brief, BRIEF FOR AMICI CURIAE ADULT PRE-ICWA INDIAN ADOPTEES SUPPORTING BIRTH FATHER AND THE CHEROKEE NATION"
    n.assert_equal(observation, expectation)

def test_empty_brief():
    n.assert_list_equal(f.amici(''), [])
    n.assert_equal(f.brief_number(''), '')
    n.assert_equal(f.posture(''), '')
