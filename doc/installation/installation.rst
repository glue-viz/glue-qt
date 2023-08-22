.. _installation:

Installing and running glue
===========================

Several installation methods for glue are outlined in the sections below. If you
run into issues, each page should provide relevant troubleshooting, and you can
also check the :ref:`known-issues` page which collects some more general issues.
If your problem is not described there, `open a new issue
<https://github.com/glue-viz/glue/issues>`_ on GitHub.

.. toctree::
   :maxdepth: 1

   standalone
   conda
   pip
   developer

Once glue is installed, you will either be able do double click on the
application icon (in the case of the standalone applications) or be able to type::

    glue

in a terminal to start glue. Glue accepts a variety of command-line arguments.
See ``glue --help`` for examples.

You can also start glue with the ``-v`` option::

    glue -v

to get more verbose output, which may help diagnose issues.
