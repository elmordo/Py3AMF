============
  Features
============

Here's a brief description of the features in Py3AMF. The
:doc:`CHANGES <../changelog>` document contains a more detailed
summary of all new features.

- :mod:`AMF0 <pyamf.amf0>` encoder/decoder for legacy Adobe Flash Players (version 6-8)
- :mod:`AMF3 <pyamf.amf3>` encoder/decoder for the new AMF format in Adobe Flash Player 9
  and newer
- Support for ``IExternalizable``, :class:`ArrayCollection <pyamf.flex.ArrayCollection>`,
  :class:`ObjectProxy <pyamf.flex.ObjectProxy>`, :class:`ByteArray <pyamf.amf3.ByteArray>`,
  :class:`RecordSet <pyamf.amf0.RecordSet>`, ``RemoteObject`` and ``more``
- Core remoting support and a WSGI_ gateway for Python web applications
- :doc:`Adapter helper modules <../architecture/adapters>` for built-in
  Python types and legacy application-level reuse
- :doc:`Authentication <../tutorials/general/authentication/index>`/``setCredentials`` support
- Python AMF :doc:`client <../tutorials/general/client>` with HTTP(S)
  and authentication support
- Service Browser requests supported
- :doc:`Local Shared Object <../tutorials/general/sharedobject>`
  support

Also see the our plans for :doc:`future development <future>`.


.. _WSGI: http://wsgi.org
