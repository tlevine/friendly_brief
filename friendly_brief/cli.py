import argparse, sys

import friendly_brief.read as r

def parser():
    description = 'Extract information about the amici in brief titles.',
    epilog = 'The spreadsheet must be in CSV format and contain a column called "brief".'
    p = argparse.ArgumentParser(description = description, epilog = epilog)
    p.add_argument('spreadsheet', nargs = '?', default = sys.stdin, type = argparse.FileType('r'))
    return p
