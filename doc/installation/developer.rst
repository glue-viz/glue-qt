Installing the latest developer version
=======================================

.. note:: The latest developer version is not guaranteed to work correctly
          or be functional at all, so use with care!

If you normally use conda or pip to install glue and want to try out the
latest developer version, the recommended way is to use pip to install
packages from the git repository directly.

If you use conda/mamba, we recommend that you first make a clean environment
dedicated to developer versions::

    mamba create -n glue-dev-env
    mamba activate glue-dev-env

You can then install the latest developer version of glue-core and glue-qt (for the
Qt desktop application) with::

    pip install git+https://github.com/glue-viz/glue
    pip install git+https://github.com/glue-viz/glue-qt
