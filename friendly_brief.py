import re
from unidecode import unidecode

def amici(brief:str) -> list:
    decoded = unidecode(brief)
    after_curiae = re.sub(r'curiae', '\t\t\t', decoded, flags = re.IGNORECASE, count = 1).partition('\t\t\t')[2].strip(', ').replace('\n',' ')
    before_date = re.sub(r'(january|february|march|april|may|june|july|august|september|october|november|december).*$', '', after_curiae, flags = re.IGNORECASE)
    newline_delimited = re.sub(r'([a-zA-Z]{2})[,.] ',r'\1\n', before_date)
    return filter(None, newline_delimited.split('\n'))

def brief_number(brief:str) -> int:
    return int(re.sub('[^0-9].+$', '', brief))

def posture(brief:str) -> int:
    return None
