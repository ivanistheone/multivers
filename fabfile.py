"""
fabfile with git operations for authors

Run using `fab taskname:arg,kwarg=kwval` assuming system-wide `fabric` installed.
"""
from __future__ import print_function, unicode_literals
import os
import sys

from fabric.api import local, lcd, task, env, hide
from fabric.colors import red, green, yellow, cyan

# SETTINGS
env.FIXTURES_DIR = 'tests/fixtures'


# MULTIVERS COMMANDS
################################################################################
# see blog post for motivation: https://minireference.com/blog/git-for-authors/

def newversion(repo, name, parent='master'):
    """
    Create a git branch (new vers) called `vers/name` forked of `parent` branch.
    """
    pass

def workon(repo, branch, vers=None):    # ??? 'vers/math' or just 'math' ???
    """
    Checkout the source code for branch `branch`.
    """
    pass

def save(repo):
    """
    Save changes done on the working directory to the local repository.
    """
    pass

def saveas(repo, newbr):
    """
    Save changes done on the working directory as a new branch called `newbr`.
    """
    pass

def publish(repo, remote='origin'):
    """
    Pushes local changes to `remote` and makes them public for others to see.
    """
    pass

def suggestedits(repo, upstream=None):
    """
    Create a pull-request to the `upsteam` repository.
    """
    pass




# GIT COMMANDS
################################################################################

@task
def rebase(repo, branch, onto='master', upstream='master'):
    """
    Rewrite all changes from `upstream` until `branch` on top of branch `onto`.
    
    Given the history shown, running the command
    
        git rebase master branch
        
    will have the follwing effect:
        
          A---B---C branch                                A'--B'--C' branch
         /                         -->                   /
     ...D---E---F---G master             ...D---E---F---G master
    
    """
    with lcd(repo):
        local('git rebase --onto %s  %s %s' % (onto, upstream, branch))

@task
def reset(repo, branch="master", rev='HEAD'):
    """
    Discard all non-committed changes in workind dir and load code from `rev`.
    By default, loads the latest commit (HEAD) from the master `branch`.
    """
    with hide('running', 'stdout', 'stderr'):
        has_head = local('git rev-parse HEAD &> /dev/null').return_code == 0
    print(green(has_head))
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
        local('git checkout %s %s' % (options, branch))

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
        local('git --no-pager diff --cached  %s' % commit)

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


# TESTS COMMANDS
################################################################################

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
    if not os.path.exists(env.FIXTURES_DIR):
        raise ValueError('No fixtures dir.')
    #
    srcdir = os.path.join(env.FIXTURES_DIR, fixname, fixstate)
    with lcd(srcdir):
        print(yellow('Fixture files:'))
        local('ls -ltr')
    local('cp -R %s/* %s/' % (srcdir,dest))
    with lcd(dest):
        local('ls -ltr')



# UTILS
################################################################################
@task
def WTF(repo):
    """
    Run this when you don't know what's going on...
    """
    status(repo)
    # check beanches, detached HEAD state, uncommited stuff, incoming, etc...
