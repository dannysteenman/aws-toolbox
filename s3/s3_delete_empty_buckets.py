"""
This script searches for empty S3 buckets without versioning enabled and optionally deletes them.
It includes a dry run mode for safe testing.

Author: Danny Steenman
Original source: https://github.com/dannysteenman/aws-toolbox
License: MIT
"""

import argparse
import sys

import boto3
from botocore.exceptions import ClientError


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Delete empty S3 buckets without versioning.")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without deleting buckets")
    return parser.parse_args()


def is_bucket_empty_and_unversioned(s3_client, bucket_name):
    """Check if a bucket is empty and has versioning disabled."""
    try:
        # Check if bucket is empty
        result = s3_client.list_objects_v2(Bucket=bucket_name, MaxKeys=1)
        if result.get("Contents"):
            return False

        # Check if versioning is disabled
        versioning = s3_client.get_bucket_versioning(Bucket=bucket_name)
        return versioning.get("Status") != "Enabled"
    except ClientError as e:
        print(f"Error checking bucket {bucket_name}: {e}", file=sys.stderr)
        return False


def get_empty_unversioned_buckets(s3_client):
    """Return a list of empty buckets with versioning disabled."""
    try:
        response = s3_client.list_buckets()
        buckets = response["Buckets"]
    except ClientError as e:
        print(f"Error listing buckets: {e}", file=sys.stderr)
        return []

    return [bucket["Name"] for bucket in buckets if is_bucket_empty_and_unversioned(s3_client, bucket["Name"])]


def delete_buckets(s3_resource, bucket_names, dry_run=False):
    """Delete the specified buckets."""
    for bucket_name in bucket_names:
        try:
            if dry_run:
                print(f"[Dry Run] Would delete bucket: {bucket_name}")
            else:
                s3_resource.Bucket(bucket_name).delete()
                print(f"Deleted bucket: {bucket_name}")
        except ClientError as e:
            print(f"Error deleting bucket {bucket_name}: {e}", file=sys.stderr)


def main():
    """Main function to run the script."""
    args = parse_arguments()

    s3_client = boto3.client("s3")
    s3_resource = boto3.resource("s3")

    empty_buckets = get_empty_unversioned_buckets(s3_client)

    if not empty_buckets:
        print("No empty, unversioned buckets found.")
        return

    print(f"Found {len(empty_buckets)} empty, unversioned bucket(s):")
    for bucket in empty_buckets:
        print(f"- {bucket}")

    if args.dry_run:
        print("\nDry run mode. No buckets will be deleted.")
    else:
        confirmation = input("\nDo you want to delete these buckets? (yes/no): ").lower()
        if confirmation != "yes":
            print("Operation cancelled.")
            return

    delete_buckets(s3_resource, empty_buckets, args.dry_run)


if __name__ == "__main__":
    main()
