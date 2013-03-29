#!/usr/bin/env python
"""
This is a script that uploads a file that is given to cloud files.

prerequisites:
* have a rackspace cloud account
* created a cloud files container named after CONTAINER_NAME global var
* setup the ~/.rackspace_cloud_credentials file

[rackspace_cloud]
username = username
api_key = api_key

Running the script:
python uploadFile.py test.tgz

"""


import os
import sys


try:
    import pyrax
    import pyrax.exceptions as exc
except:
    sys.exit("You need to install Pyrax! (sudo pip install pyrax)")


CONTAINER_NAME = 'files'


def main():
    """ Upload of a file to cloud files that is passed in. """

    # handle expecting input of file to upload
    if len(sys.argv) < 2:
        sys.exit("Expect input of the file to upload.")

    # setup auth for cloud files
    try:
        creds_file = os.path.expanduser("~/.rackspace_cloud_credential")
        pyrax.set_credential_file(creds_file)
    except pyrax.exceptions.FileNotFound, e:
        print("Setup the ~/.rackspace_cloud_credential file with this info.")
        print("[rackspace_cloud]")
        print("username = username")
        print("api_key = api_key")
        sys.exit()

    cf = pyrax.cloudfiles

    # gets the container and get list of files
    cont = cf.get_container(CONTAINER_NAME)
    cont_files = cont.get_objects()
    print(cont_files)

    # get the file name
    upload_this = sys.argv[1]
    print(upload_this)
    file_name_to_upload = os.path.basename(upload_this)
    print(file_name_to_upload)

    if is_new_file_to_upload():
        print("Uploading file...")
        cont.upload_file(upload_this)
        print(cont.get_objects())
        print("DONE!")
    else:
        # not a new file so we exit with message
        print("Expecting a different file name to upload.")
        sys.exit("FILE ALREADY EXISTS '%s'" % file_name_to_upload)


def is_new_file_to_upload():
        # validate the file is not already in the container
        name_list = [f.name for f in cont_files]
        if file_name_to_upload in name_list:
            return 0
        return 1


if __name__ == '__main__':
    main()
