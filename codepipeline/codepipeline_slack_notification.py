#  https://github.com/dannysteenman/aws-toolbox
#
# This script can be used in a lambda to enable AWS CodePipeline notifications on slack in a specific channel.


import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

import boto3

client = boto3.client("codepipeline")

ACCOUNT_DESC = os.getenv("ACCOUNT_DESC", None)
SLACK_URL = os.getenv("SLACK_URL", None)
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", None)
ALWAYS_SHOW_SUCCEEDED = os.getenv("ALWAYS_SHOW_SUCCEEDED", "false") == "true"


def get_previous_pipeline_execution(pipeline_name, execution_id):
    # Retrieves executions based on their start timestamp, so
    # the previous execution will be next in list.
    pipeline_executions = client.list_pipeline_executions(
        pipelineName=pipeline_name,
    )["pipelineExecutionSummaries"]

    is_next = False

    for item in pipeline_executions:
        # Only include succeeded and failed executions.
        # This is needed to properly detect a recovered
        # pipeline (failed -> succeeded, even if e.g. superseeded in between).
        if is_next and item["status"] in ["Succeeded", "Failed"]:
            return item
        if item["pipelineExecutionId"] == execution_id:
            is_next = True

    return None


def get_blocks_for_failed(pipeline_name, execution_id, state):
    # We only show details if the pipeline has completed with failed state.
    # If we were to process this for other events such as started events,
    # we would include details from after the event took place.
    if state != "FAILED":
        return []

    action_executions = client.list_action_executions(
        pipelineName=pipeline_name,
        filter={
            "pipelineExecutionId": execution_id,
        },
    )["actionExecutionDetails"]

    result = []

    for action_execution in action_executions:
        if action_execution["status"] == "Failed":
            stage = action_execution["stageName"]
            action = action_execution["actionName"]
            summary = action_execution["output"]["executionResult"][
                "externalExecutionSummary"
            ]
            result.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"{stage}.{action} failed:\n```\n{summary}\n```",
                    },
                }
            )

    return result


def handler(event, context):
    print("Event: " + json.dumps(event))

    if event["detail-type"] != "CodePipeline Pipeline Execution State Change":
        print("Ignoring unknown event")
        return

    account = event["account"]
    region = event["region"]
    pipeline_name = event["detail"]["pipeline"]
    state = event["detail"]["state"]
    execution_id = event["detail"]["execution-id"]

    previous_pipeline_execution = get_previous_pipeline_execution(
        pipeline_name, execution_id
    )

    previous_failed = (
        previous_pipeline_execution is not None
        and previous_pipeline_execution["status"] == "Failed"
    )

    # We still show succeeded for the first event or when
    # the previous execution was not success.
    if (
        state == "SUCCEEDED"
        and not ALWAYS_SHOW_SUCCEEDED
        and previous_pipeline_execution is not None
        and not previous_failed
    ):
        print("Ignoring succeeded event")
        return

    emoji_prefix = ""
    if state == "FAILED":
        emoji_prefix = ":x: "
    elif state == "SUCCEEDED":
        emoji_prefix = ":white_check_mark: "

    pipeline_url = f"https://{region}.console.aws.amazon.com/codesuite/codepipeline/pipelines/{quote(pipeline_name, safe='')}/view"
    execution_url = f"https://{region}.console.aws.amazon.com/codesuite/codepipeline/pipelines/{quote(pipeline_name, safe='')}/executions/{execution_id}/timeline"

    state_text = state
    if previous_failed and state == "SUCCEEDED":
        state_text += " (previously failed)"

    blocks_for_failed = get_blocks_for_failed(pipeline_name, execution_id, state)

    account_text = account
    if ACCOUNT_DESC is not None:
        account_text += f" ({ACCOUNT_DESC})"

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"{emoji_prefix}Pipeline <{pipeline_url}|{pipeline_name}> *{state_text}*\n{region} | {account_text}\n<{execution_url}|Execution details>",
            },
        },
        *blocks_for_failed,
    ]

    slack_message = {
        "channel": SLACK_CHANNEL,
        "blocks": blocks,
        "username": "Pipeline Status",
        "icon_emoji": ":traffic_light:",
    }

    req = Request(SLACK_URL, json.dumps(slack_message).encode("utf-8"))
    try:
        response = urlopen(req)
        response.read()
        print(f"Message posted to: {slack_message['channel']}")
    except HTTPError as e:
        raise Exception(f"Request to slack failed: {e.code} {e.reason}")
    except URLError as e:
        raise Exception(f"Server connection to slack failed: {e.reason}")


# Mock test event for the codepipeline slack notification
# if __name__ == "__main__":
#     handler(
#         {
#             "version": "0",
#             "id": "01896665-9ef2-b417-cccd-333otr6a9311",
#             "detail-type": "CodePipeline Pipeline Execution State Change",
#             "source": "aws.codepipeline",
#             "account": "012345678912",
#             "time": "2021-06-11T23:02:20Z",
#             "region": "eu-west-1",
#             "resources": [
#                 "arn:aws:codepipeline:eu-west-1:012345678912:PipelineStack-CdkPipelineB1A1BEA2-PH8AW5FURN8T"
#             ],
#             "detail": {
#                 "pipeline": "PipelineStack-CdkPipelineB1A1BEA2-PH8AW5FURN8T",
#                 "execution-id": "91daefbf-658a-4c6f-ad9e-13de7df5eaeb",
#                 "state": "SUCCEEDED",
#                 "version": 3,
#             },
#         },
#         None,
#     )
