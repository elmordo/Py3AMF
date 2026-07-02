*********************
  Adapter Framework 
*********************

.. topic:: Introduction

   The Adapter Framework contains helper modules for type conversions, class
   mappings, and compatibility code. In Py3AMF 0.9.0 these modules are kept
   for application-level reuse, but framework-specific automatic conversion is
   not part of the officially supported surface.


Adapters Overview
=================

Py3AMF includes helper modules for:

- :py:mod:`sets` module
- :py:mod:`decimal` module
- legacy Django, Google App Engine, SQLAlchemy, and Elixir integrations


How It Works
============

The adapter framework can register import callbacks by adding a module loader
and finder to :py:data:`sys.meta_path`. This allows helper code to be loaded
when a matching module is imported and accessed.

It is important to note that Py3AMF does not load all the modules when
registering its adapters and therefore it doesn't load modules that you
don't use in your program.

Applications should not rely on Py3AMF to keep pace with major framework
changes. Convert framework-specific objects into plain Python data at the
application layer before encoding them with Py3AMF.


Building Your Own Adapter
=========================

Your custom module:

.. literalinclude:: examples/adapters/mymodule.py
   :linenos:

Glue code:

.. literalinclude:: examples/adapters/myadapter.py
   :linenos:

And you're done!


What next?
==========

:doc:`Contributions</bugs>` (including unit tests) are always welcome!
