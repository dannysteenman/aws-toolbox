# This script finds all unused keypairs

import boto.ec2
import sys

ec2conn = boto.ec2.connect_to_region('eu-west-1')
keypairs = ec2conn.get_all_key_pairs()

all_names = [kp.name for kp in keypairs]
used_keys=[]

for reservation in ec2conn.get_all_reservations():
   [used_keys.append(instance.key_name) for instance in reservation.instances]

used_keys_unique = list(set(used_keys))

unused = list(set(all_names) - set(used_keys_unique))

print "All Keys " + str(len(all_names)) + " : " +str(all_names)
print "Used Keys " + str(len(used_keys_unique))  +" : " + str(used_keys_unique)
print "Unused Keys " + str(len(unused)) +" : "+ str(unused)
