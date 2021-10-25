#!/usr/bin/python

# This program list all the security groups which are in used and not used

import boto3
import boto.ec2.elb

if __name__ == "__main__":
    getRegion = boto.ec2.get_region("eu-west-1")
    used_SG=[]
    total_SG=[]
    #Find EC2 instances security group in used.
    ec2=boto.connect_ec2(region=getRegion)
    sgs=ec2.get_all_security_groups()
    for sg in sgs:
        total_SG.append(sg.id)
        if len(sg.instances()) != 0:
            used_SG.append(sg.id)


    #Find Classic load balancer security group in used
    elb=boto3.client('elb')
    response=elb.describe_load_balancers()
    if response["LoadBalancerDescriptions"] != []:
        for dict in response["LoadBalancerDescriptions"]:
            if 'SecurityGroups' in dict.keys():
                for sg_id in dict['SecurityGroups']:
                    used_SG.append(sg_id)

    # Find Application load balancer security group in used
    elb = boto3.client('elbv2')
    elb_response=elb.describe_load_balancers()
    if elb_response["LoadBalancers"] != []:
        for dict in elb_response["LoadBalancers"]:
            if 'SecurityGroups' in dict.keys():
                for sg_id in dict['SecurityGroups']:
                    used_SG.append(sg_id)

    #Find RDS db security group in used
    rds=boto3.client('rds')
    response=rds.describe_db_instances()
    if response["DBInstances"] != []:
        for dict in response["DBInstances"]:
            for id in dict['VpcSecurityGroups']:
                used_SG.append(id['VpcSecurityGroupId'])

    print("****************************************************************************")
    print("Total Security Groups: ")
    print(total_SG)
    print("****************************************************************************")
    print("****************************************************************************")
    print("Used Security Groups: ")
    print(list(set(used_SG)))
    print("****************************************************************************")
    print("****************************************************************************")
    print("Unused Security Groups: ")
    print(list(set(total_SG) - set(used_SG)))
    print("****************************************************************************")
