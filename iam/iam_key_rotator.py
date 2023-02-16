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
    try:
        keys = iam_client.list_access_keys(UserName=username)["AccessKeyMetadata"]
        if len(keys) >= 2:
            print(
                f"{username} already has 2 keys. You must delete a key before you can create another key."
            )
            return
        access_key_metadata = iam_client.create_access_key(UserName=username)[
            "AccessKey"
        ]
        access_key = access_key_metadata["AccessKeyId"]
        secret_key = access_key_metadata["SecretAccessKey"]
        print(
            f"Your new access key is {access_key} and your new secret key is {secret_key}"
        )
    except ClientError as e:
        print(f"Failed to create access key for {username}: {e}")


def disable_key(access_key, username):
    try:
        answer = input(f"Do you want to disable the access key {access_key}? [y/N] ")
        if answer.lower() == "y":
            iam_client.update_access_key(
                UserName=username, AccessKeyId=access_key, Status="Inactive"
            )
            print(f"{access_key} has been disabled.")
        else:
            print("Aborting.")
    except ClientError as e:
        print(f"Failed to disable access key {access_key}: {e}")


def delete_key(access_key, username):
    try:
        answer = input(f"Do you want to delete the access key {access_key}? [y/N] ")
        if answer.lower() == "y":
            iam_client.delete_access_key(UserName=username, AccessKeyId=access_key)
            print(f"{access_key} has been deleted.")
        else:
            print("Aborting.")
    except ClientError as e:
        print(f"Failed to delete access key {access_key}: {e}")


try:
    keys = iam_client.list_access_keys(UserName=username)["AccessKeyMetadata"]
    inactive_keys = sum(1 for key in keys if key["Status"] == "Inactive")
    active_keys = sum(1 for key in keys if key["Status"] == "Active")
    print(f"{username} has {inactive_keys} inactive keys and {active_keys} active keys")
    if args.disable:
        disable_key(aws_access_key, username)
    elif args.delete:
        delete_key(aws_access_key, username)
    else:
        create_key(username)
except ClientError as e:
    print(f"Failed to list access keys for {username}: {e}")
