import nose.tools as n

from friendly_brief import amicus

testcases = [
    ("2.    Brief, BRIEF AMICUS CURIAE OF THE GEORGIA ASSOCIATION OF BLACK ELECTED OFFICIALS IN SUPPORT OF APPELLANTS, July 19, 1996", ['THE GEORGIA ASSOCIATION OF BLACK ELECTED OFFICIALS']),
    ("2.       Brief of amici Curiae, The Sikh Coalition, American-Arab Anti-Discrimination Committee, Discrimination and National Security Initiative, Muslim Public Affairs Council. Sikh American Legal Defense and Education Fund, Sikh Council on Religion and E ducation, South Asian Americans Leading Together and United Sikhs in Support of Respondent Iqubal", [
        "The Sikh Coalition",
        "American-Arab Anti-Discrimination Committee",
        "Discrimination and National Security Initiative",
        "Muslim Public Affairs Council",
        "Sikh American Legal defense and Education fund",
        "Sikh Council on Religion and Education",
        "South Asian Americans Leading Together",
    ]),
]

def check_amicus(brief, expectation):
    observation = amicus(brief)
    n.assert_list_equal(sorted(observation), sorted(expectation))

def test_amicus():
    for brief, expectation in testcases:
        yield check_amicus, brief, expectation
