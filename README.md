Cloud-Servers
=============

Written by: necrux<br>
3/7/2014<br>
Forked by jay13yaj<br>
10/11/2014

Syntax: python create_servers.py<br>
	the prompts will guide you through the creation process.

This program utilizes Rackspace's Python SDK (pyrax) to create a specified number of servers. There are currently 3 methods of authenticating with the API, and this program also handles SSH auth for servers.
<br><br>
In order to run this program, you will have to install Python v2, pip, and pyrax:<br>
python -V; yum install python-pip -y && pip install pyrax
<br><br>
If you are running this from a Cloud Server that is running the wrong version of pip, you will need to install the correct version using easy_install:<br>
1) Download setup-tools according to your python version: https://pypi.python.org/pypi/setuptools<br>
2) Run easy_install pip<br>
&nbsp;&nbsp;&nbsp;&nbsp;REFERENCE FOR easy_install: http://blog.troygrosfield.com/2010/12/18/installing-easy_install-and-pip-for-python/
<br><br>
Authenticate with ~/.rackspace_cloud_credentials File:
<br>
[rackspace_cloud]<br>
username = my_username<br>
api_key = 01234567890abcdef
<br><br>
Authenticate by passing arguments to this scrip:t
<br>
python /path/to/this/script my_username 01234567890abcdef<br>
&nbsp;&nbsp;&nbsp;&nbsp;NOTE: This method trumps the ~/.rackspace_cloud_credentials file!
