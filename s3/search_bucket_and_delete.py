#  https://github.com/dannysteenman/aws-toolbox
#
#  License: MIT
#
# This script searches for your chosen bucketname and then deletes all (versioned)objects in that S3 bucket before deleting the bucket itself.
#
# Usage: python s3_search_bucket_and_delete.py <insert-bucket-name>

import sys
import boto3

# Get the target bucket name from the command line argument
if len(sys.argv) < 2:
    print("Please provide the target bucket name as a command line argument")
    sys.exit(1)

target_bucket_name = sys.argv[1]

# Create an S3 client
s3_client = boto3.client("s3")
# create an S3 resource
s3 = boto3.resource("s3")

# Get a list of all S3 buckets
response = s3_client.list_buckets()

# Iterate over the buckets
for bucket in response["Buckets"]:
    bucket_name = bucket["Name"]
    # Check if the bucket name contains the target string
    if target_bucket_name in bucket_name:
        print(f"Found bucket: {bucket_name}")

        versioning = s3_client.get_bucket_versioning(Bucket=bucket_name)
        bucket = s3.Bucket(bucket_name)

        if versioning.get("Status") == "Enabled":
            bucket.object_versions.delete()
        else:
            bucket.objects.delete()

        # Finally, delete the bucket
        s3_client.delete_bucket(Bucket=bucket_name)
        print(f"Deleted bucket: {bucket_name}")
