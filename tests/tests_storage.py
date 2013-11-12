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
        with open(__file__) as file:
            self.data = file.read()
        self.etag = hashlib.md5(self.data).hexdigest()
        self.storage.create("unittest")

    def test_content(self):
        h = self.storage.put("unittest", "/test1.file", self.data)
        self.assertEquals(h["etag"], self.etag)
        l = self.storage.list("unittest", "/")
        self.assertEquals(l["test1.file"]["hash"], self.etag)
        d = self.storage.get("unittest", "/test1.file")
        self.assertEquals(self.data, d[0])
        self.assertEquals(self.etag, d[1]["etag"])
        self.storage.remove("unittest", "/test1.file")

    def test_save_file(self):
        h = self.storage.save_file("unittest", "/test2.file", __file__)
        self.assertEquals(h["etag"], self.etag)
        d = self.storage.get("unittest", "/test2.file")
        self.assertEquals(self.data, d[0])
        self.assertEquals(self.etag, d[1]["etag"])

    def test_copy(self):
        self.storage.create("unittest")
        h = self.storage.put("unittest", "/test3.file", self.data)
        self.assertEquals(h["etag"], self.etag)
        self.storage.copy("unittest", "/test3.file", "/test4.file")
        d = self.storage.get("unittest", "/test4.file")
        self.assertEquals(self.data, d[0])
        self.assertEquals(self.etag, d[1]["etag"])

    def tearDown(self):
        l = self.storage.list("unittest", "/")
        for filename in l.keys():
            self.storage.remove("unittest", "/" + filename)
        self.storage.drop("unittest")
