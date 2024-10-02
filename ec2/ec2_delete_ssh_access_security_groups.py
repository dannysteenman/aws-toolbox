"""
Description: This script identifies and optionally removes SSH (port 22) inbound rules from all security groups in an AWS account.
It fetches all security groups, checks for SSH inbound rules, and removes them. The script supports a dry-run mode to show which
rules would be removed without actually modifying the security groups.

Key features:
- Automatically uses the region specified in the AWS CLI profile
- Supports dry run mode for safe execution
- Provides detailed logging of all operations, including group rule IDs
- Uses boto3 to interact with AWS EC2 service
- Implements error handling for robustness

Usage:
python ec2_remove_ssh_from_security_groups.py [--dry-run] [--profile PROFILE_NAME]

Author: [Your Name]
License: MIT
"""

import argparse
import logging

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


def get_all_security_groups(ec2_client):
    try:
        security_groups = []
        paginator = ec2_client.get_paginator("describe_security_groups")
        for page in paginator.paginate():
            security_groups.extend(page["SecurityGroups"])
        logger.info(f"Total Security Groups: {len(security_groups)}")
        return security_groups
    except ClientError as e:
        logger.error(f"Failed to retrieve security groups: {e}")
        return []


def has_ssh_rule(security_group):
    for rule in security_group.get("IpPermissions", []):
        if rule.get("FromPort") == 22 and rule.get("ToPort") == 22 and rule.get("IpProtocol") == "tcp":
            return True
    return False


def remove_ssh_rule(ec2_client, security_group, dry_run=False):
    group_id = security_group["GroupId"]
    group_name = security_group["GroupName"]
    ssh_rules = [
        rule
        for rule in security_group.get("IpPermissions", [])
        if rule.get("FromPort") == 22 and rule.get("ToPort") == 22 and rule.get("IpProtocol") == "tcp"
    ]

    if not ssh_rules:
        logger.info(f"No SSH rules found in security group: {group_id} ({group_name})")
        return False

    logger.info(f"{'Would remove' if dry_run else 'Removing'} SSH rules from security group: {group_id} ({group_name})")

    # Fetch the security group rules with their IDs
    try:
        response = ec2_client.describe_security_group_rules(Filters=[{"Name": "group-id", "Values": [group_id]}])
        sg_rules = {rule["SecurityGroupRuleId"]: rule for rule in response["SecurityGroupRules"]}
    except ClientError as e:
        logger.error(f"Failed to fetch security group rules for {group_id}: {e}")
        return False

    for rule in ssh_rules:
        # Find matching rule(s) in sg_rules
        matching_rules = [
            sg_rule
            for sg_rule in sg_rules.values()
            if sg_rule["IpProtocol"] == rule["IpProtocol"]
            and sg_rule["FromPort"] == rule["FromPort"]
            and sg_rule["ToPort"] == rule["ToPort"]
            and sg_rule["IsEgress"] == False  # Inbound rules
        ]

        for matching_rule in matching_rules:
            rule_id = matching_rule["SecurityGroupRuleId"]
            cidr_range = matching_rule.get("CidrIpv4", "N/A")
            logger.info(f"  Rule ID: {rule_id}")
            logger.info(f"    Port Range: {matching_rule['FromPort']}-{matching_rule['ToPort']}")
            logger.info(f"    Protocol: {matching_rule['IpProtocol']}")
            logger.info(f"    CIDR Range: {cidr_range}")

    if not dry_run:
        try:
            ec2_client.revoke_security_group_ingress(GroupId=group_id, IpPermissions=ssh_rules)
            logger.info(f"Successfully removed SSH rules from security group: {group_id} ({group_name})")
            return True
        except ClientError as e:
            logger.error(f"Failed to remove SSH rules from security group {group_id} ({group_name}): {e}")
            return False
    return True


def main(dry_run=False):
    ec2_client = get_ec2_client()
    security_groups = get_all_security_groups(ec2_client)

    affected_groups = 0
    for sg in security_groups:
        if has_ssh_rule(sg):
            if remove_ssh_rule(ec2_client, sg, dry_run):
                affected_groups += 1

    # Summary
    logger.info("Summary:")
    logger.info(f"  Total Security Groups: {len(security_groups)}")
    logger.info(f"  Security Groups with SSH rules {'that would be' if dry_run else ''} modified: {affected_groups}")


if __name__ == "__main__":
    logger = setup_logging()

    parser = argparse.ArgumentParser(description="Remove SSH (port 22) inbound rules from EC2 Security Groups")
    parser.add_argument(
        "--dry-run", action="store_true", help="Perform a dry run without actually modifying security groups"
    )
    args = parser.parse_args()

    main(dry_run=args.dry_run)
