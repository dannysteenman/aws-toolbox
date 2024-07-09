#  https://github.com/dannysteenman/aws-toolbox
#
#  License: MIT
#
# This script assigns AWS Single Sign-On (SSO) access to a specified principal (user or group) for multiple AWS accounts within a specified Organizational Unit (OU).
# It automates the process of granting permissions to the principal using a specified permission set, streamlining the management of access control across multiple accounts in an organization.

import boto3

# Replace these variables with your values
PRINCIPAL_NAME = "Administrators"  # e.g., 'user_name' or 'group_name'
PRINCIPAL_TYPE = "GROUP"  # e.g., 'USER' or 'GROUP'
PERMISSION_SET_NAME = "AdministratorAccess"
OU_NAME = "Sandbox"  # Replace with the OU name you want to fetch accounts from


# Create boto3 clients
sso_admin_client = boto3.client("sso-admin")
identitystore_client = boto3.client("identitystore")
organizations = boto3.client("organizations")


# Function to get instance information from AWS SSO
def get_instance_information():
    response = sso_admin_client.list_instances()
    if not response["Instances"]:
        raise ValueError("No SSO instances found")
    instance_info = response["Instances"][0]
    return instance_info["InstanceArn"], instance_info["IdentityStoreId"]


# Function to get account IDs in an Organizational Unit (OU) given its name
def get_accounts_in_ou(ou_name):
    response = organizations.list_roots()
    root_id = response["Roots"][0]["Id"]

    response = organizations.list_organizational_units_for_parent(ParentId=root_id)
    ou_id = next(
        (ou["Id"] for ou in response["OrganizationalUnits"] if ou["Name"] == ou_name),
        None,
    )

    if not ou_id:
        raise ValueError(f"Organizational Unit not found: {ou_name}")

    response = organizations.list_accounts_for_parent(ParentId=ou_id)
    accounts = response["Accounts"]

    return [account["Id"] for account in accounts]


# Get the principal ID for the specified principal name and type
def get_principal_id(identity_store_id, principal_name, principal_type):
    filter = {
        "AttributePath": "UserName" if principal_type == "USER" else "DisplayName",
        "AttributeValue": principal_name,
    }
    response = (
        identitystore_client.list_users(
            IdentityStoreId=identity_store_id, Filters=[filter]
        )
        if principal_type == "USER"
        else identitystore_client.list_groups(
            IdentityStoreId=identity_store_id, Filters=[filter]
        )
    )

    if not response.get("Users") and not response.get("Groups"):
        raise ValueError(f"Principal not found: {principal_name}")

    principal_id = (
        response["Users"][0]["UserId"]
        if principal_type == "USER"
        else response["Groups"][0]["GroupId"]
    )
    return principal_id


# Get the Permission Set ARN for the specified Permission Set name
def get_permission_set_arn(instance_arn, permission_set_name):
    response = sso_admin_client.list_permission_sets(InstanceArn=instance_arn)

    for permission_set_arn in response["PermissionSets"]:
        permission_set = sso_admin_client.describe_permission_set(
            InstanceArn=instance_arn, PermissionSetArn=permission_set_arn
        )
        if permission_set["PermissionSet"]["Name"] == permission_set_name:
            return permission_set_arn

    raise ValueError(f"Permission set not found: {permission_set_name}")


# Assign access to the principal for each account in the OU
def assign_access_to_principal(
    instance_arn, principal_id, account_id, permission_set_arn
):
    sso_admin_client.create_account_assignment(
        InstanceArn=instance_arn,
        TargetId=account_id,
        TargetType="AWS_ACCOUNT",
        PrincipalType=PRINCIPAL_TYPE,
        PrincipalId=principal_id,
        PermissionSetArn=permission_set_arn,
    )
    print(
        f"Assigned {PRINCIPAL_TYPE} {PRINCIPAL_NAME} with Permission Set {PERMISSION_SET_NAME} in AWS Account {account_id}"
    )


def main():
    instance_arn, identity_store_id = get_instance_information()
    principal_id = get_principal_id(identity_store_id, PRINCIPAL_NAME, PRINCIPAL_TYPE)
    permission_set_arn = get_permission_set_arn(instance_arn, PERMISSION_SET_NAME)
    account_ids = get_accounts_in_ou(OU_NAME)

    for account_id in account_ids:
        assign_access_to_principal(
            instance_arn, principal_id, account_id, permission_set_arn
        )


if __name__ == "__main__":
    main()
