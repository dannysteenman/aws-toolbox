#  https://github.com/dannysteenman/aws-toolbox
#
# This script deletes iam users

import argparse
import boto3


def delete_access_keys(iam_client, user_name):
    response = iam_client.list_access_keys(UserName=user_name)
    for access_key in response.get("AccessKeyMetadata", []):
        iam_client.delete_access_key(
            UserName=user_name, AccessKeyId=access_key["AccessKeyId"]
        )
    if response.get("AccessKeyMetadata"):
        print("Access keys deleted.")


def delete_signing_certificates(iam_client, user_name):
    response = iam_client.list_signing_certificates(UserName=user_name)
    for certificate in response.get("Certificates", []):
        iam_client.delete_signing_certificate(
            UserName=user_name, CertificateId=certificate["CertificateId"]
        )
    if response.get("Certificates"):
        print("Signing certificates deleted.")


def delete_login_profile(iam_client, user_name):
    try:
        iam_client.delete_login_profile(UserName=user_name)
        print("Login profile deleted.")
    except iam_client.exceptions.NoSuchEntityException:
        print("No login profile found.")


def delete_mfa_devices(iam_client, user_name):
    response = iam_client.list_mfa_devices(UserName=user_name)
    for device in response.get("MFADevices", []):
        iam_client.deactivate_mfa_device(
            UserName=user_name, SerialNumber=device["SerialNumber"]
        )
    if response.get("MFADevices"):
        print("MFA devices deleted.")


def detach_policies(iam_client, user_name):
    response = iam_client.list_attached_user_policies(UserName=user_name)
    for policy in response.get("AttachedPolicies", []):
        iam_client.detach_user_policy(UserName=user_name, PolicyArn=policy["PolicyArn"])
    if response.get("AttachedPolicies"):
        print("Attached policies removed.")


def delete_inline_policies(iam_client, user_name):
    response = iam_client.list_user_policies(UserName=user_name)
    for policy_name in response.get("PolicyNames", []):
        iam_client.delete_user_policy(UserName=user_name, PolicyName=policy_name)
    if response.get("PolicyNames"):
        print("Inline policies deleted.")


def delete_permission_boundary(iam_client, user_name):
    try:
        iam_client.delete_user_permissions_boundary(UserName=user_name)
        print("Permissions boundary deleted.")
    except iam_client.exceptions.NoSuchEntityException:
        print("No permissions boundary found.")


def remove_user_from_groups(iam_client, user_name):
    response = iam_client.list_groups_for_user(UserName=user_name)
    for group in response.get("Groups", []):
        iam_client.remove_user_from_group(
            GroupName=group["GroupName"], UserName=user_name
        )
    if response.get("Groups"):
        print("Removed user from groups.")


def delete_ssh_public_keys(iam_client, user_name):
    response = iam_client.list_ssh_public_keys(UserName=user_name)
    for ssh_key in response.get("SSHPublicKeys", []):
        iam_client.delete_ssh_public_key(
            UserName=user_name, SSHPublicKeyId=ssh_key["SSHPublicKeyId"]
        )
    if response.get("SSHPublicKeys"):
        print("SSH public keys deleted.")


def delete_iam_user(iam_client, user_name):
    delete_access_keys(iam_client, user_name)
    delete_signing_certificates(iam_client, user_name)
    delete_login_profile(iam_client, user_name)
    delete_mfa_devices(iam_client, user_name)
    detach_policies(iam_client, user_name)
    delete_inline_policies(iam_client, user_name)
    delete_permission_boundary(iam_client, user_name)
    remove_user_from_groups(iam_client, user_name)
