


       Comparing branches

               $ git diff topic master    (1)
               $ git diff topic..master   (2)
               $ git diff topic...master  (3)

           1. Changes between the tips of the topic and the master branches.
           2. Same as above.
           3. Changes that occurred on the master branch since when the topic branch was started off it.
           

FAB examples from https://github.com/dploi/dploi-fabric/blob/master/dploi_fabric/git.py

```
        def update():
            test = run("cd %(path)s; git --no-pager diff --stat" % env)
            if "files changed" in test:
                print CAUTION...
            run("cd %(path)s; find . -iname '*.pyc' -delete" % env)
            run("cd %(path)s; git fetch origin" % env)
            run("cd %(path)s; git reset --hard" % env)
            run("cd %(path)s; git checkout %(branch)s" % env)
            run("cd %(path)s; git pull origin %(branch)s" % env)
            if exists(posixpath.join(env.path, ".gitmodules")):
                run("cd %(path)s; git submodule init" % env)
                run("cd %(path)s; git submodule update" % env)
            append_settings()

        def incoming(remote='origin', branch=None):
            """
            Displays incoming commits 
            """
            if not branch:
                branch = env.branch
            run(("cd %(path)s; git fetch " + remote + " && git log --oneline --pretty=format:'%%C(yellow)%%h%%C(reset) - %%s %%C(bold blue)<%%an>%%C(reset)' .." + remote + '/' + branch) % env)


        def local_branch_is_dirty(ignore_untracked_files=True):
            untracked_files = '--untracked-files=no' if ignore_untracked_files else ''
            git_status = local(
                'git status %s --porcelain' % untracked_files, capture=True)
            return git_status != ''


        def local_branch_matches_remote():
            local_branch = local(
                'git rev-parse --symbolic-full-name --abbrev-ref HEAD',
                capture=True).strip()
            target_branch = env.branch.strip()
            return local_branch == target_branch
```

see also https://github.com/ronnix/fabtools/blob/master/fabtools/git.py

