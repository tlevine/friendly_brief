import re
from itertools import chain
from collections import Counter

from sliding_window import window
from unidecode import unidecode

def amici(brief:str) -> list:
    _amicus_regex = re.compile(r'(?:amicus brief|amici brief|amici curiae|amicus curiae|motion for leave to file and brief)(?: of)?', flags = re.IGNORECASE)
    amici_section = re.sub(r',? (:?january|february|april|may|june|july|august|september|october|november|december) [0-9]{1,2}.*', '', brief, flags = re.IGNORECASE)
    amici_section = re.sub(r'[0-9]+\. +Brief,', '', amici_section, flags = re.IGNORECASE)

    match = re.search(_amicus_regex, amici_section)
    if match != None and match.start() < 30:
        amici_section = amici_section[match.end():]
    match = re.search(_amicus_regex, amici_section)
    if match != None and match.start() > len(amici_section)*2/5:
        amici_section = amici_section[:match.start()]

    amici_section = re.sub(r' in support of .*', '', amici_section, flags = re.IGNORECASE)

#   if re.search(r' inc[^a-z]', amici_section, flags = re.IGNORECASE):
#       buffer = 5
#   elif ',' in amici_section and ' and ' in amici_section.lower():
#       buffer = 0
#   else:
#       buffer = 0
    buffer = 0

    l = amici_section.lower()
    if l.count(',') > 3 or ', and' in l or l.count(',') > l.count('and') or l.count(',') == l.count(', inc'):
        _regex = r', '
    else:
        _regex = r'(?:,| and) '
    amicus_separator = re.compile(_regex, flags = re.IGNORECASE)

    def clean(result):
        r = result.strip()
        match = re.search(r'brief(?: of)?(?: amicus curiae)? ', r, flags = re.IGNORECASE)
        if match and match.end() < len(result) / 2:
            return r[match.end():]
        elif match and match.start() > len(result) / 2:
            return r[:match.start()]
        else:
            return r

    results = map(clean, _amici(unidecode(amici_section), amicus_separator, buffer, 0))
    for previous_result, current_result, next_result in window(chain(['  '], results, ['  ']), n = 3):
        if 'inc.' in next_result.lower():
            yield current_result + ', ' + next_result
            next(results)
        elif 'et al.' in next_result.lower():
            yield current_result + ', ' + next_result
            next(results)
#       elif previous_result.count(' ') == 0:
#           yield previous_result + ' and ' + current_result
        else:
            yield current_result

def _amici(brief:str, amicus_separator, buffer:int, start:int) -> iter:
    match = re.search(amicus_separator, brief[start:])
    buffered_start = max(0, start - buffer)
    if match != None:
        buffered_end = start + match.start() + buffer
        result = brief[buffered_start:buffered_end]

        if result.count(' ') == 0:
            if ' and' == brief[buffered_end+1:buffered_end + 5]:
                # Probably the beginning of an amicus like
                # "Discrimination and National Security Initiative"
                nextmatch = re.search(_amicus_separator, brief[start + match.end()])
                if nextmatch != None:
                    # Replace the result.
                    result = brief[buffered_start:start + nextmatch.end() + buffer]

        if re.search(r'[a-z]{4}\.', result):
            match = re.match(r'(.*[a-z]{4})\.(.*)$', result)
            yield match.group(1)
            yield match.group(2)
        elif result == '':
            pass
        else:
            yield result
        child = _amici(brief, amicus_separator, buffer, start + match.end())
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
