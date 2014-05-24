import re
from collections import Counter

from unidecode import unidecode

def amici(brief:str) -> list:
    if ' and ' in brief.lower() and ',' in brief:
        buffer = 20
    elif re.search(r' inc[^a-z]', brief, flags = re.IGNORECASE):
        buffer = 5
    else:
        buffer = 0
    return list(filter(None, _amici(unidecode(brief), buffer, 0)))

def _amici(brief:str, buffer:int, start:int) -> iter:
    _amicus_separator = re.compile(r'(?:,| and) ')

    match = re.search(_amicus_separator, brief[start:])
    buffered_start = max(0, start - buffer)
    if match != None:
        buffered_end = start + match.end() + buffer
        yield brief[buffered_start:buffered_end]
        child = _amici(brief, buffer, start + match.end())
        if child != None:
            yield from child
    else:
        yield brief[buffered_start:]

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
        return ''
