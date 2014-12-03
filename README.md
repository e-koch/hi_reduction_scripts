Respository of 21-cm reduction scripts.

Right now this is the kitchen sink. Over the course of the next couple
months, we'd like to refine into something sleek for both Local Group
and EveryTHINGS work.

Contents:

* vla_heracles/

    Contains the produres used in the VLAHERACLES reduction. They used an
    older version of CASA (~3.0) in ~fall 2010 (some scripts have been updated to work with CASA 4.3).
    These are parts that go together into slightly individualized reduction scripts for each
    galaxy.

* m31_evla/

    Contains the scripts used to reduce the EVLA M31 HI data. This
    approach was to store switching information in a few text files, along
    with customized flagging scripts for each galaxy. Then these scripts
    were run.

* m33_archival/

    Reduction and imaging scripts for the archival VLA M33 data. Some interactive
    flagging is necessary (especially for B configuration!). Note that track 2
    is completely discarded for B config.

* obs_prep/

    Tools for assisting in preparing observations. Currently only contains a
    general function to create a grid of pointings.

