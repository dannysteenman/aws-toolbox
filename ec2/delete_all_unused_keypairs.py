#  https://github.com/dannysteenman/aws-toolbox
#
#  License: MIT
#
# This script finds and deletes all unused EC2 keypairs in all AWS Regions

import boto3

ec2 = boto3.resource("ec2")

unused_keys = {}

for region in ec2.meta.client.describe_regions()["Regions"]:
    region_name = region["RegionName"]
    try:
        ec2conn = boto3.resource("ec2", region_name=region_name)
        key_pairs = ec2conn.key_pairs.all()
        used_keys = set([instance.key_name for instance in ec2conn.instances.all()])
        for key_pair in key_pairs:
            if key_pair.name not in used_keys:
                unused_keys[key_pair.name] = region_name
                key_pair.delete()
                print(
                    f"Deleted unused key pair {key_pair.name} in region {region_name}"
                )
    except Exception as e:
        print(f"No access to region {region_name}: {e}")

print(f"Found and deleted {len(unused_keys)} unused key pairs across all regions:")
print(unused_keys)
