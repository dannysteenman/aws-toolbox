#  https://github.com/dannysteenman/aws-toolbox
#
#  License: MIT
#
# This script returns a list of acounts that are part of an Organizational Unit (OU)

import boto3
import sys

# Check if at least one OU name is provided as command-line argument
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <ou_name1> <ou_name2> ...")
    exit(1)

# Get the list of organizational unit names from the command-line arguments
ou_names = sys.argv[1:]

# Create an AWS Organizations client
organizations = boto3.client("organizations")

# Call the list_roots method to get a list of roots in the organization
response = organizations.list_roots()

# Get the ID of the root
root_id = response["Roots"][0]["Id"]

# Iterate through the list of OU names and get the ID of each OU
ou_ids = []
for ou_name in ou_names:
    # Call the list_organizational_units_for_parent method to get a list of organizational units for the root
    response = organizations.list_organizational_units_for_parent(ParentId=root_id)

    # Use a list comprehension to filter the results by name and get the ID of the first match
    ou_id = [
        ou["Id"] for ou in response["OrganizationalUnits"] if ou["Name"] == ou_name
    ][0]
    ou_ids.append(ou_id)

# Call the list_accounts method for each OU ID to get a list of accounts for each OU
accounts = []
for ou_id in ou_ids:
    response = organizations.list_accounts_for_parent(ParentId=ou_id)
    accounts.extend(response["Accounts"])

print(f"Found the following accounts for organizational units: {ou_names}\n")
for account in accounts:
    print(
        f'Account ID: {account["Id"]}, Account Alias/Name: {account.get("Alias", account["Name"])}'
    )
