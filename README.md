multivers
=========
Tools for managing multiple versions of text files and content transclusion.

Alternative name idea: `salmon`; because changes godda flow upstream!
Also analogy with salmon fish (as a kid you studied fro these books, now it's time
to return to them and add your contributions).


Motivation
----------
I would like to use part of the material from the [No bullshit guite to math and physics](http://minireference.com)
in my upcoming book on [linear algebra](http://gum.co/noBSLA), and other books.
I don't want a copy though: this will be a maintainability nightmare.
I don't want to just include either as I would like to make some modifications
to the explanations.


Software Requirements Specification
-----------------------------------
As an original author, this is what I would like to do:
  - reuse of content by transclution: DRY for text
  - adaptability: maintain modifications of original as "patches" (git branches)
  - coevolution: as the external text evolves, local inclusions will be updated  (`git rebase`)
  - revision control (text of specific revisions should be usable)

As a reusing author, this is what I'd like to do:
  - reuse other authors' work in my book (think `git clone`)
  - subscribe to updates and patches to the texts that I'm using in my derivative work
  - publish my book for my own audience
  - push my typo fixes and improvements to upstream (pull request)


Design
------
  - The entire workflow be implemented on top of git/hg branches & rebase
  - We'll focus on git as the backend (mercurial is equivalent, but doesn't have github)
  - The "base work" is a git repo that contains `.tex` files
  - A "derivative work" is a branch of the base work that contains specifics
    modifications, e.g. the `vers/LA` branch contains the parts of the MATH&PHYS
    text used in the LA book.
  - Typo fixes and modifications are implemented on the `master` branch, and then
    all derivative branches are rebased so typo fixes propagate.
  - **PROBLEM:** when a derivative work is rebased, it's hash changes so all
    derivatives of derivatives will have dangling parent pointers to be rebased too.
    We need to use tags or some other mechanism to keep derivatives of derivatives in sync.
    Also, need to standardize git hooks (commit hook?) to notify derivative works.
    Related: perhaps we want to use the "mercurial way" and keep up to date with upsteam
    edits by merging them into features/version branches? It avaoids the commit-hash changing
    problem but makes the whoel thing more complicated (end user would have to knwo what merge is).
  - Wrap commands as custom [CLI and web interface for authors](https://minireference.com/blog/git-for-authors/)

  
What happens at each edit?
--------------------------
Let's look in details at the commands that need to run to "update" a propagate
some typo fixes from the `master` branch to the `vers/LA` derivative work.

We assume the initial conditions are as follows:
  - `master` branch: main text of *No bullshit guide to math & physics*
  - `vers/LA` branch: modifications to Ch1 and Ch3 to make `.tex` files suitable
    for inclusion in the LAbook. Specifically `LAbook/inc` contains contains the
    result of `git clone ssh:git...M&Pbook inc`, `cd inc`, `git co -b vers/LA`.

1. The author makes edits to the main text of the book in the `master` branch,
   and commits them using:
   
        git add filechanged.tex
        git ci -m"Fixed a typo in filechanged.tex"
       
2. The author receives a notification that `master` branch has derivative works

        echo "Hi $AUTHOR, not branch `vers/LA` is a derivative work"

3. The author rebases the `vers/LA` branch on `master`:

        git co vers/LA
        git rebase master
        # manually fix problems if rebase isn't clean

4. The system automatically (commit hook?) all repos subscribed to the `vers/LA`
   version of the book of the changes.



Rebasing
--------
Suppose Jane uses the content in `vers/LA` of the main repo from a few months ago,
and wants to update the latest changes from the main repo. She can `fetch` the commits using

    git fetch origin

then co her local branch `vers/LA` and rebase it on origin/vers/LA 

    git rebase origin/vers/LA

or equivalently merge will also work:

    git merge origin/vers/LA

If the commits on the `vers/LA` were rewritten (e.g. using rebase -i then squash)
you won't be able to merge or rebase cleanly (conflict).
In this case, you can overwrite your local branch vers/LA and set its state to origin/vers/LA using: 

    git fetch origin
    git reset --hard origin/vers/LA




Tech research
-------------

1. Test out git rebase commands:

        git rebase [-i] [options] [--exec <cmd>] [--onto <newbase>] [<upstream>] [<branch>]


2. Test using .hg rebase:
   Mark branch as "draft mode":

        hg phase --draft --force -r <first commit on vers/LA>

   Rebase all changes on vers/LA onto latest default branch:

        hg rebase -d default --keepbranches

   Now branch `vers/LA` has two heads. 
  
   Required to make this happen:

        cat .hg/hgrc
            [extensions]
            rebase =


2. Investigate git tags

2. Check how to setup git hooks and possibly 


Issues
------
 
 1. Commit hashes change after rebasing
 2. Merge fails if source changed:
    - surface rebase conflict to user
        - what's the UI?
        - what are the commands?)
    - but better fail partially than fully
      e.g. vers/LA consists of 50 individual commits,
      so even if rebase partially fails the systme still produces a usable book



Previous (abandoned) idea 
-------------------------
Originally, I planned to write custom scripts based on the `diff-math-patch` tool,
and manually manage changes as "patch" files. This approach is way too complex,
and deemed unnecessary given the availability of `git rebase`. Much better to make
use of the first rule of software development: don't write code, someone has
already solved the problem you're trying to solve.








