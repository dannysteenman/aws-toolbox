#!/bin/zsh
# This script shows Elastic IP addresses which haven't been associated yet.

not_assigned_ip=$(aws ec2 describe-addresses --query 'Addresses[?AssociationId==`null`].PublicIp' --output text)

echo $not_assigned_ip
