#  https://github.com/dannysteenman/aws-toolbox
#
#  License: MIT
#
# This script imports users and groups from a CSV file into AWS SSO and adding the users to their respective groups.
# Use the example `sso_users.csv` file that's provided in this directory.

import boto3
import csv
import argparse
import os

# Create boto3 clients
sso_admin_client = boto3.client("sso-admin")
identitystore_client = boto3.client("identitystore")


# Function to get Identity Store information
def get_instance_information():
    response = sso_admin_client.list_instances()
    if not response["Instances"]:
        raise ValueError("No SSO instances found")
    instance_info = response["Instances"][0]
    return instance_info["IdentityStoreId"]


# Function to find a group based on group name
def find_group(identity_store_id, group_name):
    next_token = None
    while True:
        kwargs = {"IdentityStoreId": identity_store_id}
        if next_token:
            kwargs["NextToken"] = next_token
        response = identitystore_client.list_groups(**kwargs)

        for group in response["Groups"]:
            if group["DisplayName"] == group_name:
                return group["GroupId"]
        next_token = response.get("NextToken")
        if not next_token:
            break
    return None


# Function to create a group based on group name
def create_group(identity_store_id, group_name):
    group = identitystore_client.create_group(
        IdentityStoreId=identity_store_id,
        DisplayName=group_name,
    )
    print(f"Group {group_name} created")
    return group["GroupId"]


# Function to create a group if it doesn't exist
def create_group_if_not_exists(identity_store_id, group_name):
    group_id = find_group(identity_store_id, group_name)
    if not group_id:
        group_id = create_group(identity_store_id, group_name)
    return group_id


# Function to create a user based on first name, last name, and email
def create_user(identity_store_id, first_name, last_name, email):
    user_id = find_user_by_email(identity_store_id, email)

    if user_id:
        print(f"User {email} already exists.")
        return user_id

    try:
        response = identitystore_client.create_user(
            IdentityStoreId=identity_store_id,
            UserName=email,
            Name={
                "Formatted": f"{first_name} {last_name}",
                "FamilyName": last_name,
                "GivenName": first_name,
            },
            DisplayName=f"{first_name} {last_name}",
            Emails=[{"Value": email, "Type": "Work", "Primary": True}],
        )
        user_id = response["UserId"]
        print(f"Created user {email}")
        return user_id
    except identitystore_client.exceptions.ResourceNotFoundException as e:
        print(f"Error creating user for {email}: {e}")
        return None
    except identitystore_client.exceptions.ValidationException as e:
        print(f"Error creating user for {email}: {e}")
        return None


# Function to create a user based on first name, last name, and email
def find_user_by_email(identity_store_id, email):
    try:
        response = identitystore_client.list_users(
            IdentityStoreId=identity_store_id,
            Filters=[{"AttributePath": "UserName", "AttributeValue": email}],
        )

        users = response["Users"]
        if users:
            user_id = users[0]["UserId"]
            return user_id
        else:
            return None

    except identitystore_client.exceptions.ResourceNotFoundException:
        return None


# Function to add a user to a group
def add_user_to_group(identity_store_id, user_id, group_id, email, group_name):
    try:
        identitystore_client.create_group_membership(
            IdentityStoreId=identity_store_id,
            GroupId=group_id,
            MemberId={"UserId": user_id},
        )
        print(f"Added user {email} to group {group_name}")
    except identitystore_client.exceptions.ResourceNotFoundException as e:
        print(f"Error adding user {email} to group {group_name}: {e}")
    except identitystore_client.exceptions.ConflictException:
        print(f"User {email} is already a member of group {group_name}")


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Import users from a CSV file to AWS SSO"
    )
    parser.add_argument(
        "csv_file", help="The CSV file containing users and their group information"
    )
    args = parser.parse_args()

    # Get the absolute path of the CSV file
    current_working_directory = os.getcwd()
    abs_csv_file = os.path.join(current_working_directory, args.csv_file)

    # Check if the file exists
    if not os.path.isfile(abs_csv_file):
        raise ValueError(f"CSV file {abs_csv_file} not found")

    identity_store_id = get_instance_information()

    # Read the CSV file and process each row
    with open(abs_csv_file, newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # Skip the header row
        for row in reader:
            first_name, last_name, email, group_name = row
            group_id = create_group_if_not_exists(identity_store_id, group_name)
            if group_id:
                user_id = create_user(identity_store_id, first_name, last_name, email)
                if user_id is not None:
                    add_user_to_group(
                        identity_store_id, user_id, group_id, email, group_name
                    )


if __name__ == "__main__":
    main()
