#!/usr/bin/python

"""
Written by: necrux
3/7/2014

Forked by: jay13yaj
10/22/2014

This program utilizes Rackspace's Python SDK (pyrax) to create a specified number of servers.

Known Issues:

Possible Improvements:
 Give the user the option to wait for networking information.

Enjoy!
"""

import os,pyrax,threading,argparse,time
from sys import argv
from pyrax import utils
from Queue import Queue
from api_initialization import *
from server_selection import *
#from build_server import *
from threading import Thread
import novaclient.exceptions as nexc #Used to catch exceptions from novaclient. Reference: https://community.rackspace.com/developers/f/7/t/894
import pyrax.exceptions as pexc #Used to catch exceptions from pyrax. Reference: https://github.com/rackspace/pyrax/issues/83



# Removed API init and credentials prompt into seperate file for security and readability reasons.
# Still need to add crypto-functions to the API keys and whatnot
# Moved remaining functions to server_selection.py


# START user prompts

os.system("clear")
print "SERVER CREATION BADASSERY\n".center(75)

#set up consistent prompts
prompt = "\n   >>> "
ynprompt = "\n   >>>(y/N) "

# Run methods to set server information
api_initialization()
region = region_selection()
server_type, server_id = server_selection(region)
server_flv_type, server_flv_id = flv_selection(region)


# Get number of servers to create and their naming convention
while True:
    server_count = raw_input("\nHow many of these servers would you like to create?%s" % prompt) #Number of servers to be created.
    try:
        server_count = int(server_count)
        break
    except ValueError:
        print "Not a valid entry."

naming_con = raw_input("\nDesired naming convention prefix? (ex. 'www' or 'db')%s" % prompt) #User defined naming convention.

#SSH Authentication
if not os.path.isfile(os.path.expanduser("~/.ssh/id_rsa.pub")) and not os.path.isfile(os.path.expanduser("~/.ssh/id_rsa.pub")):
    ssh_auth = raw_input("I see that you currently do not have SSH keys set up on this server. Would you like to create keys for use with the new server(s)?%s" % ynprompt)
    if ssh_auth.lower().startswith("y"):
        ssh_auth = "y"
        os.system("ssh-keygen -f ~/.ssh/id_rsa -N ''")
elif os.path.isfile(os.path.expanduser("~/.ssh/id_rsa.pub")):
    ssh_auth = raw_input("I see that you currently have a public key setup at ~/.ssh/id_rsa.pub. Do you want to add that to the server as a method of authentication?%s" % ynprompt)
    if ssh_auth.lower().startswith("y"):
        ssh_auth = "y"
if ssh_auth == "y":
    try:
        with open(os.path.expanduser("~/.ssh/id_rsa.pub")) as keyfile:
            pyrax.connect_to_cloudservers(region=region).keypairs.create("my_key", keyfile.read())
        print "SSH key added."
    except nexc.Conflict as e:
        print "SSH key [name] already exists on server."

#Verification Section
wait_for_build = raw_input("Would you like to let the threads wait for build completion?%s" % prompt)
if not wait_for_build.lower().startswith("y"):
    wait_for_build = False


print "\nYou have chosen to create %s '%s' '%s' server(s) with the naming convention '%s[1-%s]' in %s." % (server_count, server_flv_type, server_type, naming_con, server_count, region)
print "    Note: After build completetion, server details can be found in ~/Server_Info.txt."
confirm = raw_input("Is this correct?%s" % ynprompt)
if not confirm.lower().startswith("y"):
    exit()

"""
Currently the servers are set to 'build' status, the program outputs available information, and exits. If you would like for the program to wait until
the build is complete and output IP information as well then you will need to uncomment the following 5 lines. This will add quite a bit of execution
time, especially for a large number of servers.

Additional Considerations after Uncommenting:
 * Create a second loop that runs after ALL servers have started building and outputs the server information; otherwise server build requests will be 
    done one at a time. 
 * Change the line breaks to improve formatting
 * The lists that contain the IPs with the networking dictionary do not appear to be ordered. This means that sometimes an IPv6 address will output
    rather than the IPv4 address.
 * Look into creating a Callback function.
"""
print "\n"

#Server Creation Section
server_info = open(os.path.join(os.path.expanduser("~"), "Server_Info.txt"), "a")
count = 1
build_queue = Queue()

while count <= server_count:
    server_name = "%s%s" % (naming_con, count)
    build_queue.put(server_name)
    count += 1


def build_server(q):
    
    try:
        print "Getting job from queue..."
        server_name = q.get()
        if ssh_auth == "y":
            print "Connecting to cloud to build server %s" % server_name
            print "print inside of try - before pyrax"
            server = pyrax.connect_to_cloudservers(region=region).servers.create(server_name, server_id, server_flv_id, ssh_auth)
            print "print inside of try - after pyrax"

            print "%s has started building" % server_name
            #pass
        else:
            #server = pyrax.connect_to_cloudservers(region=region).servers.create(server_name, server_id, server_flv_id)
            #pass
            print "Name:", server.name
            print "Root Password:", server.adminPass
            print "ID:", server.id
            print "Region:", region
            print "Status:", server.status, "\n\n"

        server_info.write("Name: " + server.name + "\n")
        server_info.write("ID: " + server.id + "\n")
        server_info.write("Region: " + region + "\n")
        server_info.write("Admin Password: " + server.adminPass + "\n\n")

        if wait_for_build == True:
            pyrax.utils.wait_for_build(server, "status", ["ACTIVE", "ERROR"], interval=20, callback=None, attempts=0, verbose=False, verbose_atts="progress")
            print "Public IP:", server.networks.get(u'public')[0]
            print "Private IP:", server.networks.get(u'private')[0], "\n\n"
            server_info.write("Public IP: " + server.networks.get(u'public')[0] + "\n")
            server_info.write("Private IP: " + server.networks.get(u'private')[0] + "\n\n")
        q.task_done()
        print "%s has finished, ending thread" % server_name
        

    except nexc.BadRequest as e:
        print "Bad image/flavor combination. Please try again. (wah wah wah)\n"
        exit()

# method for threading methods. pass it a function and a queue to work through.
def build_threads():
    count = 1
    for i in range(sizeq):
        #print "setting up worker thread %d" % count
        worker = Thread(target=build_server, args=(build_queue,))
        worker.setDaemon(True)
        worker.start()
        count += 1

sizeq = build_queue.qsize()
print "Size of build queue:\t%d" % sizeq

#server = pyrax.connect_to_cloudservers(region=region).servers.create(server_name, server_id, server_flv_id, key_name="my_key")

#build_vars = {'method':build_server,'q':build_queue,'qsize':sizeq,'region':region,'srv_id':server_id,'flv_id':server_flv_id,'auth':ssh_auth}


build_threads()

build_queue.join()

server_info.close()










