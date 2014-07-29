# coding=utf-8
import os
import json
import unittest
import hashlib
from selectel.storage import Storage


class TestsStorage(unittest.TestCase):
    def setUp(self):
        current = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current, "credentials.json")) as file:
            credentials = json.loads(file.read())
            self.auth = credentials["auth"]
            self.key = credentials["key"]
        self.storage = Storage(self.auth, self.key)
        with open(__file__, "rb") as file:
            self.data = file.read()
        self.etag = hashlib.md5(self.data).hexdigest()
        self.storage.create("unittest")

    def test_content(self):
        self.storage.put("unittest", "/test1.file", self.data)
        l = self.storage.list("unittest", "/")
        self.assertEquals(l["/test1.file"]["hash"], self.etag)
        d = self.storage.get("unittest", "/test1.file")
        self.assertEquals(self.data, d)
        self.storage.remove("unittest", "/test1.file")

    def test_put_file(self):
        self.storage.put_file("unittest", "/test2.file", __file__)
        d = self.storage.get("unittest", "/test2.file")
        self.assertEquals(self.data, d)

    def test_put_stream(self):
        self.storage.put_stream("unittest", "/test2.file",
                                open(__file__, 'r+b'), chunk=256)
        d = self.storage.get("unittest", "/test2.file")
        self.assertEquals(self.data, d)

    def test_get_stream(self):
        self.storage.put("unittest", "/test2.file", self.data)
        d = b""
        for chunk in self.storage.get_stream("unittest", "/test2.file",
                                             chunk=256):
            d += chunk
        self.assertEquals(self.data, d)

    def test_copy(self):
        self.storage.put("unittest", "/test3.file", self.data)
        self.storage.copy("unittest", "/test3.file", "/test4.file")
        d = self.storage.get("unittest", "/test4.file")
        self.assertEquals(self.data, d)

    def test_list(self):
        self.storage.put("unittest", "/test5.file", self.data)
        self.storage.put("unittest", "/test6.file", self.data)
        self.storage.put("unittest", "/dir/test7.file", self.data)
        l1 = self.storage.list("unittest", "/")
        self.assertEquals(set(["/test5.file", "/test6.file"]), set(l1.keys()))
        l2 = self.storage.list("unittest", "/dir")
        self.assertEquals(["/dir/test7.file"], list(l2.keys()))
        l3 = self.storage.list("unittest")
        self.assertEquals(set(["/dir/test7.file",
                               "/test5.file", "/test6.file"]),
                          set(l3.keys()))

    def test_info(self):
        self.storage.put("unittest", "/test8.file", self.data)
        self.storage.put("unittest", "/test9.file", self.data)
        info = self.storage.info("unittest")
        self.assertEquals(info["count"], 2)
        self.assertEquals(info["public"], False)
        self.assertTrue("tx" in info)
        self.assertTrue("rx" in info)
        self.assertTrue("usage" in info)
        info = self.storage.info("unittest", "/test9.file")
        self.assertEquals(info["downloads"], 0)
        self.assertEquals(self.etag, info["hash"])
        self.assertEquals(info["content-length"], len(self.data))
        self.assertTrue("content-type" in info)
        self.assertTrue("last-modified" in info)

    def tearDown(self):
        self.storage.drop("unittest", force=True, recursive=True)
