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

    def exists(self, uuid):
        return self._store.exists(uuid)
    
    def _get_object(self, uuid):
        po = self._store.get_object(uuid)
        json_payload = PersistentState(po.id_to_dirpath())
        return (po, json_payload)
    
    def _setup_item(self, uuid):
        _, json_payload = self._get_object(uuid)
        json_payload['_uri'] = self.uri_base + uuid
        json_payload.sync()
    
    def claim_an_id(self):
        uuid = uuid4().hex
        while(self.exists(uuid)):
            uuid = uuid4().hex
        self._setup_item(uuid)
        return uuid
        
    def list_ids(self):
        return self._store.list_ids()
        
    def put_stream(self, uuid, stream_object, filename, params={}):
        ## QUESTION: do we enforce that the uuid's have to be 'claimed' first?
        ## NB this method doesn't care if it has been
        po, json_payload = self._get_object(uuid)
        hash_vals = po.add_bytestream_by_path(filename, stream_object)
        stat_vals = po.stat(filename)
        if '_filename' in json_payload.keys():
            # remove old file which has a different name
            po.del_file(json_payload['_filename'])
            creation_date = None
        else:
            # New upload - record creation date
            creation_date = datetime.now().isoformat().split(".")[0]  ## '2010-07-08T19:56:47'
        # Userland parameters for the file
        cleaned_params = dict( [ (k, params[k]) for k in params if not k.startswith("_")])
        json_payload.update(cleaned_params)
        # Filedetails: _filename, _numberofbytes (in bytes)
        json_payload['_filename'] = filename
        try:
            json_payload['_numberofbytes'] = int(stat_vals.st_size)
        except TypeError:
            print "Error getting filesize from os.stat().st_size into an integer..."
        if creation_date:
            json_payload['_datecreated'] = creation_date
            json_payload['_lastmodified'] = creation_date
        else:
            # Modification date
           json_payload['_lastmodified'] = datetime.now().isoformat().split(".")[0]
        # Hash details:
        if hash_vals:
            json_payload['_checksum'] = "%s:%s" % (hash_vals['type'], hash_vals['checksum'])
        json_payload.sync()
        return json_payload.state

    def get_stream(self, uuid, as_stream=True):
        if self.exists(uuid):
            po, json_payload = self._get_object(uuid)
            if '_filename' in json_payload.keys():
                return po.get_bytestream(json_payload['_filename'], streamable=as_stream, path=None, appendable=False)
        raise FileNotFoundException

    def get_stream_metadata(self, uuid):
        if self.exists(uuid):
            _, json_payload = self._get_object(uuid)
            return json_payload.state
        else:
            raise FileNotFoundException
    
    def update_stream_metadata(self, uuid, params):
        if self.exists(uuid) and isinstance(params, dict):
            _, json_payload = self._get_object(uuid)
            # Userland parameters for the file
            cleaned_params = dict([(k, params[k]) for k in params if not k.startswith("_")])
            json_payload.update(cleaned_params)
            json_payload.sync()
            return json_payload.state
        else:
            raise FileNotFoundException
    
    def remove_metadata_keys(self, uuid, keys):
        if self.exists(uuid) and isinstance(keys, list):
            _, json_payload = self._get_object(uuid)
            for key in [x for x in keys if not x.startswith("_")]:
                if key in json_payload.keys():
                    del json_payload[key]
            json_payload.sync()
            return json_payload.state
        else:
            raise FileNotFoundException

    def del_stream(self, uuid):
        if self.exists(uuid):
            # deletes the whole object for uuid
            self._store.delete_object(uuid)
        else:
            raise FileNotFoundException
