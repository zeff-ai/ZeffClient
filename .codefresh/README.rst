=========
CodeFresh
=========

This directory contains the files necessary to execute CI/CD
on codefresh.io system.


Local Testing
=============


Locally testing configuration file requires docker and CodeFresh CLI
to be installed.  See
`Running Pipelines Locally <https://codefresh.io/docs/docs/configure-ci-cd-pipeline/running-pipelines-locally/>`_
for details on getting codefresh engine running.

Generally ``docker pull codefresh/engine:master`` will all that is
required.


Context
-------

A codefresh context is required to run a pipeline. Check to see if
`zeffclient` is available with

::
      
      codefresh get context zeffclient

and create if it does not exist with

::

      codefresh create context yaml zeffclient


ci_zeffclient
-------------

The following command will run the CI for ZeffClient with the results
being placed in a local volume (`~/.Codefresh/ZeffClient/ci_zeffclient`)
for after run analysis.

::

    codefresh run ZeffClient/ci_zeffclient \
        --local \
        --local-volume \
        --yaml=.codefresh/ci_zeffclient.yml \
        --context=zeffclient \
        --var-file=.codefresh/var_file.yml \
        -b master
