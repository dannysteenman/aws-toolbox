#  https://github.com/dannysteenman/aws-toolbox
#
#  License: MIT
#
# This script deletes all stack instances associated with a stackset and the stackset itself

import boto3
import sys
import botocore

# Set the region and stackset name
region = "eu-west-1"  # Change to your desired region
retain_stacks = True  # Choose if you wish to retain the stacks on the target accounts

# Check if stackset_name is provided as command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <stackset_name>")
    exit(1)

stackset_name = sys.argv[1]

# Create a CloudFormation client
cf = boto3.client("cloudformation", region_name=region)

# Get the list of stack instances associated with the stackset
response = cf.list_stack_instances(StackSetName=stackset_name)

# Check if there are any stack instances to delete
if not response["Summaries"]:
    print(f"No stack instances found for stackset {stackset_name}")
    print(f"Proceeding deletion of stackset: {stackset_name}")
    cf.delete_stack_set(StackSetName=stackset_name)
    exit()

# Get a list of unique account IDs and regions
accounts = list(set([instance["Account"] for instance in response["Summaries"]]))
regions = list(set([instance["Region"] for instance in response["Summaries"]]))


def get_root_ou_id():
    """
    Returns the ID of the root organizational unit (OU) in AWS Organizations.
    """
    # Create an Organizations client
    org_client = boto3.client("organizations")

    # Retrieve the list of roots
    roots = org_client.list_roots()["Roots"]

    # There should only be one root
    if len(roots) != 1:
        raise ValueError("Expected 1 root, found %d" % len(roots))

    # Retrieve the root OU ID
    root_id = roots[0]["Id"]

    return root_id


# Delete stack instances for this account and region
try:
    print(f"Deleting stackset instances for accounts: {accounts}")
    cf.delete_stack_instances(
        StackSetName=stackset_name,
        Accounts=accounts,
        Regions=regions,
        RetainStacks=retain_stacks,
    )
except botocore.exceptions.ClientError as error:
    # Check if error is due to SERVICE_MANAGED permission model
    if "SERVICE_MANAGED permission model" in str(error):
        cf.delete_stack_instances(
            StackSetName=stackset_name,
            Regions=regions,
            RetainStacks=retain_stacks,
            DeploymentTargets={
                "OrganizationalUnitIds": [
                    get_root_ou_id(),
                ],
            },
        )
    else:
        raise error
