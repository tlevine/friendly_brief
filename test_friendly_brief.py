import nose.tools as n

from friendly_brief import amicus

testcases = [
    ("2.    Brief, BRIEF AMICUS CURIAE OF THE GEORGIA ASSOCIATION OF BLACK ELECTED OFFICIALS IN SUPPORT OF APPELLANTS, July 19, 1996", ['THE GEORGIA ASSOCIATION OF BLACK ELECTED OFFICIALS']),
]

def check_amicus(brief, expectation):
    observation = amicus(brief)
    n.assert_list_equal(observation, expectation)

def test_amicus():
    for brief, expectation in testcases:
        yield check_amicus, brief, expectation
