#!/usr/bin/env python
"""
Command line tool managing text patches based on google-diff-match-patch

"""

import argparse
import os
from lib.diff_match_patch import diff_match_patch
import re
import sys

dmp = diff_match_patch()            # dmp object instance

class bcolors:
    REMOVED = '\033[9;97;41m'
    ADDED = '\033[97;42m'
    ENDC = '\033[0m'


def diff(file1, file2, options):
    """ print the diff between two files """

    path1 = os.path.join(options.basedir, options.extdir, file1)
    path2 = os.path.join(options.basedir, options.incdir, file2)

    diffs = dmp.diff_main(file(path1).read(), file(path2).read())
    dmp.diff_cleanupSemantic(diffs)

    sb = []
    for match in diffs:
    	if match[0] == 0:
            sb.append(match[1])
            continue
        if match[0] < 0:
            color = bcolors.REMOVED
        elif match[0] > 0:
            color = bcolors.ADDED
        s = ('\\n' + bcolors.ENDC + "\n" + color).join(match[1].split("\n"))
        s = ('\\t\t').join(s.split('\t'))
        sb.append(color)
        sb.append(s)
        sb.append(bcolors.ENDC)

    output = ''.join(sb)
    print output



def build(file1, file2, options):
    """Apply the patch to file in ext/ to produce inc/ file """

    # setup paths
    path1 = os.path.join(options.basedir, options.extdir, file1)
    noextname = os.path.splitext(os.path.basename(file1))[0]
    pathp = os.path.join(options.basedir, options.patchdir, noextname+'.patch')
    path2 = os.path.join(options.basedir, options.incdir, file2)

    text1 = open(path1).read()
    patches_text = open(pathp,'r').read()
    patches = dmp.patch_fromText(patches_text)

    text2, stats = dmp.patch_apply(patches, text1)

    print "Patching results", stats
    open(path2,'w').write(text2)


def mkpatch(file1, file2, options):
    """Generate a patch for changes in edt/ file relative to ext/ file.
       Store results in patch/ dir. """

    # setup paths
    path1 = os.path.join(options.basedir, options.extdir, file1)
    path2 = os.path.join(options.basedir, options.edtdir, file2)
    noextname = os.path.splitext(os.path.basename(file1))[0]
    pathp = os.path.join(options.basedir, options.patchdir, noextname+'.patch')

    text1 = open(path1).read()
    text2 = open(path2).read()

    diffs = dmp.diff_main(text1, text2)
    dmp.diff_cleanupSemantic(diffs)

    patches = dmp.patch_make(text1, diffs)
    patches_text = dmp.patch_toText(patches)
    open(pathp,'w').write(patches_text)



def testpatch(file1, file2, options):
    """Apply the patch to file in ext/ to produce inc/ file """

    # setup paths
    path1 = os.path.join(options.basedir, options.extdir, file1)
    noextname = os.path.splitext(os.path.basename(file1))[0]
    pathp = os.path.join(options.basedir, options.patchdir, noextname+'.patch')

    text1 = open(path1).read()
    patches_text = open(pathp,'r').read()
    patches = dmp.patch_fromText(patches_text)

    text2, stats = dmp.patch_apply(patches, text1)

    print "Patching results", stats



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='A command line tool for managing versions as patches.')
    parser.add_argument('command', action='store', choices=['build','diff','mkpatch','test'],
                         help='The command you want to run')
    parser.add_argument('file1', action='store', help="Left file")
    parser.add_argument('file2', action='store', help="Right file")
    parser.add_argument('--extdir',   action="store", default="ext"  , help="External files dir (source)")
    parser.add_argument('--patchdir', action="store", default="patch", help="Where patch files are stored")
    parser.add_argument('--incdir',   action="store", default="inc"  , help="Director for generated local files (destination)")
    parser.add_argument('--edtdir',   action="store", default="edt",   help="Where local edits happen")
    parser.add_argument('--basedir',  action="store", default="."  ,   help="Parent dir of ext/ edt/ patch/ inc/ dirs")

    args = parser.parse_args()
    print args

    if args.command == 'build':
        build(args.file1, args.file2, options=args)
    elif args.command == 'diff':
        diff(args.file1, args.file2, options=args)
    elif args.command == 'mkpatch':
        mkpatch(args.file1, args.file2, options=args)
    elif args.command == 'test':
        testpatch(args.file1, args.file2, options=args)
    else:
        print "don't know what you want me to do..."
        sys.exit(1)
        


