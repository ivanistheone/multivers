multivers
=========

Tools for managing multiple versions of text files and content transclusion.




Motivation
----------
I would like to use part of the material from the 
[No bullshit guite to math and physics](http://minireference.com)
in my upcoming book on linear algebra. 
I don't want a copy though: this will be a maintainability nightmare.
I don't want to just include either as I would like to make some modifications to the explanations.

This is what I would like to do:
  - reuse of content by transclution:  DRY for text.
  - adaptability: maintain modifications of original as patches.
  - coevolution: as the external text evolves, local inclusions will be updated 
  - revision control (text of specific revisions should be usable)



PHASE 1: diff-math-patch command line tool
------------------------------------------
Okay we need a little diff/patch mechanism. This is how it could go:

    Original file:              Edit space:    
    hg/git://topic.tex          edt/topic.tex (local modifications)
        |                          | 
       init                      mkpatch
        |                          | 
    Cache of originals:         Patch dir:                      Local include-ready file:
    ext/topic.tex        -+-    patch/topic.patch    -build->   inc/topic.tex  

                        
Example usage
-------------
    mulitvers.py build   topic.tex        incf <= extf + patch
    mulitvers.py diff    topic.tex        diff(extf,incf)             
    mulitvers.py mkpatch topic.tex        patch <= edtf - extf
    mulitvers.py test    topic.tex        test if patch works




What happens after an edit?
---------------------------
  Local editing:        (only for local-specifc changes, edit src for typos in both versions)
    edt/topic.tex SAVE
    multivers.py mkpatch topic.tex
        --> regenerate patch/topic.patch

  Parent editing:
    ext/topic.tex  SAVE
    multivers.py test topic.tex
        --> check if patch/topic.patch still applies (and correctly) to new source file
        --> if WORKS: regenerate inc/topic.patch relative to new
        --> else: manual fix


TODO
----
  - Test different settings of Match_Threshold, Match_Distance, and Patch_Margin
    We do not algo to be too smart: 
  - Could this entire worflow be implemented on top of git/hg with branches & rebases?


git rebase usage: 

      git rebase [-i] [options] [--exec <cmd>] [--onto <newbase>] [<upstream>] [<branch>]

      AWESOME!
      The first rule of software development: Don't write code, someone has already solved the problem.


Plan for tomorrow
-----------------

Test out git and work on metadata format:

    .multivars
        upstream: /CurrentPorjects/Minireference/noBSguideMathMechCalc
        notify: inc



    








