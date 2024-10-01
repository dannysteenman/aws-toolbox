"""
Description: This script identifies and optionally deletes unused EC2 key pairs in an AWS account.
It fetches all key pairs in the specified region, determines which ones are currently associated
with running EC2 instances, and identifies the unused key pairs. The script can perform a dry run
to show which key pairs would be deleted without actually deleting them.

Key features:
- Automatically uses the region specified in the AWS CLI profile
- Supports dry run mode for safe execution
- Provides detailed logging of all operations
- Uses boto3 to interact with AWS EC2 service
- Implements error handling for robustness

Usage:
python ec2_delete_unused_keypairs.py [--dry-run] [--profile PROFILE_NAME]

Author: Danny Steenman
License: MIT
"""

import argparse
import logging

import boto3
from botocore.exceptions import ClientError


def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    return logging.getLogger(__name__)


def get_ec2_client_and_resource():
    try:
        ec2_client = boto3.client("ec2")
        ec2_resource = boto3.resource("ec2")
        return ec2_client, ec2_resource
    except ClientError as e:
        logger.error(f"Failed to create EC2 client or resource: {e}")
        raise


def get_all_key_pairs(ec2_resource):
    try:
        key_pairs = list(ec2_resource.key_pairs.all())
        logger.info(f"All Keys: {len(key_pairs)} : {[kp.name for kp in key_pairs]}")
        return key_pairs
    except ClientError as e:
        logger.error(f"Failed to retrieve key pairs: {e}")
        return []


def get_used_key_pairs(ec2_resource):
    try:
        used_keys = set(instance.key_name for instance in ec2_resource.instances.all() if instance.key_name)
        logger.info(f"Used Keys: {len(used_keys)} : {used_keys}")
        return used_keys
    except ClientError as e:
        logger.error(f"Failed to retrieve used key pairs: {e}")
        return set()


def delete_unused_key_pairs(ec2_resource, unused_keys, dry_run=False):
    deleted_count = 0
    for key_name in unused_keys:
        try:
            if not dry_run:
                ec2_resource.KeyPair(key_name).delete()
                logger.info(f"Deleted unused key pair: {key_name}")
            else:
                logger.info(f"Would delete unused key pair: {key_name}")
            deleted_count += 1
        except ClientError as e:
            logger.error(f"Failed to delete key pair {key_name}: {e}")
    return deleted_count


def main(dry_run=False):
    ec2_client, ec2_resource = get_ec2_client_and_resource()

    all_key_pairs = get_all_key_pairs(ec2_resource)
    used_keys = get_used_key_pairs(ec2_resource)

    unused_keys = [key_pair.name for key_pair in all_key_pairs if key_pair.name not in used_keys]
    logger.info(f"Unused Keys: {len(unused_keys)} : {unused_keys}")

    if not unused_keys:
        logger.info("No unused key pairs found.")
        return

    deleted_count = delete_unused_key_pairs(ec2_resource, unused_keys, dry_run)

    action = "Would delete" if dry_run else "Deleted"
    logger.info(f"{action} {deleted_count} unused key pair(s).")


if __name__ == "__main__":
    logger = setup_logging()

    parser = argparse.ArgumentParser(description="Delete unused EC2 key pairs")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without actually deleting key pairs")
    args = parser.parse_args()

    main(dry_run=args.dry_run)
