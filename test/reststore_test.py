import random, unittest
from ofs.remote.reststore import RESTOFS
from ofs import OFSException
from six import StringIO
import os

TEST_TEXT = """I am a banana"""
BINARY_FILE_NAME = os.path.join(os.path.dirname(__file__), 'binary.data')

class TestRESTOFS(unittest.TestCase):

    def setUp(self):
        self.bucket_name = 'ofs-test-bucket'
        self.host_name = 'http://127.0.0.1:5000/'
        self.ofs = RESTOFS(self.host_name)
        self.ofs.claim_bucket(self.bucket_name)

    def tearDown(self):
        self.ofs._del_bucket(self.bucket_name)

    def _makefp(self):
        return StringIO(TEST_TEXT)

    def test_exists(self):
        # check for bucket only:
        self.assertTrue(self.ofs.exists(self.bucket_name))

    def test_claim_bucket(self):
        bucket_name = 'fresh-test-bucket'
        self.ofs._del_bucket(bucket_name)
        self.assertFalse(self.ofs.exists(bucket_name))
        self.assertTrue(self.ofs.claim_bucket(bucket_name))
        self.assertTrue(self.ofs.exists(bucket_name))
        self.assertFalse(self.ofs.claim_bucket(bucket_name))

        self.ofs._del_bucket(bucket_name)
        self.assertFalse(self.ofs.exists(bucket_name))

    def test_list_buckets(self):
        buckets = [b for b in self.ofs.list_buckets()]
        assert len(buckets) > 0, len(buckets)
        assert self.bucket_name in buckets, buckets

    def test_stream_write_and_read(self):
        name = "my_data.txt"
        self.ofs.put_stream(self.bucket_name, name, self._makefp())
        text = self.ofs.get_stream(self.bucket_name, name).read()
        assert text == TEST_TEXT, text
        text = self.ofs.get_stream(self.bucket_name, name, as_stream=False)
        assert text == TEST_TEXT, text

    def test_binary_write_and_read(self):
        name = "binary.data"
        fh = file(BINARY_FILE_NAME, 'rb')
        self.ofs.put_stream(self.bucket_name, name, fh)
        fh.close()

    def test_stream_delete(self):
        name = "my_data.txt"
        self.ofs.put_stream(self.bucket_name, name, self._makefp())
        assert self.ofs.get_stream(self.bucket_name, name) != None, name
        self.ofs.del_stream(self.bucket_name, name)
        self.assertRaises(OFSException, self.ofs.get_stream, self.bucket_name, name)

    def test_meta_save_read(self):
        name = "my_data.txt"
        self.ofs.put_stream(self.bucket_name, name, self._makefp(), params={'hello': 'world',
                                                                            'foo': 'bar'})
        meta = self.ofs.get_metadata(self.bucket_name, name)
        assert '_owner' in meta, meta
        assert '_creation_time' in meta, meta
        assert '_last_modified' in meta, meta
        assert '_checksum' in meta, meta
        assert '_format' in meta, meta
        assert '_bucket' in meta, meta
        assert '_label' in meta, meta
        assert '_content_length' in meta, meta
        assert meta['hello'] == 'world', meta['hello']
        assert meta['foo'] == 'bar', meta['bar']

    def test_meta_update(self):
        name = "my_data.txt"
        self.ofs.put_stream(self.bucket_name, name, self._makefp(), params={'hello': 'world',
                                                                            'foo': 'bar'})
        meta = self.ofs.get_metadata(self.bucket_name, name)
        assert meta['hello'] == 'world', meta['hello']
        assert meta['foo'] == 'bar', meta['bar']
        self.ofs.update_metadata(self.bucket_name, name, {'hello': 'mars',
                                                          'foo': 'qux'})
        meta = self.ofs.get_metadata(self.bucket_name, name)
        #print meta
        assert meta['hello'] == 'mars', meta['hello']
        assert meta['foo'] == 'qux', meta['bar']

    def test_meta_special_fields(self):
        name = "my_data.txt"
        self.ofs.put_stream(self.bucket_name, name, self._makefp(), params={'_format': 'application/x.banana'})
        meta = self.ofs.get_metadata(self.bucket_name, name)
        assert meta['_format'] == 'application/x.banana', meta['_format']
        assert meta['_content_length'] == len(TEST_TEXT), meta['_content_length']


if __name__ == '__main__':
    unittest.main()
