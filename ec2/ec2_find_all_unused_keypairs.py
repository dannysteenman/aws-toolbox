#  https://github.com/dannysteenman/aws-toolbox
#
#  License: MIT
#
# This script finds all used and unused EC2 keypairs in all AWS Regions

import boto3

ec2 = boto3.client("ec2")

all_keys = []
used_keys = set()
unused_keys = []

for region in ec2.describe_regions()["Regions"]:
    region_name = region["RegionName"]
    try:
        ec2conn = boto3.resource("ec2", region_name=region_name)
        key_pairs = ec2conn.key_pairs.all()
        all_keys += [f"{key_pair.name} ({region_name})" for key_pair in key_pairs]
        used_keys.update([instance.key_name for instance in ec2conn.instances.all()])
    except Exception as e:
        print(f"No access to region {region_name}: {e}")

unused_keys = list(set([key.split(" (")[0] for key in all_keys]) - used_keys)

print(f"All Keys: {len(all_keys)} : {sorted(all_keys)}")
print(f"Used Keys: {len(used_keys)} : {used_keys}")
print(f"Unused Keys: {len(unused_keys)} : {sorted(unused_keys)}")
