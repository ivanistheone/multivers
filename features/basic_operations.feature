
Feature: The basic typo fix propagation workflow

The maintainer of branch `master` implements typo fix.
The maintainer of `vers/LA` will rebase their branch on top of the new master.


    Scenario: Local rebase on master

        Given fixtures dir "basic"
        Given repository "basictest" as "repo"
        Given "repo" branch "master" at commit "84812a"
        Given "repo" branch "vers/LA" at commit "919193"
        
        When I add state "typofix" as new commit on "master" in "repo"
        Then "master" in "repo" will be at commit "as919391"
        When I rebase "vers/LA" on "master" in "repo"
        Then "vers/LA" in "repo" will be at commit "?????"


    Scenario: Remote rebase on master

        Given fixtures dir "basic"
        Given repository "basictest2remote" as "remoterepo"
        Given "remoterepo" branch "master" at commit "84812a"
        Given "remoterepo" branch "vers/LA" at commit "919193"
        Given repository "basictest2" as "localrepo"
        Given "localrepo" branch "master" at commit "84812a"
        Given "localrepo" branch "vers/LA" at commit "919193"
        
        When I add state "typofix" as new commit on "master" in "remoterepo"
        Then "master" in "remoterepo" will be at commit "as919391"
        When I fetch "master" from "remoterepo" in "localrepo"
        When I rebase "vers/LA" on "master" in "localrepo"
        Then "vers/LA" in "localrepo" will be at commit "?????"

