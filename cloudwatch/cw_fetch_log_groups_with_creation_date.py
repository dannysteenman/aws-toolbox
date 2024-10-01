"""
Description: This script fetches all CloudWatch log groups in an AWS account,
             calculates their age, and displays the information in a tabulated format.
             It uses the AWS SDK for Python (Boto3) to interact with CloudWatch Logs
             and implements pagination to handle potentially large numbers of log groups.
Author: Danny Steenman
License: MIT
"""

from datetime import datetime

import boto3
from tabulate import tabulate


def fetch_log_groups_with_creation_dates():
    """
    Fetches all CloudWatch log groups and their creation dates.

    Returns:
        list: A list of tuples containing log group name, creation date, and age in days.
    """
    # Create a CloudWatch Logs client
    client = boto3.client("logs")

    # List to store log group names, creation dates, and age
    log_groups_info = []

    # Use paginator to handle potential large number of log groups
    paginator = client.get_paginator("describe_log_groups")
    for page in paginator.paginate():
        for log_group in page["logGroups"]:
            # Extract log group name and creation time
            log_group_name = log_group["logGroupName"]
            creation_time_millis = log_group.get("creationTime", 0)
            creation_date = datetime.fromtimestamp(creation_time_millis / 1000)

            # Calculate the age of the log group
            age_delta = datetime.now() - creation_date
            age_human_readable = f"{age_delta.days} days" if age_delta.days > 0 else "less than a day"

            # Append the extracted information to the list
            log_groups_info.append((log_group_name, creation_date, age_delta.days))

    # Sort by age in descending order (most days to least days)
    log_groups_info.sort(key=lambda x: x[2], reverse=True)

    return log_groups_info


def main():
    """
    Main function to execute the log group fetching process and display results.
    """
    log_groups_info = fetch_log_groups_with_creation_dates()

    # Prepare data for tabulate
    table_data = [
        (log_group_name, creation_date, f"{age_days} days" if age_days > 0 else "less than a day")
        for log_group_name, creation_date, age_days in log_groups_info
    ]

    # Print table
    headers = ["Log Group", "Created On", "Age"]
    print(tabulate(table_data, headers=headers, tablefmt="pretty"))


if __name__ == "__main__":
    main()
