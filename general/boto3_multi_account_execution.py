#  https://github.com/dannysteenman/aws-toolbox
#
#  License: MIT
#
# This script gives you the ability to run Boto3 commands on all accounts which are specified in the aws_account_list

import boto3

aws_account_list = ["111111111111", "222222222222", "333333333333"]


def role_arn_to_session(**args):
    client = boto3.client("sts")
    response = client.assume_role(**args)
    return boto3.Session(
        aws_access_key_id=response["Credentials"]["AccessKeyId"],
        aws_secret_access_key=response["Credentials"]["SecretAccessKey"],
        aws_session_token=response["Credentials"]["SessionToken"],
    )


# This decides what role to use, a name of the session you will start, and potentially an external id.
# The external id can be used as a passcode to protect your role.
def set_boto3_clients(account_id):
    return role_arn_to_session(
        RoleArn="arn:aws:iam::" + account_id + ":role/your-rolename-to-assume",
        RoleSessionName="your-rolename-to-assume",
    )


# This is an example function which deletes evaluation results for a specific config rule.
# You can create your own Boto3 function which you want to execute on mutliple accounts.
def delete_awsconfig_rule_evaluations(awsconfig):
    return awsconfig.delete_evaluation_results(ConfigRuleName="SHIELD_002")


def lambda_handler(event, context):
    for account_id in aws_account_list:
        run_boto3_in_account = set_boto3_clients(account_id)
        # You can use run_boto3_in_account as if you are using boto in another account
        # For example: s3 = run_boto3_in_account.client('s3')
        awsconfig = run_boto3_in_account.client("config")
        delete_awsconfig_rule_evaluations(awsconfig)


if __name__ == "__main__":
    lambda_handler({"invokingEvent": '{"messageType":"ScheduledNotification"}'}, None)
