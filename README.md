Cloud-Servers
=============

Written by: necrux<br>
3/7/2014

This program utilizes Rackspace's Python SDK (pyrax) to create a specified number of servers. There are currently 3 methods of authenticating with the API, and this program also handles SSH auth for servers.
<br>
Authenticate with ~/.rackspace_cloud_credentials File:
<br>
[rackspace_cloud]<br>
username = my_username<br>
api_key = 01234567890abcdef<br>
<br>
Authenticate by passing arguments to this script.
<br>
python /path/to/this/script my_username 01234567890abcdef<br>
    NOTE: This method trumps the ~/.rackspace_cloud_credentials file!
