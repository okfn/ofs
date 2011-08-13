===============================================
Welcome to OFS File Storage (OFS) Documentation
===============================================

OFS is a bucket/object storage library.

It provides a common API for storing bitstreams (plus related metadata) in
'bucket/object' stores such as:

  * S3-like: S3, Google Storage, Eucalytus, Archive.org
  * Filesystem (via pairtree and other methods)
  * 'REST' Store (see remote/reststore.py - implementation at http://bitbucket.org/pudo/repod/)
  * **add a backend here** - just implement the methods in base.py

Why use the library:

  * Abstraction: write common code but use different storage backends
  * More than a filesystem, less than a database - support for metadata as well
    bitstreams


OFS Interface
~~~~~~~~~~~~~

Interface that must be implemented by all OFS backends.

.. autoclass:: ofs.base.OFSInterface
   :members:

Backends
~~~~~~~~

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

S3
==

.. autoclass:: ofs.remote.botostore.S3OFS
   :members:

Google Storage
==============

.. autoclass:: ofs.remote.botostore.GSOFS
   :members:

Archive.org OFS
===============

.. autoclass:: ofs.remote.botostore.ArchiveOrgOFS
   :members:

ProxyStore (Bounce for S3-type stores)
======================================

.. autoclass:: ofs.remote.proxystore.S3Bounce
   :members:

REST OFS: OFS Interface to RESTFul storage system
=================================================

.. autoclass:: ofs.remote.reststore.RESTOFS
   :members:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

