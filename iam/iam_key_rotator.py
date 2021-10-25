#  https://github.com/dannysteenman/aws-toolbox
#
# This script rotates IAM user keys.

import argparse
import boto3
from botocore.exceptions import ClientError

iam_client = boto3.client("iam")
parser = argparse.ArgumentParser()
parser.add_argument(
    "-u",
    "--username",
    help="An IAM username, e.g. key_rotator.py --username <username>",
)
parser.add_argument(
    "-k", "--key", help="An AWS access key, e.g. key_rotator.py --key <access_key>"
)
parser.add_argument("--disable", help="Disables an access key", action="store_true")
parser.add_argument("--delete", help="Deletes an access key", action="store_true")
args = parser.parse_args()
username = args.username
aws_access_key = args.key


def create_key(username):
    if inactive_keys + active_keys >= 2:
        print(
            f"{username} already has 2 keys. You must delete a key before you can create another key."
        )
        exit()
    access_key_metadata = iam_client.create_access_key(UserName=username)["AccessKey"]
    access_key = access_key_metadata["AccessKeyId"]
    secret_key = access_key_metadata["SecretAccessKey"]
    print(
        f"your new access key is {access_key} and your new secret key is {secret_key}"
    )
    access_key = ""
    secret_key = ""


def disable_key(access_key, username):
    i = ""
    try:
        while i != "Y" or "N":
            i = raw_input(
                "Do you want to disable the access key " + access_key + " [Y/N]?"
            )
            i = str.capitalize(i)
            if i == "Y":
                iam_client.update_access_key(
                    UserName=username, AccessKeyId=access_key, Status="Inactive"
                )
                print(f"{access_key} has been disabled.")
                exit()
            elif i == "N":
                exit()
    except ClientError as e:
        print(f"The access key with id {access_key} cannot be found: {e}")


def delete_key(access_key, username):
    i = ""
    try:
        while i != "Y" or "N":
            i = raw_input(
                "Do you want to delete the access key " + access_key + " [Y/N]?"
            )
            i = str.capitalize(i)
            if i == "Y":
                iam_client.delete_access_key(UserName=username, AccessKeyId=access_key)
                print(f"{access_key} has been deleted.")
                exit()
            elif i == "N":
                exit()
    except ClientError as e:
        print(f"The access key with id {access_key} cannot be found: {e}")


try:
    keys = iam_client.list_access_keys(UserName=username)
    inactive_keys = 0
    active_keys = 0
    for key in keys["AccessKeyMetadata"]:
        if key["Status"] == "Inactive":
            inactive_keys += 1
        elif key["Status"] == "Active":
            active_keys += 1
    print(f"{username} has {inactive_keys} inactive keys and {active_keys} active keys")
    if args.disable:
        disable_key(aws_access_key, username)
    elif args.delete:
        delete_key(aws_access_key, username)
    else:
        create_key(username)
except ClientError as e:
    print(f"The user with the name {username} cannot be found: {e}")
