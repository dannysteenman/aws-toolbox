"""
# https://github.com/dannysteenman/aws-toolbox
#
# License: MIT
#
# This script creates Route 53 health checks for multiple domains in all AWS Regions
"""

import sys
import time
import boto3
from botocore.exceptions import ClientError

def create_health_check(domain):
    """Create a health check for the given domain and add a tag."""
    client = boto3.client('route53')

    try:
        # Create health check
        response = client.create_health_check(
            CallerReference=f"{domain}-{int(time.time())}",
            HealthCheckConfig={
                'FullyQualifiedDomainName': domain,
                'Port': 443,
                'Type': 'HTTPS',
                'ResourcePath': '/',
                'RequestInterval': 30,
                'FailureThreshold': 3,
                'MeasureLatency': False,
                'Inverted': False,
                'Disabled': False,
                'EnableSNI': True,
                'Regions': [
                    'us-east-1',
                    'us-west-1',
                    'us-west-2',
                    'ap-northeast-1',
                    'ap-southeast-1',
                    'ap-southeast-2',
                    'eu-west-1',
                    'sa-east-1'
                ]
            }
        )

        health_check_id = response['HealthCheck']['Id']
        print(f"Health check created for {domain} with ID: {health_check_id}")

        # Add tag to the health check
        client.change_tags_for_resource(
            ResourceType='healthcheck',
            ResourceId=health_check_id,
            AddTags=[
                {
                    'Key': 'Name',
                    'Value': f"{domain} Health Check"
                },
            ]
        )
        print(f"Tag added to health check for {domain}")

    except ClientError as e:
        print(f"Error creating health check for {domain}: {e}")

def main():
    if len(sys.argv) < 2:
        print("Please provide one or more domain names separated by spaces.")
        print("Usage: python script.py domain1.com domain2.com domain3.com")
        sys.exit(1)

    domains = sys.argv[1:]

    for domain in domains:
        create_health_check(domain)

    print("All health checks created successfully.")

if __name__ == "__main__":
    main()
