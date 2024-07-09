#  https://github.com/dannysteenman/aws-toolbox
#
#  License: MIT
#
# This script finds all unattached EBS volumes in all AWS Regions

import boto3

ec2 = boto3.client("ec2")

count = 0
for region in ec2.describe_regions()["Regions"]:
    region_name = region["RegionName"]
    try:
        ec2conn = boto3.resource("ec2", region_name=region_name)
        unattached_volumes = [
            volume for volume in ec2conn.volumes.all() if not volume.attachments
        ]
        num_unattached_volumes = len(unattached_volumes)
        count += num_unattached_volumes
        if num_unattached_volumes > 0:
            print(
                f"Total of {num_unattached_volumes} unattached volumes in region {region_name}"
            )
    except Exception as e:
        print(f"No access to region {region_name}: {e}")

if count > 0:
    print(f"Total of {count} unattached volumes")
