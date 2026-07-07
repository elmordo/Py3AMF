=====================
 Installation Guide
=====================

.. contents::

Py3AMF 0.9.0 is a Python 3 package. CPython 3.11, 3.12, 3.13, and
3.14 are tested. Older Python 3 versions are not intentionally blocked,
but they are outside the active test matrix.


Easy Installation
=================

Install the released package with pip_::

    python -m pip install Py3AMF

The runtime dependency set is intentionally small. To install the runtime
dependencies from a source checkout::

    python -m pip install -r requirements.txt


Manual Installation
===================

:doc:`community/download` and unpack the Py3AMF archive of your choice::

    tar zxfv Py3AMF-<version>.tar.gz
    cd Py3AMF-<version>

Install the package from the source directory::

    python -m pip install .


Optional Extras
===============

The only optional extra advertised by Py3AMF 0.9.0 is lxml_ support for
XML handling::

    python -m pip install "Py3AMF[lxml]"

For source checkouts, the full test dependency set is listed in
``test-requirements.txt`` and includes lxml_.

Py3AMF 0.9.0 no longer officially supports framework integration
packages for Django, Twisted, Google App Engine, SQLAlchemy, or Elixir.
Existing adapter and gateway modules remain in the source tree for
compatibility and application-level reuse, but framework-specific object
conversion should happen in application code before values are passed to
Py3AMF.

Cython extension builds are also no longer supported. The Cython sources
remain in the tree for reference and compatibility, but installation uses
the pure Python runtime path.


Unit Tests
==========

Install the full test dependency set and run the default test suite::

    python -m pip install -r test-requirements.txt
    python -c "import pyamf.tests; pyamf.tests.main()"

The default suite covers the supported 0.9.0 surface: AMF0, AMF3, core
remoting, WSGI gateway behavior, and dependency-free helpers. Legacy
integration suites for unsupported frameworks are not part of the default
test entry point.


Documentation
=============

Sphinx
------

To build the main documentation you need:

- Sphinx_ 1.0 or newer
- `sphinxcontrib.epydoc`_ 0.4 or newer
- a :doc:`copy <community/download>` of the Py3AMF source distribution

Unix users run the command below in the ``doc`` directory to create the
HTML version of the Py3AMF documentation::

    make html

Windows users can run the make.bat file instead::

    make.bat

This will generate the HTML documentation in the ``doc/build/html``
folder.

**Note**: if you don't have the `make` tool installed then you can invoke
Sphinx from the ``doc`` directory directly like this::

    sphinx-build -b html . build

Epydoc
------

To build the API documentation you need:

- Epydoc_ 3.0 or newer
- a :doc:`copy <community/download>` of the Py3AMF source distribution

Run the command below in the root directory to create the HTML version of
the PyAMF API documentation::

    epydoc --config=setup.cfg

This will generate the HTML documentation in the ``doc/build/api``
folder.


.. _Python: 			http://www.python.org
.. _pip:                       https://pip.pypa.io/
.. _Epydoc:			http://epydoc.sourceforge.net
.. _lxml:			http://lxml.de
.. _Sphinx:     		http://sphinx.pocoo.org
.. _sphinxcontrib.epydoc:       http://packages.python.org/sphinxcontrib-epydoc
