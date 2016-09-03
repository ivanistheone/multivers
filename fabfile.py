"""
fabfile with git operations for authors

Run using `fab taskname:arg,kwarg=kwval` assuming system-wide `fabric` installed.
"""
from __future__ import print_function, unicode_literals
import os
import sys

from fabric.api import local, lcd, task, env, hide
from fabric.colors import red, green, yellow, cyan

FIXTURES_DIR = 'tests/fixtures'

@task
def createrepo(name, parentdir='.'):
    """
    Creates an empty git repo called `name` in directory `parentdir`.
    """
    lcd(parentdir)
    local('mkdir %s' % name)
    with lcd(name):
        local('git init .')


@task
def loadfixtures(fixname, fixstate, dest=None):
    """
    Copies `tests/fixtures/fixname/fixstate/` recurcively into working tree.
    """
    if not dest:
        raise ValueError('Must specify dest---where to put the fixtures files.')
    if not os.path.exists(FIXTURES_DIR):
        raise ValueError('No fixtures dir.')
    #
    srcdir = os.path.join(FIXTURES_DIR,fixname,fixstate)
    with lcd(srcdir):
        print(yellow('Fixture files:'))
        local('ls -ltr')
    local('cp -R %s/* %s/' % (srcdir,dest))
    with lcd(dest):
        local('ls -ltr')

@task
def reset(repo, branch="master", rev='HEAD'):
    """
    Discard all non-committed changes in workind dir and load code from `rev`.
    By default, loads the latest commit (HEAD) from the master `branch`.
    """
    with hide('running', 'stdout', 'stderr'):
        has_head = local('git rev-parse HEAD &> /dev/null') == 0
    with lcd(repo):
        local('rm -rf *')
        if has_head:
            local("git reset --hard %s" % rev)

@task
def checkout(repo, branch="master", force=True):
    """
    Checkout `branch` to the working directory `repo`.
    """
    if repo is None and not env.has_key('repo'):
        raise ValueError("Path to the `repo` is required")

    options = []
    if force:
        options.append('--force')
    options = ' '.join(options)

    with lcd(repo):
        cmd = 'git checkout %s %s' % (options, branch)
        local(cmd)

@task
def diff(repo, commit='HEAD'):
    """
    Shows diff between files in working directory and `commit`.
    """
    with lcd(repo):
        local('git --no-pager diff %s' % commit)

@task
def diffcached(repo, commit='HEAD', br='master'):
    """
    Shows diff between files in staging area and `commit`.
    """
    with lcd(repo):
        local('git --no-pager --cached diff %s' % commit)

@task
def diffcommits(repo, left='HEAD', right='HEAD'):
    """
    Shows diff between commits `left` and `right`.
    """
    with lcd(repo):
        local('git --no-pager diff %s %s' % (left, right) )

@task
def status(repo):
    with lcd(repo):
        local('git status')

