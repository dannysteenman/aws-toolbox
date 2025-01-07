"""
Description: This script searches for a specified S3 bucket and downloads all objects locally,
maintaining the original folder structure. It provides detailed logging and supports a dry-run mode.

Key features:
- Supports dry run mode for safe execution
- Provides detailed logging of all operations
- Maintains the original folder structure when downloading
- Implements error handling for robustness
- Shows progress of downloads
- Allows specifying a custom target path for each bucket's contents

Usage:
python s3_search_bucket_and_download.py <bucket-name> [--dry-run] [--output-dir <path>] [--target-path <path>]

Author: Danny Steenman
License: MIT
"""

import argparse
import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    return logging.getLogger(__name__)


def get_s3_client():
    try:
        config = Config(
            max_pool_connections=50,  # Increase concurrent connections
            retries={"max_attempts": 10, "mode": "adaptive"},  # Add retry logic
        )
        return boto3.client("s3", config=config)
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


def download_object(s3_client, bucket_name, obj_key, output_dir, dry_run=False):
    local_path = os.path.join(output_dir, obj_key)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    if dry_run:
        logger.info(f"Would download: s3://{bucket_name}/{obj_key} to {local_path}")
    else:
        try:
            s3_client.download_file(bucket_name, obj_key, local_path)
            logger.info(f"Downloaded: s3://{bucket_name}/{obj_key} to {local_path}")
        except ClientError as e:
            logger.error(f"Failed to download s3://{bucket_name}/{obj_key}: {e}")


def download_bucket_contents(s3_client, bucket_name, output_dir, dry_run=False):
    try:
        paginator = s3_client.get_paginator("list_objects_v2")
        total_objects = 0
        downloaded_objects = 0

        # Count total objects
        for page in paginator.paginate(Bucket=bucket_name):
            total_objects += len(page.get("Contents", []))

        logger.info(f"Total objects to download: {total_objects}")

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for page in paginator.paginate(Bucket=bucket_name):
                for obj in page.get("Contents", []):
                    future = executor.submit(download_object, s3_client, bucket_name, obj["Key"], output_dir, dry_run)
                    futures.append(future)

            for future in as_completed(futures):
                downloaded_objects += 1
                if downloaded_objects % 100 == 0 or downloaded_objects == total_objects:
                    logger.info(f"Progress: {downloaded_objects}/{total_objects} objects downloaded")

        logger.info(f"{'Would download' if dry_run else 'Downloaded'} {total_objects} objects from {bucket_name}")

    except ClientError as e:
        logger.error(f"Failed to download contents of bucket {bucket_name}: {e}")


def main(target_bucket_name, output_dir, target_path, dry_run=False):
    s3_client = get_s3_client()

    try:
        response = s3_client.list_buckets()
    except ClientError as e:
        logger.error(f"Failed to list buckets: {e}")
        sys.exit(1)

    found_buckets = [bucket["Name"] for bucket in response["Buckets"] if target_bucket_name in bucket["Name"]]

    if not found_buckets:
        logger.info(f"No buckets found containing the name: {target_bucket_name}")
        return

    for bucket_name in found_buckets:
        logger.info(f"Found bucket: {bucket_name}")
        size_bytes = get_bucket_size(s3_client, bucket_name)
        size_gb = size_bytes / (1024**3)  # Convert bytes to gigabytes
        logger.info(f"Bucket size: {size_gb:.2f} GB")

        if target_path:
            bucket_output_dir = os.path.join(output_dir, target_path)
        else:
            bucket_output_dir = os.path.join(output_dir, bucket_name)

        if dry_run:
            logger.info(f"Dry run: Would download all contents from {bucket_name} to {bucket_output_dir}")
        else:
            download_bucket_contents(s3_client, bucket_name, bucket_output_dir, dry_run)

    logger.info("Operation completed.")


if __name__ == "__main__":
    logger = setup_logging()

    parser = argparse.ArgumentParser(description="Download S3 bucket contents while maintaining folder structure")
    parser.add_argument("bucket_name", help="Name of the bucket to search for and download")
    parser.add_argument(
        "--dry-run", action="store_true", help="Perform a dry run without actually downloading anything"
    )
    parser.add_argument(
        "--output-dir", default=".", help="Base output directory for downloaded files (default: current directory)"
    )
    parser.add_argument(
        "--target-path", help="Specific target path within the output directory to store bucket contents"
    )
    args = parser.parse_args()

    main(args.bucket_name, args.output_dir, args.target_path, args.dry_run)
