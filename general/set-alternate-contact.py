#  https://github.com/dannysteenman/aws-toolbox
#
#  License: MIT
#
# This script sets alternate contacts (security, billing, and operations) for all AWS accounts
# in an organization using the AWS Organizations and Account APIs. It supports a dry run mode
# for testing without making actual changes.

import argparse
import json

import boto3

# JSON structure for contact details
contacts = {
    "securityContact": {
        "name": "John Doe",
        "title": "Security Manager",
        "emailAddress": "john.doe@example.com",
        "phoneNumber": "+1234567890",
    },
    "billingContact": {
        "name": "Jane Smith",
        "title": "Finance Director",
        "emailAddress": "jane.smith@example.com",
        "phoneNumber": "+1987654321",
    },
    "operationsContact": {
        "name": "Bob Johnson",
        "title": "Operations Lead",
        "emailAddress": "bob.johnson@example.com",
        "phoneNumber": "+1122334455",
    },
}


def get_all_accounts(organizations_client):
    """Retrieve all account IDs in the organization."""
    account_ids = []
    paginator = organizations_client.get_paginator("list_accounts")

    for page in paginator.paginate():
        for account in page["Accounts"]:
            account_ids.append(account["Id"])

    return account_ids


def set_alternate_contact(account_client, account_id, contact_type, contact_info, dry_run=False):
    """Set alternate contact for a specific account."""
    try:
        print(f"{'[DRY RUN] ' if dry_run else ''}Setting {contact_type} contact for account {account_id}")
        if not dry_run:
            account_client.put_alternate_contact(
                AccountId=account_id,
                AlternateContactType=contact_type.upper(),
                EmailAddress=contact_info["emailAddress"],
                Name=contact_info["name"],
                PhoneNumber=contact_info["phoneNumber"],
                Title=contact_info["title"],
            )
        print(f"{'[DRY RUN] ' if dry_run else ''}Successfully set {contact_type} contact for account {account_id}")
        print(f"{'[DRY RUN] ' if dry_run else ''}Contact details:")
        print(json.dumps(contact_info, indent=2))
    except account_client.exceptions.ValidationException as e:
        print(f"Error setting {contact_type} contact for account {account_id}: {str(e)}")
    except Exception as e:
        print(f"Unexpected error setting {contact_type} contact for account {account_id}: {str(e)}")


def main(dry_run=False):
    # Initialize AWS clients
    account = boto3.client("account")
    organizations = boto3.client("organizations")

    # Get all account IDs in the organization
    account_ids = get_all_accounts(organizations)
    print(f"Found {len(account_ids)} accounts in the organization.")

    # Set alternate contacts for each account
    for account_id in account_ids:
        set_alternate_contact(account, account_id, "SECURITY", contacts["securityContact"], dry_run)
        set_alternate_contact(account, account_id, "BILLING", contacts["billingContact"], dry_run)
        set_alternate_contact(account, account_id, "OPERATIONS", contacts["operationsContact"], dry_run)

        print(f"{'[DRY RUN] ' if dry_run else ''}Alternate contacts set for account {account_id}")
        print("---")

    print(f"{'[DRY RUN] ' if dry_run else ''}Process completed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set alternate contacts for AWS accounts in an organization.")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without making actual changes")
    args = parser.parse_args()

    main(dry_run=args.dry_run)
