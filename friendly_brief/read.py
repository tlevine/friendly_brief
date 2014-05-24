import re
from collections import Counter

from unidecode import unidecode

def amici(brief:str) -> list:
    amici_section = re.sub(r',? (:?january|february|april|may|june|july|august|september|october|november|december) [0-9]{1,2}.*', '', brief, flags = re.IGNORECASE)
    amici_section = re.sub(r'[0-9]+\. +Brief,', '', amici_section, flags = re.IGNORECASE)

    _amicus = re.compile(r'(?:amicus brief|amici brief|amici curiae|amicus curiae|motion for leave to file and brief)(?: of)?', flags = re.IGNORECASE)
    match = re.search(_amicus, amici_section)
    if match != None and match.start() < 30:
        amici_section = amici_section[match.end():]
    match = re.search(_amicus, amici_section)
    if match != None and match.start() > len(amici_section)*2/5:
        amici_section = amici_section[:match.start()]

    amici_section = re.sub(r' in support of .*', '', amici_section, flags = re.IGNORECASE)

    if re.search(r' inc[^a-z]', amici_section, flags = re.IGNORECASE):
        buffer = 5
    elif ',' in amici_section and ' and ' in amici_section.lower():
        buffer = 0
    else:
        buffer = 0
#   buffer = 0
    return list(_amici(unidecode(amici_section), buffer, 0))

def _amici(brief:str, buffer:int, start:int) -> iter:
    _amicus_separator = re.compile(r'(?:,| and) ', flags = re.IGNORECASE)

    match = re.search(_amicus_separator, brief[start:])
    buffered_start = max(0, start - buffer)
    if match != None:
        buffered_end = start + match.start() + buffer
        result = brief[buffered_start:buffered_end].strip()

        if result.count(' ') == 0:
            if ' and' == brief[buffered_end+1:buffered_end + 5]:
                # Probably the beginning of an amicus like
                # "Discrimination and National Security Initiative"
                nextmatch = re.search(_amicus_separator, brief[start + match.end()])
                if nextmatch != None:
                    # Replace the result.
                    result = brief[buffered_start:start + nextmatch.end() + buffer]

        if result != '':
            yield result
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
