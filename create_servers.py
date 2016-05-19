#!/usr/bin/python

"""
Written by: Wes
3/7/2014

This program utilizes Rackspace's Python SDK (pyrax) to create a specified number of servers.

Possible Improvements:
 Give the user the option to wait for networking information.

Enjoy!
"""

import os
from sys import argv
import pyrax
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

def region_selection():
    print """\nWhat region would you like to build in?

1) DFW
2) ORD
3) IAD
4) SYD
5) HKG
6) LON
"""
    while True:
        region = raw_input(prompt)
        if region not in ("1","2","3","4","5","6"):
            print "Not a valid selection."
        else:
            break
    if region == "1":
        region = "DFW"
    elif region == "2":
        region = "ORD"
    elif region == "3":
        region = "IAD"
    elif region == "4":
        region = "SYD"
    elif region == "5":
        region = "HKG"
    elif region == "6":
        region = "LON"
    return region

def server_selection():
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
    count = 1
    for img in imgs:
        if count != server:
            count += 1
        else:
            server_type = img.name
            server_id = img.id
            break
    return (server_type, server_id)

def flv_selection():
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

os.system("clear")
print "SERVER CREATION BADASSERY\n".center(75)

prompt = "\n   >>> "
ynprompt = "\n   >>>(y/N) "

api_initialization()
region = region_selection()
server_type, server_id = server_selection()
server_flv_type, server_flv_id = flv_selection()

while True:
    server_count = raw_input("\nHow many of these servers would you like to create?%s" % prompt) #Number of servers to be created.
    try:
        server_count = int(server_count)
        break
    except ValueError:
        print "Not a valid entry."

naming_con = raw_input("\nDesired naming convention prefix?%s" % prompt) #User defined naming convention.

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
while count <= server_count:
    server_name = "%s%s" % (naming_con, count)
    try:
        if ssh_auth == "y":
            server = pyrax.connect_to_cloudservers(region=region).servers.create(server_name, server_id, server_flv_id, key_name="my_key")
        else:
            server = pyrax.connect_to_cloudservers(region=region).servers.create(server_name, server_id, server_flv_id)
        #pyrax.utils.wait_for_build(server, "status", ["ACTIVE", "ERROR"], interval=20, callback=None, attempts=0, verbose=False, verbose_atts="progress")
        print "Name:", server.name
        print "Root Password:", server.adminPass
        print "ID:", server.id
        print "Region:", region
        print "Status:", server.status, "\n\n"
        #print "Public IP:", server.networks.get(u'public')[0]
        #print "Private IP:", server.networks.get(u'private')[0], "\n\n"
        server_info.write("Name: " + server.name + "\n")
        server_info.write("ID: " + server.id + "\n")
        server_info.write("Region: " + region + "\n")
        server_info.write("Admin Password: " + server.adminPass + "\n\n")
        #server_info.write("Public IP: " + server.networks.get(u'public')[0] + "\n")
        #server_info.write("Private IP: " + server.networks.get(u'private')[0] + "\n\n")
        count += 1
    except nexc.BadRequest as e:
        print "Bad image/flavor combination. Please try again. (wah wah wah)\n"
        exit()
server_info.close()
