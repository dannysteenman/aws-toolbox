#!/usr/bin/env python3

"""
File: create_sso_users.py
Description: This script creates AWS IAM Identity Center (SSO) users from a list of email addresses,
             extracts first and last names when available, and optionally assigns them to a group.
Author: Danny Steenman
License: MIT
"""

import argparse
import re

import boto3
from botocore.exceptions import ClientError


def parse_name_from_email(email):
    """
    Extracts first name and last name from an email address if possible.

    Args:
    email (str): Email address to parse.

    Returns:
    tuple: (first_name, last_name)
    """
    name_part = email.split("@")[0]
    name_parts = re.split(r"[._]", name_part)

    if len(name_parts) >= 2:
        return name_parts[0].capitalize(), name_parts[-1].capitalize()
    else:
        return name_part.capitalize(), "User"


def create_sso_users(emails, group_name=None):
    """
    Creates SSO users from a list of email addresses and optionally assigns them to a group.

    Args:
    emails (list): List of email addresses to create SSO users for.
    group_name (str, optional): Name of the group to assign users to.

    Returns:
    tuple: A tuple containing two lists - successful creations and failures.
    """
    sso_admin = boto3.client("sso-admin")
    identitystore = boto3.client("identitystore")

    # Get the Instance ARN and Identity Store ID
    instances = sso_admin.list_instances()
    if not instances["Instances"]:
        print("No SSO instance found.")
        return [], emails

    instance_arn = instances["Instances"][0]["InstanceArn"]
    identity_store_id = instances["Instances"][0]["IdentityStoreId"]

    successful = []
    failed = []

    # If a group is specified, check if it exists
    group_id = None
    if group_name:
        try:
            group_response = identitystore.list_groups(
                IdentityStoreId=identity_store_id,
                Filters=[{"AttributePath": "DisplayName", "AttributeValue": group_name}],
            )
            if group_response["Groups"]:
                group_id = group_response["Groups"][0]["GroupId"]
            else:
                print(f"Group '{group_name}' not found. Users will be created without group assignment.")
        except ClientError as e:
            print(f"Error checking group: {e}")
            return [], emails

    for email in emails:
        try:
            # Parse name from email
            first_name, last_name = parse_name_from_email(email)

            # Create user
            user_response = identitystore.create_user(
                IdentityStoreId=identity_store_id,
                UserName=email,
                Name={"GivenName": first_name, "FamilyName": last_name},
                DisplayName=f"{first_name} {last_name}",
                Emails=[{"Value": email, "Type": "Work", "Primary": True}],
            )

            # If group_id is available, add user to the group
            if group_id:
                identitystore.create_group_membership(
                    IdentityStoreId=identity_store_id, GroupId=group_id, MemberId={"UserId": user_response["UserId"]}
                )

            successful.append(email)
            print(f"Successfully created user: {email} ({first_name} {last_name})")
        except ClientError as e:
            print(f"Failed to create user {email}: {e}")
            failed.append(email)

    return successful, failed


def main():
    parser = argparse.ArgumentParser(description="Create SSO users from a list of email addresses.")
    parser.add_argument("--emails", nargs="+", required=True, help="List of email addresses")
    parser.add_argument("--group", help="Optional group name to assign users to")
    args = parser.parse_args()

    successful, failed = create_sso_users(args.emails, args.group)

    print("\nSummary:")
    print(f"Successfully created users: {len(successful)}")
    print(f"Failed to create users: {len(failed)}")

    if failed:
        print("\nFailed email addresses:")
        for email in failed:
            print(email)


if __name__ == "__main__":
    main()
