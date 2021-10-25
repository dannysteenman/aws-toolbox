#!/usr/bin/env python

# This script deletes iam user

import boto3
import argparse

#delete access key attach with user.
def delete_accesskey_for_user(iam_client,user_name):
    try:
        response = iam_client.list_access_keys(UserName=user_name)
        if response['AccessKeyMetadata'] != []:
            for data in response['AccessKeyMetadata']:
                iam_client.delete_access_key(UserName=user_name, AccessKeyId=data['AccessKeyId'])
            print("User Access key Deleted")
    except Exception as e:
        print(e)

#delete Signing Certificates
def delete_signing_certificates(iam_client,user_name):
    try:
        response = iam_client.list_signing_certificates(UserName=user_name)
        if response['Certificates'] != []:
            for data in response['Certificates']:
                iam_client.delete_signing_certificate(UserName=user_name,CertificateId=data['CertificateId'])
            print("User Signing Certificates Deleted")
    except Exception as e:
        print(e)

#delete user login profile
def delete_user_login_profile(iam_client,user_name):
    try:
        response = iam_client.get_login_profile(UserName=user_name)
        if response != {}:
            iam_client.delete_login_profile(UserName=user_name)
            print("User Login Profile Deleted")
    except Exception as e:
        print("No User login Profile Found")

#Deleting 2FA Devices associated with User
def delete_associated_fa_with_user(iam_client,user_name):
    try:
        response = iam_client.list_mfa_devices(UserName=user_name)
        if response['MFADevices'] != []:
            for data in response['MFADevices']:
                iam_client.deactivate_mfa_device(UserName=user_name,SerialNumber=data['SerialNumber'])
            print("User attached MFA Devices Deleted")
    except Exception as e:
        print(e)

#Removing Attached User Policies
def remove_attached_policies(iam_client,user_name):
    try:
        response = iam_client.list_attached_user_policies(UserName=user_name)
        if response['AttachedPolicies'] != []:
            for data in response['AttachedPolicies']:
                iam_client.detach_user_policy(UserName=user_name,PolicyArn=data['PolicyArn'])
            print("User attached Policies Removed")
    except Exception as e:
        print(e)


#deleteing Inline policies
def delete_inline_policies(iam_client,user_name):
    try:
        response = iam_client.list_user_policies(UserName=user_name)
        if response['PolicyNames'] != []:
            for policy_name in response['PolicyNames']:
                iam_client.delete_user_policy(UserName=user_name,PolicyName=policy_name)
            print("User attached Inline Policies Deleted")
    except Exception as e:
        print(e)

#delete user permissions boundary
def delete_permission_boundary(iam_client,user_name):
    try:
        iam_client.delete_user_permissions_boundary(UserName=user_name)
        print("User Permissions Boundary Deleted")
    except Exception as e:
        print("No boundary permissions attached to user")


#remove user from group memberships
def remove_user_from_groups(iam_client,user_name):
    try:
        response = iam_client.list_groups_for_user(UserName=user_name)
        if response['Groups'] != []:
            for data in response['Groups']:
                iam_client.remove_user_from_group(GroupName=data['GroupName'],UserName=user_name)
            print("User Removed from All Groups")
    except Exception as e:
        print(e)


#remove ssh public key
def remove_ssh_public_key(iam_client,user_name):
    try:
        response = iam_client.list_ssh_public_keys(UserName=user_name)
        if response['SSHPublicKeys'] != []:
            for data in response['SSHPublicKeys']:
                iam_client.delete_ssh_public_key(UserName=user_name,SSHPublicKeyId=data['SSHPublicKeyId'])
            print("User Ssh Public Key Deleted")
    except Exception as e:
        print(e)

#delete user from IAM
def delete_user_from_iam(iam_client,user_name):
    try:
        iam_client.delete_user(UserName=user_name)
        print("IAM User- {0} Deleted!".format(user_name))
    except Exception as e:
        print(e)




#main function to delete IAM User
def delete_iam_user(iam_client,user_name):
    delete_accesskey_for_user(iam_client=iam_client, user_name=user_name)
    delete_signing_certificates(iam_client=iam_client, user_name=user_name)
    delete_user_login_profile(iam_client=iam_client, user_name=user_name)
    delete_associated_fa_with_user(iam_client=iam_client, user_name=user_name)
    remove_attached_policies(iam_client=iam_client, user_name=user_name)
    delete_inline_policies(iam_client=iam_client, user_name=user_name)
    delete_permission_boundary(iam_client=iam_client, user_name=user_name)
    remove_ssh_public_key(iam_client=iam_client, user_name=user_name)
    remove_user_from_groups(iam_client=iam_client, user_name=user_name)
    delete_user_from_iam(iam_client=iam_client, user_name=user_name)


def get_args():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--user_name", help="Enter IAM user name which you want to delete",type=str,required=True)
        args = parser.parse_args()
        return args
    except Exception as e:
        print(e)


if __name__ == '__main__':

    try:
        iam_client = boto3.client("iam")
        user_name=get_args().user_name
        print("IAM User who will be deleted: {0}".format(user_name))
        ans=raw_input("Do you want to delete this user? Y/N")
        if ans.lower() == 'y':
            delete_iam_user(iam_client=iam_client,user_name=user_name)
        else:
            print("User not deleted")
    except Exception as e:
        print(e)
