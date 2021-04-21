#!/bin/bash

# this script enables you to run a request for spot instances. Configure the variables according to your specific need, as well as the launch.json file to specify the instance types etc. 

instanceDuration=60
instances=2
spotPrice="0.25"
region="us-east-1"
zone="us-east-1a"
launchFile="file://launch.json"

aws ec2 request-spot-instances --block-duration-minutes $instanceDuration --instance-count $instances --spot-price $spotPrice --region $region --launch-specification $launchFile