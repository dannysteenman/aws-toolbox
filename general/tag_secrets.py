#  https://github.com/dannysteenman/aws-toolbox
#
#  License: MIT
#
# This script allows you to tag all your secrets in AWS Secrets Manager quickly

import boto3
from botocore.exceptions import ClientError

secretsmanager = boto3.client("secretsmanager")
tags_dict = [{"Key": "copilot-environment", "Value": "prod"}]


def add_tags_to_secret(secret_name, tags_dict):
    try:
        return secretsmanager.tag_resource(SecretId=secret_name, Tags=tags_dict)
    except ClientError as e:
        raise Exception("boto3 client error in add_tags_to_secret: " + e.__str__())
    except Exception as e:
        raise Exception("Unexpected error in add_tags_to_secret: " + e.__str__())


def get_secrets():
    paginator = secretsmanager.get_paginator("list_secrets")
    response_iterator = paginator.paginate()

    return [
        secret["Name"]
        for response in response_iterator
        for secret in response["SecretList"]
    ]


def lambda_handler(event, context):
    for secret in get_secrets():
        print(add_tags_to_secret(secret, tags_dict))


if __name__ == "__main__":
    lambda_handler({"invokingEvent": '{"messageType":"ScheduledNotification"}'}, None)
