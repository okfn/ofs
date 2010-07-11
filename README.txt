Blobstore

Usage:

(local version - depends on 'pairtree', and 'simplejson')

>>> from ofs.local import OFS

>>> o = OFS()
(Equivalent to 'o = OFS(storage_dir = "data", uri_base="urn:uuid:", hashing_type="md5")')

# Claim an id - this will prevent other processes from claiming the same one
>>> uuid_id = o.claim_an_id()
>>> uuid_id
'4aaa43cdf5ba44e2ad25acdbd1cf2f70'

# Store a file:
>>> response = o.put_stream(uuid_id, open("foo....), "foo.txt")
{'_datecreated': '2010-07-08T20:33:24', '_checksum': 'md5:3d690d7e0f4479c5a7038b8a4572d0fe', '_filename': 'foo.txt', '_uri': 'urn:uuid:4aaa43cdf5ba44e2ad25acdbd1cf2f70', '_lastmodified': '2010-07-08T20:33:24', '_numberofbytes': 26}

# or:
>>> o.put_stream(uuid_id, "asidaisdiasjdiajsidjasidji", "foo.txt")
{'_datecreated': '2010-07-08T20:33:24', '_checksum': 'md5:3d690d7e0f4479c5a7038b8a4572d0fe', '_filename': 'foo.txt', '_uri': 'urn:uuid:4aaa43cdf5ba44e2ad25acdbd1cf2f70', '_lastmodified': '2010-07-08T20:33:24', '_numberofbytes': 26}

# adding a file with some parameters:
>>> o.put_stream(uuid_id, "asidaisdiasjdiajsidjasidji", "foo.txt", params={"original_uri":"http://...."})
{'original_uri': 'http://....', '_checksum': 'md5:3d690d7e0f4479c5a7038b8a4572d0fe', '_datecreated': '2010-07-08T20:33:24', '_lastmodified': '2010-07-08T20:33:29', '_uri': 'urn:uuid:4aaa43cdf5ba44e2ad25acdbd1cf2f70', '_filename': 'foo.txt', '_numberofbytes': 26}

# adding to existing metadata:
>>> o.update_stream_metadata(uuid_id, {'foo':'bar'})
{'original_uri': 'http://....', '_filename': 'foo.txt', '_checksum': 'md5:3d690d7e0f4479c5a7038b8a4572d0fe', '_datecreated': '2010-07-08T20:33:24', '_uri': 'urn:uuid:4aaa43cdf5ba44e2ad25acdbd1cf2f70', '_lastmodified': '2010-07-08T20:33:29', 'foo': 'bar', '_numberofbytes': 26}

# Remove keys
>>> o.remove_metadata_keys(uuid_id, ['foo'])
{'original_uri': 'http://....', '_checksum': 'md5:3d690d7e0f4479c5a7038b8a4572d0fe', '_filename': 'foo.txt', '_lastmodified': '2010-07-08T20:33:29', '_uri': 'urn:uuid:4aaa43cdf5ba44e2ad25acdbd1cf2f70', '_datecreated': '2010-07-08T20:33:24', '_numberofbytes': 26}

# Delete blob
>>> o.exists(uuid_id)
True
>>> o.del_stream(uuid_id)
>>> o.exists(uuid_id)
False

# Iterate through ids for blobs held:
>>> for item in o.list_ids():
...   print item
... 
447536aa0f1b411089d12399738ede8e
4a726b0a33974480a2a26d34fa0d494d
4aaa43cdf5ba44e2ad25acdbd1cf2f70
.... etc


