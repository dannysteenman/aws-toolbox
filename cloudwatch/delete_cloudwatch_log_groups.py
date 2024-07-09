#  https://github.com/dannysteenman/aws-toolbox
#
#  License: MIT
#
# This script deletes CloudWatch log groups based on their age. It can optionally keep log groups
# newer than a specified time period (e.g., days, weeks, or months). The script supports a dry run
# mode to preview deletions without making changes. It operates on all log groups in the AWS region
# configured in your CLI.

import argparse
from datetime import datetime, timedelta

import boto3
from botocore.exceptions import ClientError


def parse_time_period(value):
    try:
        num, unit = value.split()
        num = int(num)
        if unit not in ["days", "weeks", "months"]:
            raise ValueError
        return num, unit
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Time period must be in format: '<number> <unit>' where unit is 'days', 'weeks', or 'months'"
        )


def get_cloudwatch_log_groups(client):
    log_groups = []
    paginator = client.get_paginator("describe_log_groups")
    for page in paginator.paginate():
        log_groups.extend(page["logGroups"])
    return log_groups


def process_log_groups(client, retention_period=None, dry_run=False):
    log_groups = get_cloudwatch_log_groups(client)
    now = datetime.now()
    total_groups = len(log_groups)
    kept_groups = []
    to_delete_groups = []
    failed_deletions = []

    if retention_period:
        num, unit = retention_period
        if unit == "days":
            threshold = timedelta(days=num)
        elif unit == "weeks":
            threshold = timedelta(weeks=num)
        else:  # months
            threshold = timedelta(days=num * 30)  # Approximate

    for group in log_groups:
        last_event = group.get("creationTime", 0) / 1000  # Convert to seconds
        last_event_date = datetime.fromtimestamp(last_event)
        age = now - last_event_date

        if retention_period and age <= threshold:
            kept_groups.append((group["logGroupName"], age))
        else:
            to_delete_groups.append((group["logGroupName"], age))

    # Print kept groups
    print("Log groups to keep:")
    for name, age in kept_groups:
        print(f"{'[DRY RUN] ' if dry_run else ''}Keeping log group: {name} (Age: {age})")

    # Print groups to delete
    print("\nLog groups to delete:")
    for name, age in to_delete_groups:
        print(f"{'[DRY RUN] Would delete' if dry_run else 'Deleting'} log group: {name} (Age: {age})")

    print("\nSummary:")
    print(f"Total log groups: {total_groups}")
    print(f"Log groups kept: {len(kept_groups)}")
    print(f"Log groups to be deleted: {len(to_delete_groups)}")

    if not dry_run:
        for name, _ in to_delete_groups:
            try:
                client.delete_log_group(logGroupName=name)
            except ClientError as e:
                if e.response["Error"]["Code"] == "AccessDeniedException":
                    print(f"Access denied when trying to delete log group: {name}")
                    failed_deletions.append(name)
                else:
                    raise  # Re-raise the exception if it's not an AccessDeniedException

        print(f"Log groups actually deleted: {len(to_delete_groups) - len(failed_deletions)}")
        if failed_deletions:
            print(f"Failed to delete {len(failed_deletions)} log groups due to access denial:")
            for name in failed_deletions:
                print(f"  - {name}")


def main():
    parser = argparse.ArgumentParser(description="Delete CloudWatch log groups based on retention.")
    parser.add_argument(
        "--keep",
        type=parse_time_period,
        help="Keep log groups newer than this period (e.g., '5 days', '2 weeks', '1 months')",
    )
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without actually deleting log groups")
    args = parser.parse_args()

    client = boto3.client("logs")
    process_log_groups(client, args.keep, args.dry_run)


if __name__ == "__main__":
    main()
