#  https://github.com/dannysteenman/aws-toolbox
#
#  License: MIT
#
# This script finds and deletes all tagged security groups including in- and outbound rules

import boto3


def find_security_groups(ec2_client, tag_key, tag_value_contains):
    # Get all security groups in the region
    response = ec2_client.describe_security_groups()

    # Filter security groups based on the specified tags
    filtered_security_groups = []
    for sg in response["SecurityGroups"]:
        for tag in sg.get("Tags", []):
            if tag.get("Key") == tag_key and tag_value_contains in tag.get("Value", ""):
                filtered_security_groups.append(sg)

    return filtered_security_groups


def revoke_permissions(ec2_client, group_id, permissions):
    for sg in permissions:
        if sg.get("IpPermissions", []):
            for rule in sg.get("IpPermissions", []):
                ec2_client.revoke_security_group_ingress(GroupId=group_id, IpPermissions=[rule])
                print("Revoked ingress IP permissions for Security Group ID: {}".format(group_id))
        if sg.get("IpPermissionsEgress", []):
            for rule in sg.get("IpPermissionsEgress", []):
                ec2_client.revoke_security_group_egress(GroupId=group_id, IpPermissions=[rule])
                print("Revoked egress IP permissions for Security Group ID: {}".format(group_id))


def delete_security_group(ec2_client, group_id):
    ec2_client.delete_security_group(GroupId=group_id)
    print("Deleted Security Group ID: {}".format(group_id))


def main():
    # Fetch AWS account ID from boto3 session
    account_id = boto3.client("sts").get_caller_identity().get("Account")

    aws_region = "eu-central-1"
    ec2_client = boto3.client("ec2", region_name=aws_region)

    # Modify the tag key and value to your own liking
    tag_key = "ManagedByAmazonSageMakerResource"
    tag_value_contains = f"arn:aws:sagemaker:{aws_region}:{account_id}:domain"

    # Find security groups
    tagged_security_groups = find_security_groups(ec2_client, tag_key, tag_value_contains)

    # Iterate through security groups, revoke permissions, and delete
    for sg in tagged_security_groups:
        group_id = sg["GroupId"]

        # Fetch the current ingress and egress IP permissions
        sg = ec2_client.describe_security_groups(Filters=[{"Name": "group-id", "Values": [group_id]}]).get(
            "SecurityGroups", []
        )

        # Revoke permissions
        revoke_permissions(ec2_client, group_id, sg)

        # Delete the security group
        delete_security_group(ec2_client, group_id)


if __name__ == "__main__":
    main()
