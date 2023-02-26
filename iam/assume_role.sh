#!/bin/zsh
# This script uses Simple Token Service (sts) to assume a role (on the destination account)
# Then it creates a temporary AWS credential that is stored in the client profile.
# This script is perfect for AWS Codebuild commands than need crossaccount access.
#
# Usage: ./assume_role.sh arn:aws:iam::012345678910:role/role-on-destination-that-needs-to-be-assumed profile-name-to-create
# aws s3 ls --profile client-profile --region eu-central-1

ROLE_ARN=$1
OUTPUT_PROFILE=$2

echo "Assuming role $ROLE_ARN"
sts=$(aws sts assume-role \
    --role-arn "$ROLE_ARN" \
    --role-session-name "$OUTPUT_PROFILE" \
    --query 'Credentials.[AccessKeyId,SecretAccessKey,SessionToken]' \
    --output text)
echo "Converting sts to array"
sts=($sts)
aws configure set aws_access_key_id ${sts[0]} --profile $OUTPUT_PROFILE
aws configure set aws_secret_access_key ${sts[1]} --profile $OUTPUT_PROFILE
aws configure set aws_session_token ${sts[2]} --profile $OUTPUT_PROFILE
echo "AWS Credentials are stored in the profile named $OUTPUT_PROFILE"
echo "You can now use the new temporary profile to run aws cli commands e.g. 'aws s3 ls --profile $OUTPUT_PROFILE --region eu-central-1'"
