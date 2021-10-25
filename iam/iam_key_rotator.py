import argparse
import boto3
from botocore.exceptions import ClientError
iam_client = boto3.client('iam')
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="An IAM username, e.g. key_rotator.py --username <username>")
parser.add_argument("-k", "--key", help="An AWS access key, e.g. key_rotator.py --key <access_key>")
parser.add_argument("--disable", help="Disables an access key", action="store_true")
parser.add_argument("--delete", help="Deletes an access key", action="store_true")
args = parser.parse_args()
username = args.username
aws_access_key = args.key

def create_key(username):
    if inactive_keys + active_keys >= 2:
        print "%s already has 2 keys. You must delete a key before you can create another key." % username
        exit()
    access_key_metadata = iam_client.create_access_key(UserName=username)['AccessKey']
    access_key = access_key_metadata['AccessKeyId']
    secret_key = access_key_metadata['SecretAccessKey']
    print "your new access key is %s and your new secret key is %s" % (access_key, secret_key)
    access_key = ''
    secret_key = ''

def disable_key(access_key, username):
    i = ""
    try:
        while i != 'Y' or 'N':
            i = raw_input("Do you want to disable the access key " + access_key + " [Y/N]?")
            i = str.capitalize(i)
            if i == 'Y':
                iam_client.update_access_key(UserName=username, AccessKeyId=access_key, Status="Inactive")
                print access_key + " has been disabled."
                exit()
            elif i == 'N':
                exit()
    except ClientError as e:
        print "The access key with id %s cannot be found" % access_key

def delete_key(access_key, username):
    i = ""
    try:
        while i != 'Y' or 'N':
            i = raw_input("Do you want to delete the access key " + access_key + " [Y/N]?")
            i = str.capitalize(i)
            if i == 'Y':
                iam_client.delete_access_key(UserName=username, AccessKeyId=access_key)
                print access_key + " has been deleted."
                exit()
            elif i == 'N':
                exit()
    except ClientError as e:
        print "The access key with id %s cannot be found" % access_key

try:
    keys = iam_client.list_access_keys(UserName=username)
    inactive_keys = 0
    active_keys = 0
    for key in keys['AccessKeyMetadata']:
        if key['Status']=='Inactive': inactive_keys = inactive_keys + 1
        elif key['Status']=='Active': active_keys = active_keys + 1
    print "%s has %d inactive keys and %d active keys" % (username, inactive_keys, active_keys)
    if args.disable:
        disable_key(aws_access_key, username)
    elif args.delete:
        delete_key(aws_access_key, username)
    else:
        create_key(username)
except ClientError as e:
    print "The user with the name %s cannot be found." % username
