# coding=utf-8
import os
import json
import unittest
import hashlib
import tarfile
import io
import requests.exceptions
import time
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
        time.sleep(5)
        l = self.storage.list("unittest", "/")
        self.assertEquals(l["/test1.file"]["hash"], self.etag)
        d = self.storage.get("unittest", "/test1.file")
        self.assertEquals(self.data, d)
        self.storage.remove("unittest", "/test1.file")

    def test_put_file(self):
        self.storage.put_file("unittest", "/test2.file", __file__)
        time.sleep(5)
        d = self.storage.get("unittest", "/test2.file")
        self.assertEquals(self.data, d)

    def test_put_file_with_invalid_token(self):
        self.storage.auth.token = "random"
        self.storage.put_file("unittest", "/test_token.file", __file__)
        time.sleep(5)
        d = self.storage.get("unittest", "/test_token.file")
        self.assertEquals(self.data, d)

    def test_put_stream(self):
        self.storage.put_stream("unittest", "/test2.file",
                                open(__file__, 'r+b'), chunk=256)
        time.sleep(5)
        d = self.storage.get("unittest", "/test2.file")
        self.assertEquals(self.data, d)

    def test_get_stream(self):
        self.storage.put("unittest", "/test2.file", self.data)
        time.sleep(5)
        d = b""
        for chunk in self.storage.get_stream("unittest", "/test2.file",
                                             chunk=256):
            d += chunk
        self.assertEquals(self.data, d)

    def test_copy(self):
        self.storage.put("unittest", "/test3.file", self.data)
        time.sleep(5)
        self.storage.copy("unittest", "/test3.file", "/test4.file")
        d = self.storage.get("unittest", "/test4.file")
        self.assertEquals(self.data, d)

    def test_list(self):
        self.storage.put("unittest", "/test5.file", self.data)
        self.storage.put("unittest", "/test6.file", self.data)
        self.storage.put("unittest", "/dir/test7.file", self.data)
        time.sleep(5)
        l1 = self.storage.list("unittest", "/")

        self.assertEquals(
            set(["/test5.file", "/test6.file", "/dir/test7.file"]),
            set(l1.keys())
        )
        l2 = self.storage.list("unittest", "/dir")
        self.assertEquals(["/dir/test7.file"], list(l2.keys()))
        l3 = self.storage.list("unittest")
        self.assertEquals(set(["/dir/test7.file",
                               "/test5.file", "/test6.file"]),
                          set(l3.keys()))
        self.storage.put(
            "unittest", "/dir/subdir/test9.file", self.data)
        self.storage.put(
            "unittest", "/dir/subdir/subdir2/test10.file", self.data)
        time.sleep(5)
        l4 = self.storage.list("unittest", prefix='dir')
        self.assertEquals(set(["/dir/test7.file",
                               "/dir/subdir/test9.file",
                               "/dir/subdir/subdir2/test10.file"]),
                          set(l4.keys()))

    def test_info(self):
        self.storage.put("unittest", "/test8.file", self.data)
        self.storage.put("unittest", "/test9.file", self.data)
        time.sleep(5)
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

    def test_archive(self):
        self.storage.put("unittest", "/test5.file", self.data[:100])
        self.storage.put("unittest", "/test6.file", self.data[:100])
        self.storage.put("unittest", "/dir/test7.file", self.data[:100])
        self.storage.put("unittest", "/dir/test8.file", self.data[:100])
        time.sleep(5)
        archive = self.create_archive()
        created, errors = self.storage.put(
            "unittest", "/", archive, extract="tar.gz")
        self.assertEquals(created, 5)
        self.assertEquals(errors, [])
        l1 = self.storage.list("unittest", "/")
        self.assertEquals(
            set(["/test5.file", "/test6.file", "/test9.file",
                 "/dir/test8.file", "/dir/test10.file", "/dir/test7.file",
                 "/dir1/test11.file"]),
            set(l1.keys()))
        l2 = self.storage.list("unittest", "/dir")
        self.assertEquals(
            set(["/dir/test7.file", "/dir/test8.file", "/dir/test10.file"]),
            set(l2.keys()))
        d1 = self.storage.get("unittest", "/test9.file")
        self.assertEquals(self.data, d1)
        d2 = self.storage.get("unittest", "/dir/test7.file")
        self.assertEquals(self.data, d2)
        d3 = self.storage.get("unittest", "/test6.file")
        self.assertEquals(self.data, d3)
        d4 = self.storage.get("unittest", "/dir/test10.file")
        self.assertEquals(self.data, d4)
        d5 = self.storage.get("unittest", "/dir/test8.file")
        self.assertEquals(self.data[:100], d5)
        d6 = self.storage.get("unittest", "/test5.file")
        self.assertEquals(self.data[:100], d6)
        d7 = self.storage.get("unittest", "/dir1/test11.file")
        self.assertEquals(self.data, d7)

    def create_archive(self):
        buffer = io.BytesIO()
        archive = tarfile.open(mode="w:gz", fileobj=buffer)
        fileobj = open(__file__, "r+b")
        for name in ["/test9.file", "/dir/test7.file",
                     "/dir/test10.file", "test6.file",
                     "/dir1/test11.file"]:
            archive.addfile(
                archive.gettarinfo(
                    arcname=name,
                    fileobj=fileobj),
                fileobj=fileobj)
            fileobj.seek(0)
        archive.close()
        fileobj.close()
        return buffer.getvalue()

    def tearDown(self):
        while True:
            try:
                self.storage.drop("unittest", force=True, recursive=True)
            except requests.exceptions.HTTPError:
                pass
            else:
                return
