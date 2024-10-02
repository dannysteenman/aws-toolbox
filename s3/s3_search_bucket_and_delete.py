"""
Description: This script searches for a specified bucket name and optionally deletes all (versioned) objects
in that S3 bucket before deleting the bucket itself. It supports a dry-run mode and provides information
about the storage used in the bucket.

Key features:
- Supports dry run mode for safe execution
- Provides detailed logging of all operations
- Shows total storage used in the bucket
- Handles both versioned and non-versioned buckets
- Implements error handling for robustness

Usage:
python s3_search_bucket_and_delete.py <bucket-name> [--dry-run]

Author: Danny Steenman
License: MIT
"""

import argparse
import logging
import sys

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    return logging.getLogger(__name__)


def get_s3_client():
    try:
        return boto3.client("s3")
    except ClientError as e:
        logger.error(f"Failed to create S3 client: {e}")
        sys.exit(1)


def get_bucket_size(s3_client, bucket_name):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        total_size = sum(obj["Size"] for obj in response.get("Contents", []))
        return total_size
    except ClientError as e:
        logger.error(f"Failed to get bucket size for {bucket_name}: {e}")
        return 0


def delete_bucket_contents(s3_client, bucket_name, dry_run=False):
    try:
        versioning = s3_client.get_bucket_versioning(Bucket=bucket_name)
        is_versioned = versioning.get("Status") == "Enabled"

        # Configure the client for more concurrency
        config = Config(
            max_pool_connections=50,  # Increase concurrent connections
            retries={"max_attempts": 10, "mode": "adaptive"},  # Add retry logic
        )
        s3_resource = boto3.resource("s3", config=config)
        bucket = s3_resource.Bucket(bucket_name)

        def delete_objects(object_versions):
            if not dry_run:
                try:
                    bucket.delete_objects(Delete={"Objects": object_versions})
                except ClientError as e:
                    logger.error(f"Error deleting objects: {e}")

        object_versions = []
        count = 0

        if is_versioned:
            iterator = bucket.object_versions.iterator()
        else:
            iterator = bucket.objects.iterator()

        for obj in iterator:
            if is_versioned:
                object_versions.append({"Key": obj.object_key, "VersionId": obj.id})
            else:
                object_versions.append({"Key": obj.key})
            count += 1

            # Process in batches of 1000 (S3 delete_objects limit)
            if len(object_versions) >= 1000:
                if dry_run:
                    logger.info(f"Would delete {len(object_versions)} {'versions' if is_versioned else 'objects'}")
                else:
                    delete_objects(object_versions)
                object_versions = []

            # Log progress every 10000 objects
            if count % 10000 == 0:
                logger.info(f"Processed {count} {'versions' if is_versioned else 'objects'}")

        # Delete any remaining objects
        if object_versions:
            if dry_run:
                logger.info(f"Would delete {len(object_versions)} {'versions' if is_versioned else 'objects'}")
            else:
                delete_objects(object_versions)

        logger.info(
            f"{'Would delete' if dry_run else 'Deleted'} a total of {count} {'versions' if is_versioned else 'objects'} from {bucket_name}"
        )

    except ClientError as e:
        logger.error(f"Failed to delete contents of bucket {bucket_name}: {e}")


def delete_bucket(s3_client, bucket_name, dry_run=False):
    try:
        if dry_run:
            logger.info(f"Would delete bucket: {bucket_name}")
        else:
            s3_client.delete_bucket(Bucket=bucket_name)
            logger.info(f"Deleted bucket: {bucket_name}")
    except ClientError as e:
        logger.error(f"Failed to delete bucket {bucket_name}: {e}")


def main(target_bucket_name, dry_run=False):
    s3_client = get_s3_client()

    try:
        response = s3_client.list_buckets()
    except ClientError as e:
        logger.error(f"Failed to list buckets: {e}")
        sys.exit(1)

    found_buckets = []
    for bucket in response["Buckets"]:
        bucket_name = bucket["Name"]
        if target_bucket_name in bucket_name:
            found_buckets.append(bucket_name)

    if not found_buckets:
        logger.info(f"No buckets found containing the name: {target_bucket_name}")
        return

    for bucket_name in found_buckets:
        logger.info(f"Found bucket: {bucket_name}")
        size_bytes = get_bucket_size(s3_client, bucket_name)
        size_gb = size_bytes / (1024**3)  # Convert bytes to gigabytes
        logger.info(f"Bucket size: {size_gb:.2f} GB")

        if dry_run:
            logger.info(f"Dry run: Would delete all contents and the bucket itself: {bucket_name}")
        else:
            delete_bucket_contents(s3_client, bucket_name, dry_run)
            delete_bucket(s3_client, bucket_name, dry_run)

    logger.info("Operation completed.")


if __name__ == "__main__":
    logger = setup_logging()

    parser = argparse.ArgumentParser(description="Delete S3 bucket and its contents")
    parser.add_argument("bucket_name", help="Name of the bucket to search for and delete")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without actually deleting anything")
    args = parser.parse_args()

    main(args.bucket_name, args.dry_run)
