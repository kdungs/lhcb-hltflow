#!/usr/bin/env python

import argparse
import json
import sys

from hltflow.core import StreamerFlowchart
from hltflow import latex


DESC = '''
Turn an Hlt1 streamer into a nice TikZ-based flowchart.
This program will read the streamer's code from stdin.
Thus it can be used with pipes as for example:
  {} Test < tests/data/code.txt
'''.format(sys.argv[0])

EPILOG = '''
When supplying a configuration in a JSON file make sure that
the syntax is correct. Example:
[{
  "name": "Your streamer's name here.",
  "code": "Your streamer's code here. Separate newlines by \\n"
}, {
  "name": "Another streamer's name, you can add as many as you like.",
  "code": "Its code."
}]
'''

def main():
    """
        Run a command line interface that exposes the functionality in a simple
        way.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=DESC,
        epilog=EPILOG
    )
    parser.add_argument('name', help='the streamer\'s name')
    parser.add_argument('-c', '--config', metavar='configfile',
        help='Path of a JSON file containing a valid config.')
    args = parser.parse_args()
    if args.config is None:  # process single file read from stdin
        streamers = [{'name': args.name, 'code': sys.stdin.read()}]
    else:  # process one or more files from config
        with open(args.config) as cf:
            streamers = json.load(cf)

    flowcharts = (StreamerFlowchart(**s) for s in streamers)
    figures = (latex.make_figure(f) for f in flowcharts)
    document = latex.make_document(figures)
    print(document)


if __name__ == '__main__':
    main()
