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

The ``[qt]`` ensures PyQt5 gets installed and set as the front-end,
but you can also instead install PySide2, PySide6, or PyQt6 by doing e.g.::

    pip install glue-qt PyQt6
