# Roadmap

## Py3AMF 0.9.0

Py3AMF 0.9.0 narrows the project scope to a modern, pure Python AMF
implementation with a small supported surface.

### Supported

- Test CPython 3.11, 3.12, 3.13, and 3.14.
- Keep installation open for older Python 3 versions when possible. Older
  versions are not actively tested, but they are not intentionally blocked.
- Support AMF0 and AMF3 encoding and decoding.
- Support core remoting behavior.
- Support the WSGI gateway as the only core gateway.
- Keep the pure Python implementation as the supported runtime path.
- Keep `pyamf.adapters` helper modules available.

### No Longer Officially Supported

- Jython.
- Cython extension builds.
- Twisted gateway integration.
- Django gateway integration.
- Google App Engine gateway integration.
- Django, SQLAlchemy, Elixir, and Google App Engine adapter integrations.
- Automatic conversion of third-party framework models.

### Compatibility Policy

Existing Cython sources and third-party adapter modules should remain in the
source tree for compatibility, reference, and application-level reuse. They are
not part of the actively tested support surface for 0.9.0.

Applications should convert framework-specific objects at the application layer
before passing data to Py3AMF. The project should not try to track every major
version change in Django, SQLAlchemy, Google App Engine, Elixir, or similar
frameworks.

### Test Policy

The default test suite should focus on:

- AMF0 and AMF3 codecs.
- Core type registration and alias behavior.
- Core remoting.
- WSGI gateway behavior.
- Dependency-free helper modules.

The default test suite should exclude legacy integration tests for:

- Twisted.
- Django.
- Google App Engine.
- SQLAlchemy.
- Elixir.
- Cython extension builds.
