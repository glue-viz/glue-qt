Installing with conda
=====================

**Platforms:** MacOS X, Linux, and Windows

Because glue is a reasonably big package with a number of dependencies, we have
found that the default ``conda`` command included in Anaconda/Miniconda can run
into issues when trying to solve the dependencies, so we highly recommend making use
of the `mamba <https://mamba.readthedocs.io/en/latest/>`_ tool to install glue. We have
provided separate instructions below for new and existing conda users.

New conda user
--------------

If you have never used conda before, we recommend downloading the **Mambaforge**
distribution from https://conda-forge.org/miniforge/. For Windows users, you can
download and install using an ``.exe`` installer. For Linux and MacOS X you
should download the appropriate ``.sh`` file and install it using::

    bash MambaForge-*.sh

Once installed, we recommend you create a new environment to install glue in using::

    mamba create -n glue-env

You can then switch to this environment using::

    mamba activate glue-env

and install glue with::

    mamba install glueviz

Existing conda user
-------------------

If you already use the `Anaconda <https://www.anaconda.com/distribution/>`__ Python
distribution from Continuum Analytics or the related `Miniconda
<https://docs.conda.io/en/latest/miniconda.html>`__ distribution, we recommend first
installing ``mamba`` using::

    conda install -c conda-forge mamba

Once installed, we recommend you create a new environment to install glue in using::

    mamba create -n glue-env

You can then switch to this environment using::

    mamba activate glue-env

and install glue with::

    mamba install -c conda-forge glueviz

Updating glue
-------------

To update the packages in your ``glue-env`` environment to the latest available
versions, you can do::

    mamba update -c conda-forge --all
