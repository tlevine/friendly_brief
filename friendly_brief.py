import re
from collections import Counter

from unidecode import unidecode

def amici(brief:str) -> list:
    return list(_amici(unidecode(brief), 0))

def _amici(brief:str, start:int) -> iter:
    _amicus_separator = re.compile(r'(?:,| and) ')
    _buffer = 20

    match = re.search(_amicus_separator, brief[start:])
    if match != None:
        buffered_start = max(0, start - _buffer)
        buffered_end = match.end() + _buffer
        yield brief[buffered_start:buffered_end]
        yield from _amici(brief, start + match.end())

def brief_number(brief:str) -> int:
    return int(re.sub('[^0-9].+$', '', brief))

def posture(brief:str) -> int:
    codes = [
        (0, ('Neither party',)), # maybe change it to just "Neither"?
        (1, ('Petitioner', 'Appellant', 'Reversal')),
        (2, ('Respondent', 'Appellee', 'Affirmance')),
        (3, ('Plaintiff',)),
        (4, ('Defendant',)),
    ]

    code_phrase_observations = Counter()
    for code, phrases in codes:
        for phrase in phrases:
            if phrase.lower() in brief.lower():
                code_phrase_observations[code] += 1

    if len(code_phrase_observations.keys()) == 1:
        return list(code_phrase_observations.keys())[0]
    else:
        return None
