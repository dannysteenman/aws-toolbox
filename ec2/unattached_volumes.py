# This script list all unattached volumes

import boto.ec2

regions = boto.ec2.regions()
count = 0
for region in regions:
    try:
        ec2conn = boto.ec2.connect_to_region(region.name)
        vols =  ec2conn.get_all_volumes()
        unattached_volumes = [ volume for volume in vols if volume.attachment_state() ==  None ]
        count = count + len(unattached_volumes)
        print "Total of " + str(len(unattached_volumes)) + " unattached volumes in regions " + str(region.name)
    except:
        print "No Access To Region : " + region.name

print "Total " + str(count) + " unattached Volumes"
