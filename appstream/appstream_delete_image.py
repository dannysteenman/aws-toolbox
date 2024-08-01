#  https://github.com/dannysteenman/aws-toolbox
#
#  License: MIT
#
# The script retrieves all AWS accounts an AppStream image is shared with, offers to unshare it from those accounts, and then deletes the image.

import sys

import boto3
import botocore


def get_all_shared_account_ids(appstream_client, image_name):
    shared_account_ids = []
    next_token = None

    try:
        while True:
            if next_token:
                response = appstream_client.describe_image_permissions(Name=image_name, NextToken=next_token)
            else:
                response = appstream_client.describe_image_permissions(Name=image_name)

            for permission in response.get("SharedImagePermissionsList", []):
                shared_account_ids.append(permission["sharedAccountId"])

            next_token = response.get("NextToken")
            if not next_token:
                break

        return shared_account_ids
    except appstream_client.exceptions.ResourceNotFoundException:
        print(f"Image '{image_name}' not found.")
        return None
    except botocore.exceptions.ClientError as e:
        print(f"Error retrieving image permissions: {e}")
        return None


def unshare_image(appstream_client, image_name, account_ids):
    for account_id in account_ids:
        try:
            appstream_client.delete_image_permissions(Name=image_name, SharedAccountId=account_id)
            print(f"Unshared image from account: {account_id}")
        except Exception as e:
            print(f"Failed to unshare image from account {account_id}: {str(e)}")


def delete_appstream_image(image_name):
    appstream_client = boto3.client("appstream")

    try:
        # Get all shared account IDs
        shared_account_ids = get_all_shared_account_ids(appstream_client, image_name)

        if shared_account_ids is None:
            return

        if shared_account_ids:
            print(f"Image '{image_name}' is shared with {len(shared_account_ids)} account(s):")
            for account_id in shared_account_ids:
                print(f"  - {account_id}")
            confirm = input("Do you want to unshare and then delete the image? (y/n): ")
            if confirm.lower() != "y":
                print("Operation cancelled.")
                return

            unshare_image(appstream_client, image_name, shared_account_ids)
        else:
            print(f"Image '{image_name}' is not shared with any accounts.")

        # Try to delete the image
        appstream_client.delete_image(Name=image_name)
        print(f"Image '{image_name}' deleted successfully.")

    except botocore.exceptions.ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]
        print(f"An AWS error occurred: {error_code} - {error_message}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python appstream_delete_image.py <image_name>")
        sys.exit(1)

    image_name = sys.argv[1]
    delete_appstream_image(image_name)
