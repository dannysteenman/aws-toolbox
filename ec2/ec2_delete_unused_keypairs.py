#  https://github.com/dannysteenman/aws-toolbox
#
#  License: MIT
#
# This script finds and deletes all unused EC2 keypairs in a single AWS Region

import boto3

ec2 = boto3.resource("ec2")
key_pairs = ec2.key_pairs.all()

used_keys = set([instance.key_name for instance in ec2.instances.all()])
unused_keys = [
    key_pair.name for key_pair in key_pairs if key_pair.name not in used_keys
]

for key_name in unused_keys:
    ec2.KeyPair(key_name).delete()

print(f"Deleted {len(unused_keys)} unused key pairs.")
