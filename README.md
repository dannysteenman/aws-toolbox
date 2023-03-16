![AWS Toolbox](aws-toolbox-header.jpg)

# AWS Toolbox 🧰

A Collection of Awesome Tools and Scripts for Cloud Engineers.

## Table of Contents

- [AWS Toolbox 🧰](#aws-toolbox-)
  - [Table of Contents](#table-of-contents)
  - [Getting started](#getting-started)
  - [Shell \& Python scripts categorized by AWS Service](#shell--python-scripts-categorized-by-aws-service)
    - [General scripts](#general-scripts)
    - [CloudFormation scripts](#cloudformation-scripts)
    - [CloudWatch scripts](#cloudwatch-scripts)
    - [CodePipeline](#codepipeline)
    - [EC2 scripts](#ec2-scripts)
    - [ECS scripts](#ecs-scripts)
    - [IAM scripts](#iam-scripts)
    - [Organizations scripts](#organizations-scripts)
    - [S3 scripts](#s3-scripts)
    - [SSM scripts](#ssm-scripts)
  - [Tools](#tools)
    - [General](#general)
    - [CI/CD](#cicd)
    - [EC2](#ec2)
    - [ECS](#ecs)
    - [IAM](#iam)
    - [Infra as Code](#infra-as-code)
    - [Lambda](#lambda)
    - [S3](#s3)
    - [Security](#security)
    - [SSM](#ssm)
  - [Contributors](#contributors)
  - [Author](#author)
  - [Support my work](#support-my-work)

## Getting started

- [What is the AWS Command Line Interface?](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)
- [How to install the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- [Configure the AWS CLI for usage](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
- [Some examples on how to use the AWS CLI to work with AWS Services](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-services.html)

## Shell & Python scripts categorized by AWS Service

### General scripts

- **[delete_unused_security_groups.py](general/delete_unused_security_groups.py)** - Deletes all unused security groups in a single AWS Region
- **[find_unused_security_groups.py](general/find_unused_security_groups.py)** - Finds all unused security groups in a single AWS Region
- **[alias](cli/alias)** - This file contains a bunch of easy to remember aliases that runs complex AWS CLI commands.
- **[tag_secrets.py](general/tag_secrets.py)** - This script allows you to tag all your secrets in AWS Secrets Manager quickly.
- **[multi_account_execution.py](general/multi_account_execution.py)** - Gives you the ability to run Boto3 commands on all accounts which are specified in the aws_account_list.

### CloudFormation scripts

- **[delete_stackset.py](cloudformation/delete_stackset.py)** - Deletes all stack instances associated with a stackset and the stackset itself

### CloudWatch scripts
- **[set_cloudwatch_logs_retention.py](cloudwatch/set_cloudwatch_logs_retention.py)** - Sets a CloudWatch Logs Retention Policy to x number of days for all log groups in the region that you exported in your cli.

### CodePipeline
- **[slack_notification.py](codepipeline/slack_notification.py)** - Can be used in a lambda to enable AWS CodePipeline notifications on slack in a specific channel.

### EC2 scripts

- **[delete_all_unattached_volumes.py](ec2/delete_all_unattached_volumes.py)** - Deletes all unattached EBS volumes in all AWS Regions
- **[delete_all_unused_elastic_ips.py](ec2/delete_all_unused_elastic_ips.py)** - Finds and deletes all unused Elastic IPs in all AWS Regions
- **[delete_all_unused_keypairs.py](ec2/delete_all_unused_keypairs.py)** - Deletes all unused EC2 keypairs in all AWS Region
- **[delete_unused_keypairs.py](ec2/delete_unused_keypairs.py)** - Finds and deletes all unused EC2 keypairs in a single AWS Region
- **[find_all_unattached_volumes.py](ec2/find_all_unattached_volumes.py)** - Finds all unattached EBS volumes in all AWS Regions
- **[find_all_unused_keypairs.py](ec2/find_all_unused_keypairs.py)** - Finds all used and unused EC2 keypairs in all AWS Regions
- **[find_unused_keypairs.py](ec2/find_unused_keypairs.py)** - Finds all used and unused EC2 keypairs in a single region
- **[asg_ssh.sh](ec2/asg_ssh.sh)** - A ssh wrapper for connecting quickly to EC2 instances in an Auto Scaling group.
- **[available_eip.sh](ec2/available_eip.sh)** - Shows Elastic IP addresses which haven't been associated yet.
- **[req_spot_instances.sh](ec2/req_spot_instances.sh)** - Enables you to run a request for spot instances.
- **[resize_volume.sh](ec2/resize_volume.sh)** - specifies the desired volume size in GiB as a command line argument. If not specified, default to 20 GiB.

### ECS scripts
- **[delete_all_inactive_task_definitions.py](ecs/delete_all_inactive_task_definitions.py)** - Deletes all inactive task definitions in the ECS service in all AWS Regions.
- **[publish_ecr_image.sh](ecs/publish_ecr_image.sh)** - Build a Docker image and publish it to Amazon ECR.

### IAM scripts

- **[delete_iam_user](iam/delete_iam_user.py)** - This script deletes iam users.
- **[key_rotator](iam/key_rotator.py)** - This script rotates IAM user keys.
- **[assume_role.sh](iam/assume_role.sh)** - This script uses Simple Token Service (sts) to assume a role (on the destination account).

### Organizations scripts

- **[assign_sso_access_by_ou.py](organizations/assign_sso_access_by_ou.py)** - Assigns AWS Single Sign-On (SSO) access to a specified principal (user or group) for multiple AWS accounts within a specified Organizational Unit (OU).
- **[list_accounts_by_ou.py](organizations/list_accounts_by_ou.py)** - Returns a list of acounts that are part of an Organizational Unit (OU)
- **[list_accounts_sso_assignments.py](organizations/list_accounts_sso_assignments.py)** - The script lists all AWS accounts along with their assigned users, groups, and permission sets in a structured JSON format.
- **[remove_sso_access_by_ou.py](organizations/remove_sso_access_by_ou.py)** - Removes AWS Single Sign-On (SSO) access to a specified principal (user or group) for multiple AWS accounts within a specified Organizational Unit (OU).

### S3 scripts
- **[create_tar_file.py](s3/create_tar_file.py)** - Allows you to create tar file creation.
- **[delete_empty_buckets.py](s3/delete_empty_buckets.py)** - Finds empty S3 buckets on your account and deletes them.
- **[list_file_older_than_number_of_days.py](s3/list_file_older_than_number_of_days.py)** - Allows you to list all files older than N numbers of days.
- **[search_bucket_and_delete.py](s3/search_bucket_and_delete.py)** - Searches for your chosen bucketname and then deletes all (versioned)objects in that S3 bucket before deleting the bucket itself.
- **[search_file_in_bucket.py](s3/search_file_in_bucket.py)** - Allows you to search file in S3 bucket.
- **[search_subdirectory.py](s3/search_subdirectory.py)** - Allows you to search subdirectory under nested folder structure.

### SSM scripts
- **[parameter_delete.sh](ssm/parameter_delete.sh)** - Allows you to delete ssm parameters through a json file.
- **[parameter_register.sh](ssm/parameter_register.sh)** - Allows you to import ssm parameters through a json file.

## Tools

This list contains links to tools that automate or simplify the usage of AWS in the console, CLI or API's.

### General

- **[Steampipe](https://github.com/turbot/steampipe)** - Query AWS resources in a SQL like fashion.
- **[AWS Nuke](https://github.com/rebuy-de/aws-nuke)** - Remove all resources from an AWS account.

### CI/CD

- **[Awesome CI](https://github.com/ligurio/awesome-ci)** - List of Continuous Integration services.

### EC2

- **[AutoSpotting](https://github.com/AutoSpotting/AutoSpotting)** - AutoSpotting is the leading open source spot market automation tool, optimized towards quick/easy/frictionless adoption of the EC2 spot market at any scale.

### ECS

- **[Awesome ECS](https://github.com/nathanpeck/awesome-ecs)** - A curated list of awesome ECS guides, development tools, and resources.
- **[AWS Copilot CLI](https://github.com/aws/copilot-cli)** - The AWS Copilot CLI is a tool for developers to build, release and operate production ready containerized applications on Amazon ECS and AWS Fargate.
- **[ECS Compose-X](https://github.com/compose-x/ecs_composex)** - A python app/lib to use your existing docker-compose files, add CFN resources definitions (or via Discovery) that takes care of all the complexity (IAM, Security Groups, Secrets, Volumes etc.) and generates curated CFN templates to deploy to AWS.

### IAM

- **[IAM Floyd](https://github.com/udondan/iam-floyd)** - AWS IAM policy statement generator with fluent interface.
- **[IAM Zero](https://iamzero.dev)** - IAM Zero detects identity and access management issues and automatically suggests least-privilege policies.

### Infra as Code

- **[Awesome CDK](https://github.com/kolomied/awesome-cdk)** - Curated list of awesome AWS Cloud Development Kit (AWS CDK) open-source projects, guides, blogs and other resources.
- **[Awesome CloudFormation](https://github.com/aws-cloudformation/awesome-cloudformation)** - A curated list of resources and projects for working with AWS CloudFormation.
- **[Awesome Terraform](https://github.com/shuaibiyy/awesome-terraform)** - Curated list of resources on HashiCorp's Terraform.
- **[CDK Snippets](https://towardsthecloud.com/blog/autocomplete-aws-cdk-constructs-vscode)** - This extension adds L1 construct snippets from CDK into Visual Studio Code.
- **[CloudFormation Snippets](https://towardsthecloud.com/blog/autocomplete-cloudformation-resources-vscode)** - This extension adds snippets for all the AWS CloudFormation resources into Visual Studio Code.
- **[Former2](https://github.com/iann0036/former2)** - Generate CloudFormation / Terraform / Troposphere templates from your existing AWS resources.
- **[Open CDK Guide](https://github.com/kevinslin/open-cdk)** - This guide is an opinionated set of tips and best practices for working with the AWS Cloud Development Kit.

### Lambda

- **[AWS Lambda Power Tuning](https://github.com/alexcasalboni/aws-lambda-power-tuning)** - AWS Lambda Power Tuning is a state machine powered by AWS Step Functions that helps you optimize your Lambda functions for cost and/or performance in a data-driven way.
- **[Serverless Cost Calculator Comparison](http://serverlesscalc.com)** - Calculating the cost for AWS Lambda, Azure Functions, Google Cloud Functions. Providing good comparison or prediction on how the cost can vary depending on the memory, execution time, and number of executions on different cloud providers.
- **[Serverless Cost Calculator](https://cost-calculator.bref.sh)** - Estimate AWS costs when running serverless applications on AWS Lambda.

### S3

- **[s3s3mirror](https://github.com/cobbzilla/s3s3mirror)** - A lightning-fast and highly concurrent utility for mirroring content from one S3 bucket to another.

### Security

- **[Leapp](https://github.com/Noovolari/leapp)** - Cross-platform APP to manage Programmatic access in AWS.
- **[Prowler](https://github.com/prowler-cloud/prowler)** - Prowler is an Open Source Security tool to perform Cloud Security best practices assessments, audits, incident response, continuous monitoring, hardening and forensics readiness.
- **[AWS Security Tools](https://github.com/0xVariable/AWS-Security-Tools)** - A curated list of Security tools that you can use on AWS.

### SSM

- **[aws-gate](https://github.com/xen0l/aws-gate)** - A Better AWS SSM Session manager CLI client.
- **[aws-ssm-ec2-proxy-command](https://github.com/qoomon/aws-ssm-ec2-proxy-command)** - Open an SSH connection to your ec2 instances via AWS SSM without the need to open any ssh port in you security groups.

---

## Contributors

This project exists thanks to all the people who contribute.

[![Code Contributors](https://contrib.rocks/image?repo=dannysteenman/aws-toolbox)](https://github.com/dannysteenman/aws-toolbox/graphs/contributors)

See how you can [contribute to this repository.](https://github.com/dannysteenman/aws-toolbox/blob/main/.github/CONTRIBUTING.md)

## Author

**[Danny Steenman](https://towardsthecloud.com)**

<p align="left">
  <a href="https://twitter.com/dannysteenman"><img src="https://img.shields.io/twitter/follow/dannysteenman?label=%40dannysteenman&style=social"></a>
</p>

---

## Support my work

If you found this project helpful, please consider showing your support by buying me a coffee.

<a href="https://www.buymeacoffee.com/dannysteenman" target="_blank"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=dannysteenman&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff"></a>