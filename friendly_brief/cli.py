import argparse, sys
import csv
from itertools import chain

import friendly_brief.read as r

def parser():
    description = 'Extract information about the amici in brief titles.',
    epilog = 'The spreadsheet must be in CSV format and contain a column called "brief".'
    p = argparse.ArgumentParser(description = description, epilog = epilog)
    p.add_argument('spreadsheet', nargs = '?', default = sys.stdin, type = argparse.FileType('r'))
    return p

def main():
    fp = parser().parse_args().spreadsheet
    reader = csv.reader(fp)
    brief_header = next(reader)
    if 'brief' not in brief_header:
        sys.stderr.write('The input spreadsheet contains no "brief" column.\n')
        sys.exit(1)
    else:
        i = brief_header.index('brief')
        writer = csv.writer(sys.stdout)

        amicus_header = ('brief_number', 'posture', 'amici')
        writer.writerow(tuple(chain(brief_header, amicus_header)))

        for brief_row in reader:
            brief = brief_row[i]
            if brief == '':
                # Stop at the first empty brief.
                break
            try:
                brief_annotations = (r.brief_number(brief), r.posture(brief))
                for amicus in r.amici(brief):
                    writer.writerow(tuple(chain(brief_row, brief_annotations, (amicus,))))
            except:
                sys.stderr.write('Error on the following brief:\n    %s\n' % brief)
