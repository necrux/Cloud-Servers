#!/usr/bin/env python

import os,pyrax,threading,argparse,time
from pyrax import utils
from Queue import Queue
from threading import Thread
import novaclient.exceptions as nexc #Used to catch exceptions from novaclient. Reference: https://community.rackspace.com/developers/f/7/t/894
import pyrax.exceptions as pexc #Used to catch exceptions from pyrax. Reference: https://github.com/rackspace/pyrax/issues/83


def build_server(var):
    
    try:
        print "Getting job from queue..."
        server_name = var['q'].get()
        if ssh_auth == "y":
            print "Connecting to cloud to build server %s" % server_name
            print "print inside of try - before pyrax"
            server = pyrax.connect_to_cloudservers(region=var['region']).servers.create(server_name, var['srv_id'], var['flv_id'], key_name=var['auth'])
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
def build_threads(var):
    count = 1
    for i in range(var['qsize']):
        #print "setting up worker thread %d" % count
        worker = Thread(target=var['method'], args=(var,))
        worker.setDaemon(True)
        worker.start()
        count += 1



