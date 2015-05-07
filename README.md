![pypi-version](http://img.shields.io/pypi/v/selectel--api.svg)
## selectel-api ##

Simple python module which provide access to [selectel](http://selectel.com) cloud services.

### Selectel Cloud Storage ###

#### Creating and dropping containers ####

For handle containers you should use global selectel credentials:

	>>> from selectel.storage import Storage
	>>> storage = Storage(auth, key)

You can create public and private containers with specific [headers](https://support.selectel.ru/storage/api_info/#cors):

	>>> storage.create("mycontainer")
	>>> headers = {"X-Container-Meta-Access-Control-Request-Method": "HEAD, GET"}
	>>> storage.create("mypubliccontainer", public=True, headers=headers)

and drop it:

	>>> storage.drop("mypubliccontainer")

Use `storage.drop("mypubliccontainer", recursive=True)` for dropping nonempty container.

#### Working with objects inside container ####

For working with objects you can use container specific credentials:

	>>> from selectel.storage import Container
	>>> container = Container(auth_container, key_container, "mycontainer")

You can add objects from content:

	>>> container.put("/test1.file", b"something")

from file:

	>>> container.put_file("/test2.file", "./test.zip")

or from readable stream:

	>>> container.put_stream("/dir/test3.file", open("./test.zip", "r+b"))

Optionally you can add specific headers:

	>>> container.put_stream("/dir/test3.file", open("./test.zip", "r+b"), headers={"Content-Type": "application/zip"})
	
Also you can use `put*` commands to [extract](https://support.selectel.ru/storage/api_info/#id15) archives(tar, tar.gz, tar.bz2) to container, e.g.:

    >>> container.put_file("/dir", "archive.tar.gz", extract="tar.gz")
    (18, [])

In this case put command returns count of created(overwritten) files and list of errors. 

API allows to get some info about container and objects inside it:

	>>> container.list().keys()
	[u'/test1.file', u'/dir/test3.file', u'/test2.file']
	>>> container.list("/dir").keys()
	[u'/dir/test3.file']
	>>> container.list("/").keys()
	[u'/test1.file', u'/test2.file']
	>>> container.list("/dir")["/dir/test3.file"]
	{'hash': u'29dc385f67f38be9bddac38785aea25d', 'content-length': 101974, 'content-type': u'application/zip', 'last-modified': datetime.datetime(2013, 11, 12, 13, 31, 56, 527830)}
	>>> container.info()
	{'count': 3, 'usage': 203957, 'rx': 512219, 'public': False, 'tx': 126390}
	>>> container.info("/dir/test3.file")
	{'downloads': 0, 'last-modified': datetime.datetime(2013, 11, 12, 13, 31, 56), 'content-length': 101974, 'hash': '29dc385f67f38be9bddac38785aea25d', 'content-type': 'application/zip'}

You can get content of object as string:

	>>> container.get("/test1.file")
	'something'

or as stream:

	>>> for chunk in container.get_stream("/test2.file", chunk=2**15):
	...     print len(chunk)
	...
	32768
	32768
	32768
	3670

And last that you can do:

	>>> container.copy("/dir/test3.file", "/test4.file")
	>>> container.list("/").keys()
	[u'/test4.file', u'/test1.file', u'/test2.file']
	>>> container.remove("/test1.file")
	>>> container.list("/").keys()
	[u'/test4.file', u'/test2.file']

### Running tests ###

Add file **tests/credentials.json**  with your credentials:

	{
		"auth": "my-selectel-login",
		"key": "my-selectel-password"
	}

Then, run

	tox

