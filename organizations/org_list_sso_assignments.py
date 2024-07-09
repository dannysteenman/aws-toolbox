#  https://github.com/dannysteenman/aws-toolbox
#
#  License: MIT
#
# The script lists all AWS accounts along with their assigned users, groups, and permission sets in a structured JSON format.

import boto3
import json

# Create boto3 clients
sso_admin_client = boto3.client("sso-admin")
identitystore_client = boto3.client("identitystore")
organizations = boto3.client("organizations")


# Function to get all AWS accounts
def get_all_accounts():
    accounts = []
    paginator = organizations.get_paginator("list_accounts")
    for page in paginator.paginate():
        accounts.extend(page["Accounts"])
    return accounts


# Function to get all permission sets
def get_all_permission_sets(instance_arn):
    permission_sets = []
    paginator = sso_admin_client.get_paginator("list_permission_sets")
    for page in paginator.paginate(InstanceArn=instance_arn):
        permission_sets.extend(page["PermissionSets"])
    return permission_sets


# Function to get account assignments
def get_account_assignments(account_id, instance_arn, permission_set_arn):
    assignments = []
    paginator = sso_admin_client.get_paginator("list_account_assignments")

    for page in paginator.paginate(
        InstanceArn=instance_arn,
        AccountId=account_id,
        PermissionSetArn=permission_set_arn,
    ):
        assignments.extend(page["AccountAssignments"])

    return assignments


# Function to get instance information from AWS SSO
def get_instance_information():
    response = sso_admin_client.list_instances()
    if not response["Instances"]:
        raise ValueError("No SSO instances found")
    instance_info = response["Instances"][0]
    return instance_info["InstanceArn"], instance_info["IdentityStoreId"]


# Main function
def main():
    instance_arn, identity_store_id = get_instance_information()
    aws_accounts = get_all_accounts()
    permission_sets = get_all_permission_sets(instance_arn)
    all_account_results = []

    for account in aws_accounts:
        account_id = account["Id"]
        account_name = account["Name"]
        account_email = account["Email"]

        account_result = {
            "Name": account_name,
            "Id": account_id,
            "Email": account_email,
            "Assignments": [],
        }

        for permission_set_arn in permission_sets:
            account_assignments = get_account_assignments(
                account_id, instance_arn, permission_set_arn
            )

            for assignment in account_assignments:
                try:
                    principal_type = assignment["PrincipalType"]
                    principal_id = assignment["PrincipalId"]

                    principal = (
                        identitystore_client.describe_user(
                            IdentityStoreId=identity_store_id, UserId=principal_id
                        )
                        if principal_type == "USER"
                        else identitystore_client.describe_group(
                            IdentityStoreId=identity_store_id, GroupId=principal_id
                        )
                    )

                    principal_name = principal.get("UserName", principal["DisplayName"])
                    permission_set_arn = assignment["PermissionSetArn"]
                    permission_set = sso_admin_client.describe_permission_set(
                        InstanceArn=instance_arn, PermissionSetArn=permission_set_arn
                    )

                    permission_set_name = permission_set["PermissionSet"]["Name"]

                    account_result["Assignments"].append(
                        {
                            "PrincipalType": principal_type,
                            "PrincipalName": principal_name,
                            "PermissionSetName": permission_set_name,
                        }
                    )

                except identitystore_client.exceptions.ResourceNotFoundException:
                    print(f"Resource not found: {assignment}")
                    continue

            all_account_results.append(account_result)

    # Output the JSON
    output = {"Accounts": all_account_results}
    print(json.dumps(output, indent=4))


if __name__ == "__main__":
    main()
