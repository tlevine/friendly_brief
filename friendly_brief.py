import re
from unidecode import unidecode

def amicus(text):
    decoded = unidecode(text)
    after_curiae = re.sub(r'curiae', '\t\t\t', decoded, flags = re.IGNORECASE, count = 1).partition('\t\t\t')[2].strip(', ').replace('\n',' ')
    newline_delimited = re.sub(r'([^.])[,.] ',r'\1\n', after_curiae)
    return newline_delimited.split('\n')
