"""
Description: This script counts the total number of CloudWatch log groups in an AWS account.
             It uses the AWS SDK for Python (Boto3) to interact with CloudWatch Logs and
             implements pagination to handle potentially large numbers of log groups.
Author: Danny Steenman
License: MIT
"""

import boto3


def count_log_groups():
    """
    Counts the total number of CloudWatch log groups in the AWS account.

    Returns:
        int: The total number of CloudWatch log groups.
    """
    # Create a CloudWatch Logs client
    client = boto3.client("logs")

    # Initialize log group count
    log_group_count = 0

    # Use paginator to handle potential large number of log groups
    paginator = client.get_paginator("describe_log_groups")
    for page in paginator.paginate():
        log_group_count += len(page["logGroups"])

    return log_group_count


def main():
    """
    Main function to execute the log group counting process.
    """
    log_group_count = count_log_groups()
    print(f"Total number of CloudWatch log groups: {log_group_count}")


if __name__ == "__main__":
    main()
