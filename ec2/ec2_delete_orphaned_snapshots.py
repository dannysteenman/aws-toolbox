"""
Description: This script identifies and optionally deletes EBS snapshots in an AWS account where the
associated volume no longer exists and the snapshot is not part of any AMI.
The script can perform a dry run to show which snapshots would be deleted without actually deleting them.
It also supports a retention period to keep snapshots for a specified number of days.

Key features:
- Automatically uses the region specified in the AWS CLI profile
- Supports dry run mode for safe execution
- Provides detailed logging of all operations, including list of orphaned snapshot IDs
- Uses boto3 to interact with AWS EC2 service
- Implements error handling for robustness
- Allows setting a retention period for snapshots
- Ensures snapshots associated with AMIs are not deleted

Usage:
python ec2_delete_orphaned_snapshots.py [--dry-run] [--retention-days DAYS] [--profile PROFILE_NAME]

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


def get_owned_snapshots(ec2_client):
    try:
        owned_snapshots = []
        paginator = ec2_client.get_paginator("describe_snapshots")
        for page in paginator.paginate(OwnerIds=["self"]):
            owned_snapshots.extend(page["Snapshots"])
        logger.info(f"Owned snapshots: {len(owned_snapshots)}")
        return owned_snapshots
    except ClientError as e:
        logger.error(f"Failed to retrieve owned snapshots: {e}")
        return []


def is_volume_exists(ec2_client, volume_id):
    try:
        ec2_client.describe_volumes(VolumeIds=[volume_id])
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "InvalidVolume.NotFound":
            return False
        logger.error(f"Error checking volume {volume_id}: {e}")
        return True  # Assume volume exists in case of other errors


def get_snapshots_used_by_amis(ec2_client):
    try:
        used_snapshots = set()
        paginator = ec2_client.get_paginator("describe_images")
        for page in paginator.paginate(Owners=["self"]):
            for image in page["Images"]:
                for block_device in image.get("BlockDeviceMappings", []):
                    if "Ebs" in block_device and "SnapshotId" in block_device["Ebs"]:
                        used_snapshots.add(block_device["Ebs"]["SnapshotId"])
        logger.info(f"Snapshots used by AMIs: {len(used_snapshots)}")
        logger.info(f"Snapshot IDs used by AMIs: {list(used_snapshots)}")
        return used_snapshots
    except ClientError as e:
        logger.error(f"Failed to retrieve snapshots used by AMIs: {e}")
        return set()


def delete_snapshot(ec2_client, snapshot_id, dry_run=False):
    try:
        if not dry_run:
            ec2_client.delete_snapshot(SnapshotId=snapshot_id)
            logger.info(f"Deleted snapshot: {snapshot_id}")
        else:
            logger.info(f"Would delete snapshot: {snapshot_id}")
        return True
    except ClientError as e:
        logger.error(f"Failed to delete snapshot {snapshot_id}: {e}")
        return False


def delete_orphaned_snapshots(ec2_client, orphaned_snapshots, dry_run=False):
    deleted_count = 0
    for snapshot in orphaned_snapshots:
        if delete_snapshot(ec2_client, snapshot["SnapshotId"], dry_run):
            deleted_count += 1
    return deleted_count


def main(dry_run=False, retention_days=None):
    ec2_client = get_ec2_client()

    owned_snapshots = get_owned_snapshots(ec2_client)
    snapshots_used_by_amis = get_snapshots_used_by_amis(ec2_client)

    # Find orphaned snapshots
    orphaned_snapshots = [
        snapshot
        for snapshot in owned_snapshots
        if "VolumeId" in snapshot
        and not is_volume_exists(ec2_client, snapshot["VolumeId"])
        and snapshot["SnapshotId"] not in snapshots_used_by_amis
    ]
    logger.info(f"Orphaned snapshots: {len(orphaned_snapshots)}")
    logger.info(f"Orphaned snapshot IDs: {[snapshot['SnapshotId'] for snapshot in orphaned_snapshots]}")

    if retention_days is not None:
        # Filter snapshots based on retention period
        cutoff_date = datetime.now(orphaned_snapshots[0]["StartTime"].tzinfo) - timedelta(days=retention_days)
        orphaned_snapshots = [snapshot for snapshot in orphaned_snapshots if snapshot["StartTime"] < cutoff_date]
        logger.info(f"Orphaned snapshots older than {retention_days} days: {len(orphaned_snapshots)}")
        logger.info(
            f"Orphaned snapshot IDs to be deleted: {[snapshot['SnapshotId'] for snapshot in orphaned_snapshots]}"
        )

    if not orphaned_snapshots:
        logger.info("No orphaned snapshots found to delete.")
        return

    if dry_run:
        logger.info(f"Dry run: Would delete {len(orphaned_snapshots)} orphaned snapshot(s).")
        logger.info(
            f"Snapshot IDs that would be deleted: {[snapshot['SnapshotId'] for snapshot in orphaned_snapshots]}"
        )
    else:
        deleted_count = delete_orphaned_snapshots(ec2_client, orphaned_snapshots, dry_run)
        logger.info(f"Deleted {deleted_count} orphaned snapshot(s).")

    # Summary
    logger.info("Summary:")
    logger.info(f"  Total owned snapshots: {len(owned_snapshots)}")
    logger.info(f"  Snapshots used by AMIs: {len(snapshots_used_by_amis)}")
    logger.info(f"  Orphaned snapshots: {len(orphaned_snapshots)}")


if __name__ == "__main__":
    logger = setup_logging()

    parser = argparse.ArgumentParser(description="Delete orphaned EC2 snapshots")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without actually deleting snapshots")
    parser.add_argument("--retention-days", type=int, help="Number of days to retain snapshots before deletion")
    parser.add_argument("--profile", help="AWS CLI profile name")
    args = parser.parse_args()

    if args.profile:
        boto3.setup_default_session(profile_name=args.profile)

    main(dry_run=args.dry_run, retention_days=args.retention_days)
