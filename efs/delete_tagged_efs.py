#  https://github.com/dannysteenman/aws-toolbox
#
#  License: MIT
#
# This script finds and deletes all tagged elastic file systems including mount targets

import boto3
import time
import random


def find_efs_filesystems(efs_client, tag_key, tag_value_contains):
    response = efs_client.describe_file_systems()

    filtered_filesystems = []
    for fs in response["FileSystems"]:
        for tag in fs.get("Tags", []):
            if tag.get("Key") == tag_key and tag_value_contains in tag.get("Value", ""):
                filtered_filesystems.append(fs)

    return filtered_filesystems


def delete_mount_targets(efs_client, filesystem_id):
    response = efs_client.describe_mount_targets(FileSystemId=filesystem_id)

    for mt in response["MountTargets"]:
        efs_client.delete_mount_target(MountTargetId=mt["MountTargetId"])
        print("Deleted Mount Target: {}".format(mt["MountTargetId"]))


def delete_efs_filesystem(efs_client, filesystem_id):
    max_retries = 5
    current_retry = 0

    while current_retry < max_retries:
        try:
            # Delete the mount targets for the EFS filesystem
            delete_mount_targets(efs_client, filesystem_id)

            # Wait with exponential backoff
            delay = (2**current_retry) + random.uniform(0, 1)
            print(f"Waiting for {delay} seconds before attempting to delete the EFS filesystem.")
            time.sleep(delay)

            # Delete the specified EFS filesystem
            efs_client.delete_file_system(FileSystemId=filesystem_id)
            print("Deleted EFS Filesystem: {}".format(filesystem_id))
            break
        except efs_client.exceptions.FileSystemInUse as e:
            current_retry += 1
            print(f"Retry {current_retry}/{max_retries}: {e}")


def main():
    # Fetch AWS account ID from boto3 session
    account_id = boto3.client("sts").get_caller_identity().get("Account")
    aws_region = "eu-central-1"

    # Modify the tag key and value to your own liking
    tag_key = "ManagedByAmazonSageMakerResource"
    tag_value_contains = f"arn:aws:sagemaker:{aws_region}:{account_id}:domain"

    efs_client = boto3.client("efs", region_name=aws_region)
    efs_filesystems = find_efs_filesystems(efs_client, tag_key, tag_value_contains)

    for fs in efs_filesystems:
        filesystem_id = fs["FileSystemId"]
        delete_efs_filesystem(efs_client, filesystem_id)


if __name__ == "__main__":
    main()
