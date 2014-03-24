Cloud-Servers
=============

Written by: necrux
3/7/2014

This program utilizes Rackspace's Python SDK (pyrax) to create a specified number of servers. There are currently 3 methods of authenticating with the API, and this program also handles SSH auth for servers.

Authenticate with ~/.rackspace_cloud_credentials File:

[rackspace_cloud]

username = my_username

api_key = 01234567890abcdef

Authenticate by passing arguments to this script.

python /path/to/this/script my_username 01234567890abcdef

    NOTE: This method trumps the ~/.rackspace_cloud_credentials file!
