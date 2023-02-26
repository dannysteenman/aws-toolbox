#  https://github.com/dannysteenman/aws-toolbox
#
#  License: MIT
#
# This script will set a CloudWatch Logs Retention Policy to x number of days for all log groups in the region that you exported in your cli.

import argparse
import boto3

cloudwatch = boto3.client("logs")


def get_cloudwatch_log_groups():
    kwargs = {"limit": 50}
    cloudwatch_log_groups = []

    while True:  # Paginate
        response = cloudwatch.describe_log_groups(**kwargs)

        cloudwatch_log_groups += [log_group for log_group in response["logGroups"]]

        if "NextToken" in response:
            kwargs["NextToken"] = response["NextToken"]
        else:
            break

    return cloudwatch_log_groups


def cloudwatch_set_retention(args):
    retention = vars(args)["retention"]
    cloudwatch_log_groups = get_cloudwatch_log_groups()

    for group in cloudwatch_log_groups:
        print(group)
        if "retentionInDays" not in group or group["retentionInDays"] != retention:
            print(f"Retention needs to be updated for: {group['logGroupName']}")
            cloudwatch.put_retention_policy(
                logGroupName=group["logGroupName"], retentionInDays=retention
            )
        else:
            print(
                f"CloudWatch Loggroup: {group['logGroupName']} already has the specified retention of {group['retentionInDays']} days."
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Set a retention in days for all your CloudWatch Logs in a single region."
    )
    parser.add_argument(
        "retention",
        metavar="RETENTION",
        type=int,
        choices=[
            1,
            3,
            5,
            7,
            14,
            30,
            60,
            90,
            120,
            150,
            180,
            365,
            400,
            545,
            731,
            1827,
            3653,
        ],
        help="Enter the retention in days for the CloudWatch Logs.",
    )
    args = parser.parse_args()
    cloudwatch_set_retention(args)
