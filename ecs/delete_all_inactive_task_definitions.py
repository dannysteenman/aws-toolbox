#  https://github.com/dannysteenman/aws-toolbox
#
#  License: MIT
#
# This script deletes all inactive task definitions in the ECS service in all AWS Regions.

import boto3


def get_inactive_task_definition_arns(region):
    client = boto3.client("ecs", region_name=region)
    response = client.list_task_definitions(status="INACTIVE")
    return response.get("taskDefinitionArns", [])


def delete_task_definition(region, arn):
    client = boto3.client("ecs", region_name=region)
    client.delete_task_definitions(taskDefinitions=[arn])


def delete_inactive_task_definitions_in_all_regions():
    ecs_regions = boto3.session.Session().get_available_regions("ecs")
    for region in ecs_regions:
        try:
            arns = get_inactive_task_definition_arns(region)
            if not arns:
                print(f"No inactive task definitions found in region {region}")
            else:
                for arn in arns:
                    print(f"Deleting inactive task definition with ARN: {arn}")
                    delete_task_definition(region, arn)
        except Exception:
            print(f"No access to region: {region}")
            continue


if __name__ == "__main__":
    delete_inactive_task_definitions_in_all_regions()
