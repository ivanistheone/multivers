#!/usr/bin/env python
from __future__ import print_function, unicode_literals
import io
import re
import fileinput
import sys
from argparse import ArgumentParser
from functools import partial


def print_left_right(left_fn, right_fn, lines):
    """ A basic script for spliting a diff file into a left and a right file,
        so that I can run 
    
    left_f = open(left_fn, "w")
    right_f = open(right_fn, "w")
    pl = left_f.write
    pr = right_f.write

    for line_u in lines:
        line = line_u.decode('utf8')
        if line.startswith('+++'):
            pass
        elif line.startswith('---'):
            pass
        elif line.startswith('+'):
            pr(line[1:].encode( "utf-8" ))
        elif line.startswith('-'):
            pl(line[1:].encode( "utf-8" ))
        #elif line.startswith('diff'):
        #    p('<span class="diffcommand">{}</span>'.format(q(line)))
        #else:
        #    m = re.match(r'^@@.*?@@', line)
        #    if m:
        #        num = m.group(0)
        #        rest = line[len(num):]
        #        p('<span class="linenumber">{}</span>{}'
        #                    .format(q(num), q(rest)))
        #    else:
        #        p(q(line))
    left_f.close()
    right_f.close()


def main():
    parser = ArgumentParser()
    parser.add_argument('file', action='store')

    args = parser.parse_args()

    print_left_right( "left.txt", "right.txt", open(args.file).readlines() )


if __name__ == '__main__':
    main()
