Installing with pip
===================

**Platforms:** MacOS X, Linux, and Windows

You can install glue along with **all** required and optional dependencies
with `pip <https://pip.pypa.io/en/stable/>`__ using::

    pip install glueviz[qt]

The above will include domain-specific plugins as well as the PyQt5 library.
If you only want to install glue with minimal dependencies, you can instead
install individual glue packages, e.g.::

    pip install glue-core   # base package with no front-end
    pip install glue-qt[qt] # Qt-based front-end
    pip install glue-vispy-viewers  # 3D viewers

The ``[qt]`` ensures PyQt5 gets installed, but you can also install PyQt6 or
PySide yourself and miss out the ``[qt]``.
