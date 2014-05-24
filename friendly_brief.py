import re
from unidecode import unidecode

def amicus(text:str):
    decoded = unidecode(text)
    after_curiae = re.sub(r'curiae', '\t\t\t', decoded, flags = re.IGNORECASE, count = 1).partition('\t\t\t')[2].strip(', ').replace('\n',' ')
    before_date = re.sub(r'(january|february|march|april|may|june|july|august|september|october|november|december).*$', '', after_curiae, flags = re.IGNORECASE)
    newline_delimited = re.sub(r'([a-zA-Z]{2})[,.] ',r'\1\n', before_date)
    return filter(None, newline_delimited.split('\n'))

def brief_number(text:str):
