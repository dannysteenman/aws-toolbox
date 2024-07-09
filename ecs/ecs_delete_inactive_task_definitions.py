#  https://github.com/dannysteenman/aws-toolbox
#
#  License: MIT
#
# This script deletes all inactive task definitions in the ECS service in all AWS Regions.

import boto3
import sys
import time  # Import time module for sleep


def get_inactive_task_definition_arns(region):
    client = boto3.client("ecs", region_name=region)
    arns = []
    paginator = client.get_paginator("list_task_definitions")
    for page in paginator.paginate(status="INACTIVE"):
        arns.extend(page.get("taskDefinitionArns", []))
    return arns


def delete_task_definition(region, arn):
    client = boto3.client("ecs", region_name=region)
    max_retries = 5
    backoff = 1  # Initial backoff time in seconds
    for attempt in range(1, max_retries + 1):
        try:
            client.delete_task_definitions(taskDefinitions=[arn])
            print(f"Deleted task definition {arn}")
            break  # Break the loop if deletion was successful
        except client.exceptions.ClientException as e:
            if "Throttling" in str(e):  # Check for throttling in the error message
                print(f"Throttling exception when deleting {arn}: {e}, retrying in {backoff} seconds...")
                time.sleep(backoff)
                backoff *= 2  # Exponential backoff
            else:
                print(f"Client exception when deleting task definition {arn}: {e}")
                break  # Break the loop for other client exceptions
        except client.exceptions.ServerException as e:
            if "Throttling" in str(e):  # Check for throttling in the error message
                print(f"Throttling exception when deleting {arn}: {e}, retrying in {backoff} seconds...")
                time.sleep(backoff)
                backoff *= 2  # Exponential backoff
            else:
                print(f"Server exception when deleting task definition {arn}: {e}")
                break  # Break the loop for other server exceptions
        except Exception as e:
            print(f"Unexpected error deleting task definition {arn}: {e}")
            break  # Break the loop for any other unexpected errors


def delete_inactive_task_definitions_in_region(region):
    try:
        arns = get_inactive_task_definition_arns(region)
        if not arns:
            print(f"No inactive task definitions found in region {region}")
        else:
            for arn in arns:
                delete_task_definition(region, arn)
    except Exception as e:
        print(f"Error accessing region {region}: {e}")


def delete_inactive_task_definitions_in_all_regions():
    ecs_regions = boto3.session.Session().get_available_regions("ecs")
    for region in ecs_regions:
        delete_inactive_task_definitions_in_region(region)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Usage: python script.py [region]")
        sys.exit(1)
    elif len(sys.argv) == 2:
        region = sys.argv[1]
        delete_inactive_task_definitions_in_region(region)
    else:
        delete_inactive_task_definitions_in_all_regions()
