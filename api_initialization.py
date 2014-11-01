#!/usr/bin/python

import os,pyrax,threading
from sys import argv
from pyrax import utils
from Queue import Queue
import novaclient.exceptions as nexc #Used to catch exceptions from novaclient. Reference: https://community.rackspace.com/developers/f/7/t/894
import pyrax.exceptions as pexc #Used to catch exceptions from pyrax. Reference: https://github.com/rackspace/pyrax/issues/83


def api_initialization():
    pyrax.set_setting("identity_type", "rackspace")
    try:
        progname, username, api_key = argv
        pyrax.set_credentials(username, api_key)
    except ValueError:
        if os.path.isfile(os.path.expanduser("~/.rackspace_cloud_credentials")):
            creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
            try:
                pyrax.set_credential_file(creds_file)
            except pexc.AuthenticationFailed:
                print "The credentials located in ~/.rackspace_cloud_credentials are not valid. Please provide the correct Username and API Key below.\n"
                cred_prompt()
        else:
            cred_prompt()
    except pexc.AuthenticationFailed:
        if os.path.isfile(os.path.expanduser("~/.rackspace_cloud_credentials")):
            print "The provided credentials are not valid; reverting to the ~/.rackspace_cloud_credentials file."
            creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
            try:
                pyrax.set_credential_file(creds_file)
            except pexc.AuthenticationFailed:
                print "The credentials located in ~/.rackspace_cloud_credentials are not valid. Please provide the correct Username and API Key below.\n"
                cred_prompt()
        else:
            print "The provided credentials are not valid; please enter them below.\n"
            cred_prompt()

def cred_prompt():
    print """Before we can proceed, you will need to enter your username and API key. Protip: In the future you can authenticate with the following methods:

Authenticate with ~/.rackspace_cloud_credentials File.

[rackspace_cloud]
username = my_username
api_key = 01234567890abcdef

Authenticate by passing arguments to this script.

python /path/to/this/script my_username 01234567890abcdef
    NOTE: This method trumps the ~/.rackspace_cloud_credentials file!
"""
    while True:
        username = raw_input("Rackspace Username%s" % prompt)
        api_key = raw_input("Rackspace API Key%s" % prompt)
        try:
            pyrax.set_credentials(username, api_key)
            break
        except pexc.AuthenticationFailed:
            print "The credentials provided are not valid. Please try again."
            continue
    cred_save = raw_input("Would you like for me to store these credentials in ~/.rackspace_cloud_credentials for you?%s" % ynprompt)
    if cred_save.lower().startswith("y"):
        cred_save_file = open(os.path.join(os.path.expanduser("~"), ".rackspace_cloud_credentials"), "w")
        cred_save_file.write("[rackspace_cloud]\n" + "username = " + username + "\napi_key = " + api_key + "\n")
        cred_save_file.close()   





