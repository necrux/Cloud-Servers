#!/usr/bin/env python

import pyrax

prompt = "\n   >>> "
ynprompt = "\n   >>>(y/N) "

# Select region. Need to add yaml file for defaults for all of these functions to enable speedy creation.
def region_selection():
    print """\nWhat region would you like to build in?

1) DFW
2) ORD
3) IAD
4) SYD
5) HKG
6) LON
"""
    # Changing from long if/elif to dict
    reg_options = {1:'DFW',2:'ORD',3:'IAD',4:'SYD',5:'HKG',6:'LON'}
    while True:
        region = raw_input(prompt)
        region = int(region)
        if region not in range(1,7):
            print "Not a valid selection."
        else:
            break

    return reg_options[region]

def server_selection(region):
    #Displays a list of all available images, allows the user to select one, and performs input validation.
    imgs = pyrax.connect_to_cloudservers(region=region).images.list()
    count = 1
    for img in imgs:
        print count, ")", img.name
        count += 1
    total_count = len(imgs)
    while True:
        server = raw_input("\nSelect the server that you want to create by entering a number between 1 and %s.%s" % (total_count, prompt))
        try:
            server = int(server)
            if server < 1 or server > total_count:
                print "Selection out of range."
            else:
                break
        except ValueError:
            print "Not a valid selection."
    
    # not sure why this was done this way but it currently works. Will re-evaluate at later date
    count = 1
    for img in imgs:
        if count != server:
            count += 1
        else:
            server_type = img.name
            server_id = img.id
            break
    return (server_type, server_id)

def flv_selection(region):
    #Displays a list of all available flavors, allows the user to select one, and performs input validation.
    flvs = pyrax.connect_to_cloudservers(region=region).list_flavors()
    count = 1
    for flv in flvs:
        print count, ")", flv.name
        count += 1
    total_count = len(flvs)
    while True:
        server_flv = raw_input("\nSelect the server that you want to create by entering a number between 1 and %s.%s" % (total_count, prompt))
        try:
            server_flv = int(server_flv)
            if server_flv < 1 or server_flv > total_count:
                print "Selection out of range."
            else:
                break
        except ValueError:
            print "Not a valid selection."
    count = 1
    for flv in flvs:
        if count != server_flv:
            count += 1
        else:
            server_flv_type = flv.name
            server_flv_id = flv.id
            break
    return (server_flv_type, server_flv_id)