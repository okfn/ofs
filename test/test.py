# -*- coding: utf-8 -*-
import random, unittest, re

import shutil

from ofs.local import OFS as PTOFS

class TestPairtreeOFS(unittest.TestCase):
   
    def setUp(self):
        self.o = PTOFS(storage_dir="pt_deleteme")

    def tearDown(self):
        shutil.rmtree("pt_deleteme")

    def test_empty(self):
        pass
    
    def test_claimid(self):
        a = self.o.claim_an_id()
        self.assertTrue(self.o.exists(a))
    
    def test_store_bytes_no_params(self):
        a = self.o.claim_an_id()
        b = self.o.put_stream(a, "Some bytes to store", "foo.txt")
        self.assertEquals(b['_filename'], "foo.txt")
        self.assertEquals(b['_numberofbytes'], 19)
        self.assertEquals(b['_checksum'], 'md5:eee89bbbcf416f658c7bc18cd8f2b61d')
    
    def test_store_bytes_with_params(self):
        a = self.o.claim_an_id()
        b = self.o.put_stream(a, "Some bytes to store", "foo.txt", {"a":"1", "b":[1,2,3,4,5]})
        self.assertEquals(b['a'], "1")
        self.assertEquals(b['b'], [1,2,3,4,5])
    
    def test_store_params_after_bytes(self):
        a = self.o.claim_an_id()
        self.o.put_stream(a, "Some bytes to store", "foo.txt")
        b = self.o.update_stream_metadata(a, {"a":"1", "b":[1,2,3,4,5]})
        self.assertEquals(b['a'], "1")
        self.assertEquals(b['b'], [1,2,3,4,5])
        
    def test_params_persistence(self):
        a = self.o.claim_an_id()
        self.o.put_stream(a, "Some bytes to store", "foo.txt", {"a":"1", "b":[1,2,3,4,5]})
        b = self.o.get_stream_metadata(a)        
        self.assertEquals(b['a'], "1")
        self.assertEquals(b['b'], [1,2,3,4,5])
        
    def test_params_deletion(self):
        a = self.o.claim_an_id()
        self.o.put_stream(a, "Some bytes to store", "foo.txt", {"a":"1", "b":[1,2,3,4,5]})
        self.o.remove_metadata_keys(a, ['b'])
        b = self.o.get_stream_metadata(a)        
        self.assertEquals(b['a'], "1")
        self.assertFalse(b.has_key('b'))        
        
if __name__ == '__main__':
    unittest.main()
