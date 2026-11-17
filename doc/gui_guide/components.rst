.. _new_components:

Defining New Attributes
=======================

New attributes of data items can be easily created from mathematical
operations on existing attributes. In this section, we define new
attributes for the W5 Point Source catalog from the
:ref:`tutorial <getting_started>`.

To start off, click on the **Arithmetic Attributes** tool in the toolbar:

.. figure:: images/arithmetic_toolbar.png
    :align: center
    :width: 350

A new window will appear for defining attributes. To start off, use the
drop-down menu to select the dataset for which you want to create an arithmetic
attribute. Then, click on **New arithmetic attribute**, which will open up the
equation editor. From here, set the new attribute name, then type the expression
in the box provided. Attribute names should be included in curly brackets, e.g.
``{ID}``. You can either type attribute names directly, using tab-completion
if necessary, or you can also select an attribute from the list of available
attributes and click on **Insert** to insert it into the expression.

Here we define a new attribute ``J - K`` to be the difference between the J and
the Ks magnitudes:

.. figure:: images/arithmetic_equation.png
    :align: center
    :width: 500

After clicking **OK**, the new attribute is listed in the list of arithmetic
attributes:

.. figure:: images/arithmetic_defined.png
    :align: center
    :width: 500

At this point, you could if you wished define additional attributes, or go back
and edit existing ones. Clicking **OK** again will return to the main glue
interface, from which you can now use the new arithmetic attribute(s).

Note that the expression line can include Numpy functions (prefaced with
``np.``), and functions that you define in your ``config.py`` file for Glue
(see :ref:`configuration`). For example, you could define a normalized version
of ``Jmag`` using:

.. figure:: images/arithmetic_numpy.png
    :align: center
    :width: 500

.. _expression_rules:

What can be used in expressions
-------------------------------

Expressions are saved in session files, and a session file can come from
someone else, so glue does not run expressions as arbitrary Python code.
Instead, by default, expressions are limited to the following:

* Attributes of the dataset, in curly brackets (e.g. ``{Jmag}``), numbers and
  strings, and lists and tuples of these.

* Arithmetic, comparison, logical and bitwise operators, indexing and slicing
  (e.g. ``{Jmag}[::-1]``), and conditional expressions of the form
  ``a if condition else b``.

* Numpy universal functions such as ``np.sin``, ``np.log10`` and ``np.hypot``,
  and the Numpy functions that compute values from arrays, such as ``np.mean``,
  ``np.nanmedian``, ``np.where``, ``np.clip``, ``np.percentile`` and
  ``np.cumsum``, along with the functions in ``np.linalg``, ``np.fft`` and
  ``np.random``, constants such as ``np.pi``, and data types such as
  ``np.float32``.

* The functions and constants of the Python ``math`` module (e.g.
  ``math.pi``).

* The Python functions ``abs``, ``all``, ``any``, ``bool``, ``complex``,
  ``divmod``, ``float``, ``int``, ``len``, ``max``, ``min``, ``pow``, ``round``
  and ``sum``.

* Methods of arrays that compute values, such as ``{Jmag}.mean()``,
  ``{Jmag}.astype(int)`` or ``{Jmag}.clip(0, 10)``, and properties of arrays
  such as ``{Jmag}.shape`` and ``{Jmag}.real``.

* Functions, classes and constants that are defined in your ``config.py``
  file. Note that this means things that are defined there with ``def``,
  ``class`` or by assignment - modules and functions that are only *imported*
  in ``config.py`` are not available, with the exception of Numpy functions
  that would be allowed anyway. If you want to use a function from another
  package, define a function that calls it in ``config.py``::

      from scipy.ndimage import gaussian_filter1d

      def smooth(values, width):
          return gaussian_filter1d(values, width)

  after which ``smooth({Jmag}, 3)`` can be used in expressions.

Anything else is not allowed by default. This includes:

* Python functions other than the ones listed above, such as ``open``,
  ``eval``, ``getattr`` or ``__import__``.

* Numpy functions that read or write files or that wrap other code, such as
  ``np.load``, ``np.save``, ``np.loadtxt``, ``np.vectorize`` or
  ``np.frompyfunc``, and methods of arrays that write files or change data in
  place, such as ``tofile``, ``dump``, ``byteswap`` or ``fill``.

* Access to modules other than ``np`` and ``math``, and to attributes with
  names that start with an underscore.

* Methods of strings, and Python syntax other than what is described above,
  such as ``lambda`` functions, list comprehensions and assignments.

Using expressions that are not allowed by default
-------------------------------------------------

If you type an expression that uses something that is not allowed by default
in the equation editor, the reason is shown at the bottom of the window and
the **OK** button is disabled. A checkbox labelled **Allow this expression to
use functions that are not allowed by default** also appears. Ticking it
allows that specific expression to use any Python function as well as
everything that is imported in your ``config.py`` file, and the choice is
reset if you change the expression. ``lambda`` functions, comprehensions and
other syntax that is not supported cannot be enabled in this way, and the
expression remains invalid if the checkbox is ticked - define a function in
``config.py`` instead.

The choice to allow an expression is not stored in session files. When you
open a session file that contains expressions that are not allowed by
default - whether you created the file or received it from someone else - glue
lists these expressions along with the reason each one is not allowed, and
asks you which ones to allow:

* **Disallow all** (the default) loads the session without evaluating any of
  the listed expressions.

* **Allow selected** evaluates only the expressions you have ticked in the
  list.

* **Allow all** evaluates all the listed expressions.

* **Cancel** does not load the session.

The attributes for expressions that are not allowed will be filled with NaN
values. You can allow such an expression later on by opening it from the
**Arithmetic Attributes** window and ticking the checkbox described above.

.. warning:: An expression that you allow can run arbitrary code on your
             computer, so only allow expressions from a session file if you
             trust the source of the file and have checked what the
             expressions do.

When loading a session from Python, the expressions to allow can be passed to
:meth:`~glue.core.application_base.Application.restore_session` using the
``allowed_expressions`` argument, and the expressions in a file that are not
allowed by default can be listed with
``glue.core.state.find_unsafe_expressions``.
