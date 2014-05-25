import re
from itertools import chain
from collections import Counter

from sliding_window import window
from unidecode import unidecode

def _remove_date(brief:str) -> str:
    return re.sub(r',? (:?january|february|march|april|may|june|july|august|september|october|november|december) [0-9]{1,2}.*$', '', brief, flags = re.IGNORECASE)

MANUAL_OVERRIDE = [
    (r'^$', []),
    ("1. Brief, BRIEF OF AMICI CURIAE NATIONAL ASSOCIATION OF CRIMINAL DEFENSE LAWYERS AND FAMILIES AGAINST MANDATORY MINIMUMS FOUNDATION AND ASSOCIATION OF FEDERAL DEFENDERS IN SUPPORT OF PETITIONERTHE NATIONAL ASSOCIATION OF CRIMINAL DEFENSE LAWYERS and FAMILIES AGAINST MANDATORY MINIMUMS FOUNDATION and THE ASSOCIATION OF FEDERAL DEFENDERS", ['NATIONAL ASSOCIATION OF CRIMINAL DEFENSE LAWYERS', 'FAMILIES AGAINST MANDATORY MINIMUMS FOUNDATION', 'ASSOCIATION OF FEDERAL DEFENDERS'])
]

def amici(brief:str) -> list:
    for member, result in MANUAL_OVERRIDE:
        if re.match(member, brief):
            return result

    _amicus_regex = re.compile(r'(?:amicus brief|amici brief|amici curiae|amicus curiae|motion for leave to file and brief)(?: of)?', flags = re.IGNORECASE)
    amici_section = _remove_date(brief)
    amici_section = re.sub(r'[0-9]+\. +Brief,', '', amici_section, flags = re.IGNORECASE)

    match = re.search(_amicus_regex, amici_section)
    if match != None and match.start() < 30:
        amici_section = amici_section[match.end():]
    match = re.search(_amicus_regex, amici_section)
    if match != None and match.start() > len(amici_section)*2/5:
        amici_section = amici_section[:match.start()]

    amici_section = re.sub(r' in support of .*', '', amici_section, flags = re.IGNORECASE)

    # Inc.The
    amici_section = re.sub(r'([^ ])The ', r'\1, The ', amici_section)

    onlycomma = r'(?:,| and the| and other) '
    l = amici_section.lower()
    if l.count(';') > 0:
        _regex = r'; '
    elif l.count(',') > 3 or ', and' in l or l.count(',') > l.count('and') or l.count(',') == l.count(', inc'):
        _regex = onlycomma 
    else:
        _regex = r'(?:,| and) '
    amicus_separator = re.compile(_regex, flags = re.IGNORECASE)

    def clean(result):
        r = result.strip()
        r = re.sub(r' as ?$', '', r, flags = re.IGNORECASE)
        r = re.sub(r'^ ?(for|of|and|amic(i|us) curiae) ?', '', r, flags = re.IGNORECASE)
        match = re.search(r'brief(?: for| of)?(?: the)?(?: amic(?:us|i) curiae)? ', r, flags = re.IGNORECASE)
        if match and match.start() < len(result) / 2:
            return r[match.end():]
        elif match and match.end() > len(result) / 2:
            return r[:match.start()]
        else:
            return r

    # Clean twice
    results = map(clean, map(clean, _amicus(unidecode(amici_section), amicus_separator, 0)))
    slider = window(chain([''], results, ['']), n = 3)
    out = []
    for previous_result, current_result, next_result in slider:
        if re.match(r'^(|as|amic(i|us) curiae)$', current_result, flags = re.IGNORECASE):
            pass
        elif re.match(r'^[^a-z]{0,2}(inc|jr)[^a-z]{0,2}', next_result, flags = re.IGNORECASE):
            out.append(current_result + ', ' + next_result)
            next(slider)
        elif re.match(r'^et al\.?,?$', next_result, flags = re.IGNORECASE):
            out.append(current_result + ', ' + next_result)
            next(slider)
        else:
            out.append(current_result)

    if len(out) >= 3 and _regex == onlycomma:
        out = out[:-1] + re.split(r' and ', out[-1], flags = re.IGNORECASE)

    def finalize(result):
        result = re.sub(r'^ ?(amici|of )', '', result, flags = re.IGNORECASE)
        result = re.sub(r' (on behalf of).*$', '', result, flags = re.IGNORECASE)
        result = re.sub(r',$', '', result)
        return result
    return list(map(finalize, out))

def _amicus(brief:str, amicus_separator, start:int) -> iter:
    match = re.search(amicus_separator, brief[start:])
    if match != None:
        end = start + match.start()
        result = brief[start:end]

        if result.count(' ') == 0:
            if ' and' == brief[end+1:end + 5]:
                # Probably the beginning of an amicus like
                # "Discrimination and National Security Initiative"
                nextmatch = re.search(amicus_separator, brief[start + match.end()])
                if nextmatch != None:
                    # Replace the result.
                    result = brief[start:start + nextmatch.end()]

        if re.search(r'[a-z]{4}\.', result):
            match = re.match(r'^(.*[a-z]{4})\.(.*)$', result)
            yield match.group(1)
            yield match.group(2)
        elif result == '':
            pass
        else:
            yield result
        child = _amicus(brief, amicus_separator, start + match.end())
        if child != None:
            yield from child
    else:
        yield brief[start:]

def brief_number(brief:str) -> str:
    return re.sub('[^0-9].+$', '', brief)

def posture(brief:str) -> str:
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
        return str(list(code_phrase_observations.keys())[0])
    else:
        return ''
