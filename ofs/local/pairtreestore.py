#!/usr/bin/env python

from __future__ import with_statement

from storedjson import PersistentState

from pairtree import PairtreeStorageClient
from pairtree import id_encode, id_decode
from pairtree import FileNotFoundException, ObjectNotFoundException

from datetime import datetime

from uuid import uuid4

class OFSNotFound(Exception):
    pass

class OFS(object):
    def __init__(self, storage_dir="data", uri_base="urn:uuid:", hashing_type="md5"):
        self.storage_dir = storage_dir
        self.uri_base = uri_base
        self.hashing_type = hashing_type
        self._open_store()
    
    def _open_store(self):
        if self.hashing_type:
            self._store = PairtreeStorageClient(self.uri_base, self.storage_dir, shorty_length=2, hashing_type=self.hashing_type)
        else:
            self._store = PairtreeStorageClient(self.uri_base, self.storage_dir, shorty_length=2)

    def exists(self, bucket, label=None):
        if self._store.exists(bucket):
            if label:
                return self._store.isfile(bucket, label)
            else:
                return True
    
    def _get_object(self, bucket, label):
        po = self._store.get_object(bucket)
        json_payload = PersistentState(po.id_to_dirpath())
        if not json_payload.has_key(bucket):
            json_payload[bucket] = {}
        return (po, json_payload)
    
    def _setup_item(self, bucket):
        _, json_payload = self._get_object(bucket)
        json_payload[bucket]['_uri'] = self.uri_base + bucket
        json_payload.sync()
    
    def claim_a_bucket(self):
        uuid = uuid4().hex
        while(self.exists(uuid)):
            uuid = uuid4().hex
        self._setup_item(uuid)
        return uuid
        
    def list_ids(self):
        return self._store.list_ids()
        
    def put_stream(self, bucket, label, stream_object, params={}):
        ## QUESTION: do we enforce that the bucket's have to be 'claimed' first?
        ## NB this method doesn't care if it has been
        po, json_payload = self._get_object(bucket)
        stat_vals = po.stat(label)
        
        if '_filename' in json_payload[bucket].keys():
            # remove old file which has a different name
            po.del_file(json_payload[bucket]['_filename'])
            creation_date = None
        else:
            # New upload - record creation date
            creation_date = datetime.now().isoformat().split(".")[0]  ## '2010-07-08T19:56:47'

        hash_vals = po.add_bytestream_by_path(label, stream_object)
        # Userland parameters for the file
        cleaned_params = dict( [ (k, params[k]) for k in params if not k.startswith("_")])
        json_payload[bucket].update(cleaned_params)
        # Filedetails: _filename, _numberofbytes (in bytes)
        json_payload[bucket]['_filename'] = filename
        try:
            json_payload[bucket]['_content_length'] = int(stat_vals.st_size)
        except TypeError:
            print "Error getting filesize from os.stat().st_size into an integer..."
        if creation_date:
            json_payload[bucket]['_creation_date'] = creation_date
            json_payload[bucket]['_last_modified'] = creation_date
        else:
            # Modification date
           json_payload[bucket]['_last_modified'] = datetime.now().isoformat().split(".")[0]
        # Hash details:
        if hash_vals:
            json_payload[bucket]['_checksum'] = "%s:%s" % (hash_vals['type'], hash_vals['checksum'])
        json_payload.sync()
        return json_payload.state

    def get_stream(self, bucket, label, as_stream=True):
        if self.exists(bucket):
            po, json_payload = self._get_object(bucket)
            if '_filename' in json_payload[bucket].keys():
                return po.get_bytestream(json_payload[bucket]['_filename'], streamable=as_stream, path=None, appendable=False)
        raise FileNotFoundException

    def get_metadata(self, bucket, label):
        if self.exists(bucket):
            _, json_payload = self._get_object(bucket)
            return json_payload.state[bucket]
        else:
            raise FileNotFoundException
    
    def update_stream_metadata(self, bucket, label, params):
        if self.exists(bucket) and isinstance(params, dict):
            _, json_payload = self._get_object(bucket)
            # Userland parameters for the file
            cleaned_params = dict([(k, params[k]) for k in params if not k.startswith("_")])
            json_payload[bucket].update(cleaned_params)
            json_payload.sync()
            return json_payload.state[bucket]
        else:
            raise FileNotFoundException
    
    def remove_metadata_keys(self, bucket, label, keys):
        if self.exists(bucket) and isinstance(keys, list):
            _, json_payload = self._get_object(bucket)
            for key in [x for x in keys if not x.startswith("_")]:
                if key in json_payload[bucket].keys():
                    del json_payload[bucket][key]
            json_payload[bucket].sync()
            return json_payload.state[bucket]
        else:
            raise FileNotFoundException

    def del_stream(self, bucket, label):
        if self.exists(bucket, label):
            # deletes the whole object for uuid
            self._store.del_stream(bucket, label)
        else:
            raise FileNotFoundException
