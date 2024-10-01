"""
Description: This script identifies and optionally deletes unused security groups in an AWS account.
It fetches security groups based on the specified type (EC2, RDS, ELB, or all), determines which ones
are currently in use, and identifies the unused security groups. The script can perform a dry run
to show which security groups would be deleted without actually deleting them.

Key features:
- Supports filtering of security groups by type (EC2, RDS, ELB, or all)
- Automatically uses the region specified in the AWS CLI profile
- Supports dry run mode for safe execution
- Provides detailed logging of all operations
- Implements error handling for robustness
- Skips deletion of security groups with 'default' in their name
- Handles cases where load balancers might not have associated security groups

Usage:
python delete_unused_security_groups.py [--dry-run] [--type {all,ec2,rds,elb}]

Arguments:
--dry-run            Perform a dry run without deleting security groups
--type {all,ec2,rds,elb}  Specify the type of security groups to consider (default: all)

The script performs the following steps:
1. Retrieves all security groups of the specified type
2. Identifies security groups in use by EC2 instances, load balancers, and RDS instances
3. Determines unused security groups by comparing all groups to those in use
4. Deletes unused security groups (unless in dry-run mode)

Note: This script requires appropriate AWS permissions to describe and delete security groups,
as well as to describe EC2 instances, load balancers, and RDS instances.

Author: Danny Steenman
License: MIT
"""

import argparse
import logging

import boto3
from botocore.exceptions import ClientError


def setup_logging():
    """Configure logging for the script."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    return logging.getLogger(__name__)


def get_used_security_groups(ec2, elb, elbv2, rds, logger, sg_type):
    """Collect all security groups in use."""
    used_sg = set()

    if sg_type in ["all", "ec2"]:
        try:
            # EC2 instances
            for reservation in ec2.describe_instances()["Reservations"]:
                for instance in reservation["Instances"]:
                    used_sg.update(sg["GroupId"] for sg in instance["SecurityGroups"])
        except ClientError as e:
            logger.error(f"Error describing EC2 instances: {str(e)}")

    if sg_type in ["all", "elb"]:
        try:
            # Classic Load Balancers
            for lb in elb.describe_load_balancers()["LoadBalancerDescriptions"]:
                if "SecurityGroups" in lb:
                    used_sg.update(lb["SecurityGroups"])
                else:
                    logger.debug(
                        f"Classic Load Balancer without SecurityGroups: {lb.get('LoadBalancerName', 'Unknown')}"
                    )
        except ClientError as e:
            logger.error(f"Error describing Classic Load Balancers: {str(e)}")

        try:
            # Application and Network Load Balancers
            for lb in elbv2.describe_load_balancers()["LoadBalancers"]:
                if "SecurityGroups" in lb:
                    used_sg.update(lb["SecurityGroups"])
                else:
                    logger.debug(f"ALB/NLB without SecurityGroups: {lb.get('LoadBalancerName', 'Unknown')}")
        except ClientError as e:
            logger.error(f"Error describing Application/Network Load Balancers: {str(e)}")

    if sg_type in ["all", "rds"]:
        try:
            # RDS Instances
            for instance in rds.describe_db_instances()["DBInstances"]:
                used_sg.update(sg["VpcSecurityGroupId"] for sg in instance["VpcSecurityGroups"])
        except ClientError as e:
            logger.error(f"Error describing RDS instances: {str(e)}")

    return used_sg


def get_all_security_groups(ec2, sg_type):
    """Get all security groups in the region based on the specified type."""
    all_sg = set()
    try:
        response = ec2.describe_security_groups()
        for sg in response["SecurityGroups"]:
            group_name = sg["GroupName"].lower()
            if sg_type == "all":
                all_sg.add(sg["GroupId"])
            elif sg_type == "ec2" and not (group_name.startswith("rds-") or group_name.startswith("elb-")):
                all_sg.add(sg["GroupId"])
            elif sg_type == "rds" and group_name.startswith("rds-"):
                all_sg.add(sg["GroupId"])
            elif sg_type == "elb" and group_name.startswith("elb-"):
                all_sg.add(sg["GroupId"])
    except ClientError as e:
        logger.error(f"Error describing security groups: {str(e)}")
    return all_sg


def delete_unused_security_groups(ec2, unused_sg, dry_run, logger):
    """Delete unused security groups, skipping those with 'default' in the name."""
    for sg_id in unused_sg:
        try:
            sg_info = ec2.describe_security_groups(GroupIds=[sg_id])["SecurityGroups"][0]
            sg_name = sg_info["GroupName"]

            if "default" in sg_name.lower():
                logger.info(
                    f"Skipping deletion of security group '{sg_name}' (ID: {sg_id}) because it contains 'default'"
                )
                continue

            if dry_run:
                logger.info(f"[DRY RUN] Would delete security group '{sg_name}' (ID: {sg_id})")
            else:
                logger.info(f"Deleting security group '{sg_name}' (ID: {sg_id})")
                ec2.delete_security_group(GroupId=sg_id)
        except ClientError as e:
            if e.response["Error"]["Code"] == "DependencyViolation":
                logger.warning(
                    f"Skipping deletion of security group '{sg_name}' (ID: {sg_id}) because it has a dependent object."
                )
            else:
                logger.error(f"Error deleting security group '{sg_name}' (ID: {sg_id}): {str(e)}")


def main(dry_run, sg_type):
    logger = setup_logging()

    # Initialize AWS clients
    ec2 = boto3.client("ec2")
    elb = boto3.client("elb")
    elbv2 = boto3.client("elbv2")
    rds = boto3.client("rds")

    used_sg = get_used_security_groups(ec2, elb, elbv2, rds, logger, sg_type)
    all_sg = get_all_security_groups(ec2, sg_type)
    unused_sg = all_sg - used_sg

    logger.info(f"Total Security Groups ({sg_type}): {len(all_sg)}")
    logger.info(f"Used Security Groups ({sg_type}): {len(used_sg)}")
    logger.info(f"Unused Security Groups ({sg_type}): {len(unused_sg)}")
    logger.info(f"Unused Security Group IDs: {list(unused_sg)}\n")

    if dry_run:
        logger.info("Running in dry-run mode. No security groups will be deleted.")

    delete_unused_security_groups(ec2, unused_sg, dry_run, logger)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete unused AWS security groups")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without deleting security groups")
    parser.add_argument(
        "--type",
        choices=["all", "ec2", "rds", "elb"],
        default="all",
        help="Specify the type of security groups to consider (default: all)",
    )
    args = parser.parse_args()

    main(args.dry_run, args.type)
