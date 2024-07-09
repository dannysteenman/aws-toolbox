#  https://github.com/dannysteenman/aws-toolbox
#
#  License: MIT
#
# This script returns a list of acounts that are part of an Organizational Unit (OU)

import boto3
import sys


def get_ou_for_account(account_id, root_id):
    response = organizations.list_parents(ChildId=account_id)
    parent_id = response["Parents"][0]["Id"]

    if parent_id == root_id:
        return "Root"
    else:
        response = organizations.describe_organizational_unit(
            OrganizationalUnitId=parent_id
        )
        return response["OrganizationalUnit"]["Name"]


# Get the list of organizational unit names from the command-line arguments
ou_names = sys.argv[1:]

# Create an AWS Organizations client
organizations = boto3.client("organizations")

# Call the list_roots method to get a list of roots in the organization
response = organizations.list_roots()

# Get the ID of the root
root_id = response["Roots"][0]["Id"]

if not ou_names:
    # If no OU names are provided, list all accounts in the organization
    response = organizations.list_accounts()
    accounts = response["Accounts"]
    print("Found the following accounts for the organization:\n")

    for account in accounts:
        ou_name = get_ou_for_account(account["Id"], root_id)
        print(
            f'Account ID: {account["Id"]}, Account Alias/Name: {account.get("Alias", account["Name"])}, Organizational Unit: {ou_name}'
        )
else:
    # Iterate through the list of OU names and get the ID of each OU
    ou_ids = []
    for ou_name in ou_names:
        # Call the list_organizational_units_for_parent method to get a list of organizational units for the root
        response = organizations.list_organizational_units_for_parent(ParentId=root_id)

        # Use a list comprehension to filter the results by name (case-insensitive) and get the ID of the first match
        ou_id = [
            ou["Id"]
            for ou in response["OrganizationalUnits"]
            if ou["Name"].lower() == ou_name.lower()
        ][0]
        ou_ids.append(ou_id)

    # Call the list_accounts method for each parent ID (OU or root) to get a list of accounts
    accounts = []
    for parent_id in ou_ids:
        response = organizations.list_accounts_for_parent(ParentId=parent_id)
        accounts.extend(response["Accounts"])

    print(f"Found the following accounts for organizational units: {ou_names}\n")

    for account in accounts:
        print(
            f'Account ID: {account["Id"]}, Account Alias/Name: {account.get("Alias", account["Name"])}'
        )
