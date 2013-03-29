#!/usr/bin/env python

import os
import sys

try:
    import pyrax
    import pyrax.exceptions as exc
except:
    sys.exit("You need to install Pyrax! (sudo pip install pyrax)")


# handle expecting input of file to upload
if len(sys.argv) < 2:
    sys.exit("Expect input of the file to upload.")


# setup auth for cloud files
creds_file = os.path.expanduser("~/.rackspace_cloud_credential")
pyrax.set_credential_file(creds_file)
cf = pyrax.cloudfiles


# gets the container and get list of files
cont = cf.get_container('release-candidate')
cont_files = cont.get_objects()
print cont_files


# get the file name
upload_this = sys.argv[1]
print upload_this
file_name_to_upload = os.path.basename(upload_this)
print file_name_to_upload


# validate the file is not already in the container
name_list = [f.name for f in cont_files]
if file_name_to_upload in name_list:
    msg = "Expecting a different file name to upload. (FILE ALREADY EXISTS '%s')" % file_name_to_upload
    sys.exit(msg)


print "Uploading file..."
cont.upload_file(upload_this)
print cont.get_objects()
print "DONE!"
