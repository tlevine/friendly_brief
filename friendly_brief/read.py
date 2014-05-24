import re
from collections import Counter

from unidecode import unidecode

def amici(brief:str) -> list:
    amici_section = re.sub(r' (:?january|february|april|may|june|july|august|september|october|november|december) [0-9]{1,2}.*', '', brief, flags = re.IGNORECASE)
    amici_section = re.sub(r'[0-9]+\. +Brief,', '', amici_section, flags = re.IGNORECASE)

    match = re.search(r'amici (?:curiae)?', amici_section, flags = re.IGNORECASE)
    if match != None and match.start() < 30:
        amici_section = amici_section[match.end():]
    match = re.search(r'amici (?:curiae)?', amici_section, flags = re.IGNORECASE)
    if match != None and match.start() > len(amici_section) / 2:
        amici_section = amici_section[:match.start()]

    if amici_section.lower().count(' support ') <= 1:
        amici_section = re.sub(r' support .*', '', amici_section, flags = re.IGNORECASE)

    if ',' in amici_section and ' and ' in amici_section.lower():
        buffer = 20
    elif re.search(r' inc[^a-z]', amici_section, flags = re.IGNORECASE):
        buffer = 5
    else:
        buffer = 0
    return list(filter(None, _amici(unidecode(amici_section), buffer, 0)))

def _amici(brief:str, buffer:int, start:int) -> iter:
    _amicus_separator = re.compile(r'(?:,| and) ', flags = re.IGNORECASE)

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
