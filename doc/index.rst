Welcome to OFS File Storage (OFS) Documentation
===============================================

OFS is a bucket/object storage library.

It provides a common API for storing bitstreams (plus related metadata) in
'bucket/object' stores such as:

  * S3, Google Storage, Eucalytus, Archive.org
  * Filesystem (via pairtree and other methods)
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

Abstract Interface
==================

Interface that must be implemented by all OFS backends.

.. autoclass:: ofs.base.OFSInterface
   :members:


Pairtree Backend: Local Filesystem based using Pairtree
=======================================================

.. autoclass:: ofs.local.pairtreestore.PTOFS
   :members:

LocalFile Store: Ultra-Simple Local File System
===============================================

.. warning:: Not yet implemented.

.. autoclass:: ofs.local.filestore.LocalFileOFS
   :members:

Metadata Store: Local File System with Metadata Focus
=====================================================

.. autoclass:: ofs.local.metadatastore.MDOFS
   :members:

ZipStore: OFS Storage Backed onto Zipfile
=========================================

.. autoclass:: ofs.local.zipstore.ZOFS
   :members:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

