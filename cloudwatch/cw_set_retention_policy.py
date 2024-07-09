#  https://github.com/dannysteenman/aws-toolbox
#
#  License: MIT
#
# This script sets CloudWatch Logs Retention Policy for log groups in the configured AWS region.
# It can set a specific retention period for all log groups or print a summary of current retention periods.
#
# Features:
# - Set retention from 1 day to 10 years
# - Print retention count summary
# - Detailed logging and verification of updates
#
# Usage:
# 1. Set retention: python script_name.py --retention <days>
# 2. Print retention counts: python script_name.py --print-retention-counts


import argparse
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

import boto3
import botocore

cloudwatch = boto3.client("logs")


def get_cloudwatch_log_groups():
    kwargs = {"limit": 50}
    cloudwatch_log_groups = []

    while True:  # Paginate
        response = cloudwatch.describe_log_groups(**kwargs)
        cloudwatch_log_groups += [log_group for log_group in response["logGroups"]]
        if "nextToken" in response:
            kwargs["nextToken"] = response["nextToken"]
        else:
            break

    return cloudwatch_log_groups


def update_log_group_retention(group, retention):
    try:
        if "retentionInDays" not in group or group["retentionInDays"] != retention:
            cloudwatch.put_retention_policy(logGroupName=group["logGroupName"], retentionInDays=retention)

            # Verify the update
            updated_group = cloudwatch.describe_log_groups(logGroupNamePrefix=group["logGroupName"])["logGroups"][0]
            if updated_group.get("retentionInDays") == retention:
                return f"Successfully updated retention for: {group['logGroupName']}"
            else:
                return f"Failed to update retention for: {group['logGroupName']}. Current retention: {updated_group.get('retentionInDays')}"
        else:
            return (
                f"CloudWatch Loggroup: {group['logGroupName']} already has the specified retention of {retention} days."
            )
    except botocore.exceptions.ClientError as e:
        return f"Error updating {group['logGroupName']}: {e}"


def count_retention_periods(cloudwatch_log_groups):
    retention_counts = defaultdict(int)
    for group in cloudwatch_log_groups:
        retention = group.get("retentionInDays", "Not set")
        retention_counts[retention] += 1
    return retention_counts


def cloudwatch_set_retention(args):
    cloudwatch_log_groups = get_cloudwatch_log_groups()

    if args.print_retention_counts:
        retention_counts = count_retention_periods(cloudwatch_log_groups)
        print("Retention periods and log group counts:")

        # Separate 'Not set' from other retention periods
        not_set_count = retention_counts.pop("Not set", 0)

        # Sort the remaining items (all integers now)
        sorted_items = sorted(retention_counts.items(), key=lambda x: int(x[0]))

        # Print 'Not set' first if it exists
        if not_set_count:
            print(f"Retention: Not set, Count: {not_set_count}")

        # Print the rest of the sorted items
        for retention_period, count in sorted_items:
            print(f"Retention: {retention_period} days, Count: {count}")
        return

    retention = vars(args)["retention"]
    groups_to_update = [
        group
        for group in cloudwatch_log_groups
        if "retentionInDays" not in group or group["retentionInDays"] != retention
    ]

    if not groups_to_update:
        print(f"All log groups already have the specified retention of {retention} days.")
        return

    print(f"Log groups that need to be updated to {retention} days retention:")
    for group in groups_to_update:
        current_retention = group.get("retentionInDays", "Not set")
        print(f"  {group['logGroupName']} (current retention: {current_retention})")

    if input("\nDo you want to proceed with the update? (y/n): ").lower() != "y":
        print("Update cancelled.")
        return

    updated_count = 0
    failed_count = 0

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_group = {
            executor.submit(update_log_group_retention, group, retention): group for group in groups_to_update
        }
        for future in as_completed(future_to_group):
            result = future.result()
            print(result)
            if "Successfully updated" in result:
                updated_count += 1
            else:
                failed_count += 1

    print(f"\nAttempted to update {len(groups_to_update)} log groups.")
    print(f"Successfully updated: {updated_count}")
    print(f"Failed to update: {failed_count}")

    if failed_count > 0:
        print("\nSome updates failed. Please check the output above for details.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Set a retention in days for all your CloudWatch Logs in a single region."
    )
    parser.add_argument(
        "--retention",
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
    parser.add_argument(
        "--print-retention-counts", action="store_true", help="Print the number of log groups for each retention period"
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if args.print_retention_counts and args.retention is not None:
        parser.error("--print-retention-counts cannot be used with --retention argument")

    cloudwatch_set_retention(args)
