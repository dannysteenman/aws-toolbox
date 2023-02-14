import sys
import boto3

# Get the target bucket name from the command line argument
if len(sys.argv) < 2:
    print("Please provide the target bucket name as a command line argument")
    sys.exit(1)

target_bucket_name = sys.argv[1]

# Create an S3 client
s3 = boto3.client('s3')

# Get a list of all S3 buckets
response = s3.list_buckets()

# Iterate over the buckets
for bucket in response['Buckets']:
    # Check if the bucket name contains the target string
    if target_bucket_name in bucket['Name']:
        print(f"Found bucket: {bucket['Name']}")

        # Get a list of all object versions in the bucket
        versions = s3.list_object_versions(Bucket=bucket['Name'])

        # Delete all object versions in the bucket
        if 'Versions' in versions:
            for version in versions['Versions']:
                s3.delete_object(Bucket=bucket['Name'], Key=version['Key'], VersionId=version['VersionId'])

        # Delete all delete markers in the bucket
        if 'DeleteMarkers' in versions:
            for delete_marker in versions['DeleteMarkers']:
                s3.delete_object(Bucket=bucket['Name'], Key=delete_marker['Key'], VersionId=delete_marker['VersionId'])

        # Get a list of all objects in the bucket
        objects = s3.list_objects_v2(Bucket=bucket['Name'])

        # Delete all objects in the bucket
        if 'Contents' in objects:
            for obj in objects['Contents']:
                s3.delete_object(Bucket=bucket['Name'], Key=obj['Key'])

        # Finally, delete the bucket
        s3.delete_bucket(Bucket=bucket['Name'])
        print(f"Deleted bucket: {bucket['Name']}")
