import friendly_brief.cli as cli

import nose.tools as n

def test_parser():
    observed = cli.parser().parse_args([])
    import sys
    n.assert_equal(observed.spreadsheet, sys.stdin)
