OFS documentation
=================

OFS is a bucket/object storage library.

It provides a common API for storing bitstreams (plus related metadata) in
'bucket/object' stores such as:

  * S3, Google Storage, Eucalytus, Archive.org
  * Filesystem (via pairtree)
  * 'REST' Store (see remote/reststore.py - implementation at http://bitbucket.org/pudo/repod/)
  * Riak (buggy)
  * **add a backend here** - just implement the methods in base.py

Why use the library:

  * Abstraction: write common code but use different storage backends
  * More than a filesystem, less than a database - support for metadata as well
    bitstreams

Contents:

.. toctree::
   :maxdepth: 2


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

