# -*- coding: utf-8 -*-
#
# Glue documentation build configuration file

import os
import sys
import importlib.metadata

# -- General configuration ----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '1.6'

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.todo',
              'sphinx.ext.coverage',
              'sphinx.ext.mathjax',
              'sphinx.ext.viewcode',
              'sphinx.ext.intersphinx',
              'numpydoc',
              'sphinx_automodapi.automodapi',
              'sphinx_automodapi.smart_resolver',
              'sphinxcontrib.spelling']

# Add the redirect.py plugin which is in this directory
sys.path.insert(0, os.path.abspath('.'))
extensions.append('redirect')

# Workaround for RTD where the default encoding is ASCII
if os.environ.get('READTHEDOCS') == 'True':
    import locale
    locale.setlocale(locale.LC_ALL, 'C.UTF-8')

intersphinx_cache_limit = 10     # days to keep the cached inventories
intersphinx_mapping = {
    'python': ('https://docs.python.org/3.7', None),
    'matplotlib': ('https://matplotlib.org', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'astropy': ('https://docs.astropy.org/en/stable/', None),
    'echo': ('https://echo.readthedocs.io/en/latest/', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable/', None),
    'PyQt5': ('https://www.riverbankcomputing.com/static/Docs/PyQt5/', None),
    'glue': ('http://glue-core.readthedocs.org/en/latest/', None),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'Glue'
copyright = u'2012-2019, Chris Beaumont, Thomas Robitaille, Michelle Borkin'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
version = release = importlib.metadata.version('glue-core')

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', '_templates', '.eggs']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output --------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_book_theme'

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = '_static/logo.png'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Output file base name for HTML help builder.
htmlhelp_basename = 'Gluedoc'

# -- Options for LaTeX output -------------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
    ('index', 'Glue.tex', u'Glue Documentation',
     u'Chris Beaumont, Thomas Robitaille, Michelle Borkin', 'manual'),
]

# -- Options for manual page output -------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'glue', u'Glue Documentation',
     [u'Chris Beaumont, Thomas Robitaille, Michelle Borkin'], 1)
]

# -- Options for Texinfo output -----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    ('index', 'Glue', u'Glue Documentation',
     u'Chris Beaumont, Thomas Robitaille, Michelle Borkin',
     'Glue', 'One line description of project.', 'Miscellaneous'),
]

# -- Additional options------- ------------------------------------------------

todo_include_todos = True
autoclass_content = 'both'

nitpick_ignore = [('py:obj', 'glue_qt.viewers.common.toolbar.BasicToolbar.insertAction'),
                  ('py:obj', 'glue_qt.viewers.common.toolbar.BasicToolbar.setTabOrder'),
                  ('py:class', 'glue_qt.viewers.common.toolbar.BasicToolbar'),
                  ('py:class', 'glue_qt.viewers.common.base_widget.BaseQtViewerWidget'),
                  ('py:class', 'sip.voidptr'),
                  ('py:class', 'PyQt5.sip.voidptr'),
                  ('py:class', 'PYQT_SLOT')]

nitpick_ignore_regex = [('py:class', r'PyQt5\.QtCore\.Q[a-zA-Z]+'),
                        ('py:class', r'PyQt5\.QtGui\.Q[a-zA-Z]+'),
                        ('py:class', r'PyQt5\.QtWidgets\.Q[a-zA-Z]+'),
                        ('py:class', r'PyQt6\.QtCore\.Q[a-zA-Z]+'),
                        ('py:class', r'PyQt6\.QtGui\.Q[a-zA-Z]+'),
                        ('py:class', r'PyQt6\.QtWidgets\.Q[a-zA-Z]+'),
                        ('py:class', r'PySide2\.QtCore\.Q[a-zA-Z]+'),
                        ('py:class', r'PySide2\.QtGui\.Q[a-zA-Z]+'),
                        ('py:class', r'PySide2\.QtWidgets\.Q[a-zA-Z]+'),
                        ('py:class', r'PySide6\.QtCore\.Q[a-zA-Z]+'),
                        ('py:class', r'PySide6\.QtGui\.Q[a-zA-Z]+'),
                        ('py:class', r'PySide6\.QtWidgets\.Q[a-zA-Z]+'),
                        ('py:class', r'Qt\.[a-zA-Z]+'),
                        ('py:class', r'QPalette\.[a-zA-Z]+'),
                        ('py:class', r'QWidget\.[a-zA-Z]+'),
                        ('py:class', r'Q[a-zA-Z]+')]

# coax Sphinx into treating descriptors as attributes
# see https://bitbucket.org/birkenfeld/sphinx/issue/1254/#comment-7587063
from glue_qt.utils.widget_properties import WidgetProperty
WidgetProperty.__get__ = lambda self, *args, **kwargs: self

viewcode_follow_imported_members = False

numpydoc_show_class_members = False
autosummary_generate = True
automodapi_toctreedirnm = 'api'

linkcheck_ignore = [r'https://s3.amazonaws.com']
linkcheck_retries = 5
linkcheck_timeout = 10
