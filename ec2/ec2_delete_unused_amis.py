"""
Description: This script identifies and optionally deletes unused AMIs (Amazon Machine Images) in an AWS account.
It fetches all AMIs owned by the account, determines which ones are currently used by EC2 instances,
and identifies the unused AMIs. The script can perform a dry run to show which AMIs would be deleted
without actually deleting them. It also supports a retention period to keep AMIs for a specified number of days.

Key features:
- Automatically uses the region specified in the AWS CLI profile
- Supports dry run mode for safe execution
- Provides detailed logging of all operations
- Uses boto3 to interact with AWS EC2 service
- Implements error handling for robustness
- Allows setting a retention period for AMIs
- Deletes associated snapshots when deleting AMIs

Usage:
python ec2_delete_unused_amis.py [--dry-run] [--retention-days DAYS] [--profile PROFILE_NAME]

Author: [Your Name]
License: MIT
"""

import argparse
import logging
from datetime import datetime, timedelta

import boto3
from botocore.exceptions import ClientError


def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    return logging.getLogger(__name__)


def get_ec2_client():
    try:
        return boto3.client("ec2")
    except ClientError as e:
        logger.error(f"Failed to create EC2 client: {e}")
        raise


def get_owned_amis(ec2_client):
    try:
        owned_amis = []
        paginator = ec2_client.get_paginator("describe_images")
        for page in paginator.paginate(Owners=["self"]):
            owned_amis.extend(page["Images"])
        logger.info(f"Owned AMIs: {len(owned_amis)} : {[ami['ImageId'] for ami in owned_amis]}")
        return owned_amis
    except ClientError as e:
        logger.error(f"Failed to retrieve owned AMIs: {e}")
        return []


def get_used_amis(ec2_client):
    try:
        used_amis = set()
        paginator = ec2_client.get_paginator("describe_instances")
        for page in paginator.paginate():
            for reservation in page["Reservations"]:
                for instance in reservation["Instances"]:
                    if "ImageId" in instance:
                        used_amis.add(instance["ImageId"])
        logger.info(f"Used AMIs: {len(used_amis)} : {used_amis}")
        return used_amis
    except ClientError as e:
        logger.error(f"Failed to retrieve used AMIs: {e}")
        return set()


def delete_ami_and_snapshot(ec2_client, ami_id, dry_run=False):
    try:
        # Get snapshot IDs associated with the AMI
        image = ec2_client.describe_images(ImageIds=[ami_id])["Images"][0]
        snapshot_ids = [
            block_device["Ebs"]["SnapshotId"]
            for block_device in image.get("BlockDeviceMappings", [])
            if "Ebs" in block_device
        ]

        if not dry_run:
            # Deregister the AMI
            ec2_client.deregister_image(ImageId=ami_id)
            logger.info(f"Deregistered AMI: {ami_id}")

            # Delete associated snapshots
            for snapshot_id in snapshot_ids:
                ec2_client.delete_snapshot(SnapshotId=snapshot_id)
                logger.info(f"Deleted snapshot: {snapshot_id}")
        else:
            logger.info(f"Would deregister AMI: {ami_id}")
            for snapshot_id in snapshot_ids:
                logger.info(f"Would delete snapshot: {snapshot_id}")
        return True
    except ClientError as e:
        logger.error(f"Failed to delete AMI {ami_id} or its snapshots: {e}")
        return False


def delete_unused_amis(ec2_client, unused_amis, dry_run=False):
    deleted_count = 0
    for ami in unused_amis:
        if delete_ami_and_snapshot(ec2_client, ami["ImageId"], dry_run):
            deleted_count += 1
    return deleted_count


def main(dry_run=False, retention_days=None):
    ec2_client = get_ec2_client()

    owned_amis = get_owned_amis(ec2_client)
    used_amis = get_used_amis(ec2_client)

    # Find unused AMIs
    unused_amis = [ami for ami in owned_amis if ami["ImageId"] not in used_amis]
    logger.info(f"Unused AMIs: {len(unused_amis)} : {[ami['ImageId'] for ami in unused_amis]}")

    if retention_days is not None:
        # Filter AMIs based on retention period
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        unused_amis = [
            ami for ami in unused_amis if datetime.strptime(ami["CreationDate"], "%Y-%m-%dT%H:%M:%S.%fZ") < cutoff_date
        ]
        logger.info(
            f"Unused AMIs older than {retention_days} days: {len(unused_amis)} : {[ami['ImageId'] for ami in unused_amis]}"
        )

    if not unused_amis:
        logger.info("No unused AMIs found to delete.")
        return

    if dry_run:
        logger.info(f"Dry run: Would delete {len(unused_amis)} unused AMI(s) and their associated snapshots.")
    else:
        deleted_count = delete_unused_amis(ec2_client, unused_amis, dry_run)
        logger.info(f"Deleted {deleted_count} unused AMI(s) and their associated snapshots.")

    # Summary
    logger.info("Summary:")
    logger.info(f"  Total owned AMIs: {len(owned_amis)}")
    logger.info(f"  Used AMIs: {len(used_amis)}")
    logger.info(f"  Unused AMIs: {len(unused_amis)}")


if __name__ == "__main__":
    logger = setup_logging()

    parser = argparse.ArgumentParser(description="Delete unused EC2 AMIs")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without actually deleting AMIs")
    parser.add_argument("--retention-days", type=int, help="Number of days to retain AMIs before deletion")
    args = parser.parse_args()

    main(dry_run=args.dry_run, retention_days=args.retention_days)
