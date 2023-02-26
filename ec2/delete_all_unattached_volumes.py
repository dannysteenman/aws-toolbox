#  https://github.com/dannysteenman/aws-toolbox
#
#  License: MIT
#
# This script deletes all unattached EBS volumes in all AWS Regions

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
        for volume in unattached_volumes:
            count += 1
            volume.delete()
            print(f"Deleted unattached volume {volume.id} in region {region_name}")
    except Exception as e:
        print(f"No access to region {region_name}: {e}")

if count > 0:
    print(f"Deleted {count} unattached volumes")
