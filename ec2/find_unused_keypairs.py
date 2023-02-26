#  https://github.com/dannysteenman/aws-toolbox
#
#  License: MIT
#
# This script finds all used and unused EC2 keypairs in a single region

import boto3

ec2 = boto3.resource("ec2")
key_pairs = ec2.key_pairs.all()

all_keys = [key_pair.name for key_pair in key_pairs]
used_keys = set([instance.key_name for instance in ec2.instances.all()])
unused_keys = [
    key_pair.name for key_pair in key_pairs if key_pair.name not in used_keys
]

print(f"All Keys: {len(all_keys)} : {all_keys}")
print(f"Used Keys: {len(used_keys)} : {used_keys}")
print(f"Unused Keys: {len(unused_keys)} : {unused_keys}")
