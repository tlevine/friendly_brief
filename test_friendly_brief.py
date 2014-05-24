import nose.tools as n

import friendly_brief as f

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
    ("7.    Brief, BRIEF OF AMICI CURIAE NOW LEGAL DEFENSE AND EDUCATION FUND, LAWYERS COMMITTEE FOR HUMAN RIGHTS, AND ALLARD K. LOWENSTEIN INTERNATIONAL HUMAN RIGHTS CLINIC IN SUPPORT OF RESPONDENTS, August 10, 2001, 2001 U.S. S. Ct. Briefs LEXIS 43 ", [
        "Now Legal Defense and Education Fund",
        "Lawyers Committee for Human Rights",
        "Allard L Lowestein International Human Rights Clinic",
    ]),
]

def check_amici(brief, expectation):
    def standard(xs):
        return [x.lower() for x in sorted(xs)]
    observation = f.amici(brief)
    n.assert_list_equal(standard(observation), standard(expectation))

@n.nottest
def test_amici():
    for brief, expectation in testcases:
        yield check_amici, brief, expectation

def test_brief_number():
    brief = '6.    Amicus Brief, BRIEF OF LIBERTY LEGAL FOUNDATION AS AMICUS CURIAE IN SUPPORT OF PETITIONERS, February 8, 2012, 2012 U.S. S. Ct. Briefs LEXIS 709 '
    n.assert_equal(f.brief_number(brief), 6)
