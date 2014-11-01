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