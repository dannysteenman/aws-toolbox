# [![AWS Toolbox header](https://raw.githubusercontent.com/dannysteenman/aws-toolbox/main/icons/github-header-image.png)](https://towardsthecloud.com)

# AWS Toolbox 🧰

This repository contains a collection of awesome tools and scripts for Developers and Engineers seeking to automate routine tasks on AWS Cloud.

> [!TIP]
> Struggling with AWS complexity or stuck on-premise? Let's transform your cloud journey.
>
> [Schedule a call with me](https://towardsthecloud.com/contact) to find out how I can enhance your existing AWS setup or guide your journey from on-premise to the Cloud.
>
> <details><summary>☁️ <strong>Discover more about my one-person business: Towards the Cloud</strong></summary>
>
> <br/>
>
> Hi, I'm Danny – AWS expert and founder of [Towards the Cloud](https://towardsthecloud.com). With over a decade of hands-on experience, I specialized myself in deploying well-architected, highly scalable and cost-effective AWS Solutions using Infrastructure as Code (IaC).
>
> #### When you work with me, you're getting a package deal of expertise and personalized service:
>
> - **AWS CDK Proficiency**: I bring deep AWS CDK knowledge to the table, ensuring your infrastructure is not just maintainable and scalable, but also fully automated.
> - **AWS Certified**: [Equipped with 7 AWS Certifications](https://www.credly.com/users/dannysteenman/badges), including DevOps Engineer & Solutions Architect Professional, to ensure best practices across diverse cloud scenarios.
> - **Direct Access**: You work with me, not a team of managers. Expect quick decisions and high-quality work.
> - **Tailored Solutions**: Understanding that no two businesses are alike, I Custom-fit cloud infrastructure for your unique needs.
> - **Cost-Effective**: I'll optimize your AWS spending without cutting corners on performance or security.
> - **Seamless CI/CD**: I'll set up smooth CI/CD processes using GitHub Actions, making changes a breeze through Pull Requests.
>
> *My mission is simple: I'll free you from infrastructure headaches so you can focus on what truly matters – your core business.*
>
> Ready to unlock the full potential of AWS Cloud?
>
> <a href="https://towardsthecloud.com/contact"><img alt="Schedule your call" src="https://img.shields.io/badge/schedule%20your%20call-success.svg?style=for-the-badge"/></a>
> </details>

## Python and Bash Scripts, Sorted by AWS Service

### CloudFormation scripts
- **[delete_stackset.py](cloudformation/delete_stackset.py)** - Deletes all stack instances associated with a stackset and the stackset itself

### CloudWatch scripts
- **[set_cloudwatch_logs_retention.py](cloudwatch/set_cloudwatch_logs_retention.py)** - Sets a CloudWatch Logs Retention Policy to x number of days for all log groups in the region that you exported in your cli.

### CodePipeline scripts
- **[slack_notification.py](codepipeline/slack_notification.py)** - Can be used in a lambda to enable AWS CodePipeline notifications on slack in a specific channel.

### EC2 scripts
- **[delete_all_unattached_volumes.py](ec2/delete_all_unattached_volumes.py)** - Deletes all unattached EBS volumes in all AWS Regions
- **[delete_all_unused_elastic_ips.py](ec2/delete_all_unused_elastic_ips.py)** - Finds and deletes all unused Elastic IPs in all AWS Regions
- **[delete_all_unused_keypairs.py](ec2/delete_all_unused_keypairs.py)** - Deletes all unused EC2 keypairs in all AWS Region
- **[delete_unused_keypairs.py](ec2/delete_unused_keypairs.py)** - Finds and deletes all unused EC2 keypairs in a single AWS Region
- **[delete_tagged_security_groups.py](ec2/delete_tagged_security_groups.py)** - Finds and deletes all tagged security groups including in- and outbound rules
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

### EFS scripts
- **[delete_tagged_efs.py](efs/delete_tagged_efs.py)** - Finds and deletes all tagged elastic file systems including mount targets

### IAM scripts
- **[delete_iam_user](iam/delete_iam_user.py)** - This script deletes iam users.
- **[key_rotator](iam/key_rotator.py)** - This script rotates IAM user keys.
- **[assume_role.sh](iam/assume_role.sh)** - This script uses Simple Token Service (sts) to assume a role (on the destination account).

### Organizations & IAM Identity Center scripts
- **[assign_sso_access_by_ou.py](organizations/assign_sso_access_by_ou.py)** - Assigns AWS Single Sign-On (SSO) access to a specified principal (user or group) for multiple AWS accounts within a specified Organizational Unit (OU).
- **[import_users_to_aws_sso.py](organizations/import_users_to_aws_sso.py)** - Imports users and groups from a CSV file into AWS SSO and adding the users to their respective groups.
- **[list_accounts_by_ou.py](organizations/list_accounts_by_ou.py)** - Returns a list of acounts that are part of an Organizational Unit (OU)
- **[list_accounts_sso_assignments.py](organizations/list_accounts_sso_assignments.py)** - The script lists all AWS accounts along with their assigned users, groups, and permission sets in a structured JSON format.
- **[remove_sso_access_by_ou.py](organizations/remove_sso_access_by_ou.py)** - Removes AWS Single Sign-On (SSO) access to a specified principal (user or group) for multiple AWS accounts within a specified Organizational Unit (OU).

### S3 scripts
- **[create_tar_file.py](s3/create_tar_file.py)** - Allows you to create tar file creation.
- **[delete_empty_buckets.py](s3/delete_empty_buckets.py)** - Finds empty S3 buckets on your account and deletes them.
- **[list_file_older_than_number_of_days.py](s3/list_file_older_than_number_of_days.py)** - Allows you to list all files older than N numbers of days.
- **[search_bucket_and_delete.py](s3/search_bucket_and_delete.py)** - Searches for your chosen bucketname and then deletes all (versioned)objects in that S3 bucket before deleting the bucket itself.
- **[search_file_in_bucket.py](s3/search_file_in_bucket.py)** - Allows you to search file in S3 bucket.
- **[search_key_bucket.py](s3/search_key_bucket.py)** - Searches for a single keys/object in an S3 bucket and let's you know wether it exists or not.
- **[search_multiple_keys_bucket.py](s3/search_multiple_keys_bucket.py)** - Searches for multiple keys/objects in an S3 bucket and let's you know wether it exists or not.
- **[search_subdirectory.py](s3/search_subdirectory.py)** - Allows you to search subdirectory under nested folder structure.

### SSM scripts
- **[parameter_delete.sh](ssm/parameter_delete.sh)** - Allows you to delete ssm parameters through a json file.
- **[parameter_register.sh](ssm/parameter_register.sh)** - Allows you to import ssm parameters through a json file.

### Other scripts
- **[delete_unused_security_groups.py](general/delete_unused_security_groups.py)** - Deletes all unused security groups in a single AWS Region
- **[find_unused_security_groups.py](general/find_unused_security_groups.py)** - Finds all unused security groups in a single AWS Region
- **[alias](cli/alias)** - This file contains a bunch of easy to remember aliases that runs complex AWS CLI commands.
- **[tag_secrets.py](general/tag_secrets.py)** - This script allows you to tag all your secrets in AWS Secrets Manager quickly.
- **[multi_account_execution.py](general/multi_account_execution.py)** - Gives you the ability to run Boto3 commands on all accounts which are specified in the aws_account_list.

---

## Tools
This list contains links to tools that automate or simplify the usage of AWS in the console, CLI or API's.

### EC2 Tools
- **[AutoSpotting](https://github.com/AutoSpotting/AutoSpotting)** - AutoSpotting is the leading open source spot market automation tool, optimized towards quick/easy/frictionless adoption of the EC2 spot market at any scale.

### ECS Tools
- **[Awesome ECS](https://github.com/nathanpeck/awesome-ecs)** - A curated list of awesome ECS guides, development tools, and resources.
- **[AWS Copilot CLI](https://github.com/aws/copilot-cli)** - The AWS Copilot CLI is a tool for developers to build, release and operate production ready containerized applications on Amazon ECS and AWS Fargate.
- **[ECS Compose-X](https://github.com/compose-x/ecs_composex)** - A python app/lib to use your existing docker-compose files, add CFN resources definitions (or via Discovery) that takes care of all the complexity (IAM, Security Groups, Secrets, Volumes etc.) and generates curated CFN templates to deploy to AWS.

### IAM Tools
- **[AWS IAM Actions](https://www.awsiamactions.io)** - Website that contains every IAM action including a way to generate your own policy.
- **[IAM Floyd](https://github.com/udondan/iam-floyd)** - AWS IAM policy statement generator with fluent interface.
- **[IAM Zero](https://iamzero.dev)** - IAM Zero detects identity and access management issues and automatically suggests least-privilege policies.

### Infra as Code Tools
- **[Awesome CDK](https://github.com/kolomied/awesome-cdk)** - Curated list of awesome AWS Cloud Development Kit (AWS CDK) open-source projects, guides, blogs and other resources.
- **[AWS CDK Starterkit](https://github.com/dannysteenman/aws-cdk-starterkit)** - Create and deploy an AWS CDK app on your AWS account in less than 5 minutes using GitHub actions!
- **[Awesome CloudFormation](https://github.com/aws-cloudformation/awesome-cloudformation)** - A curated list of resources and projects for working with AWS CloudFormation.
- **[Awesome Terraform](https://github.com/shuaibiyy/awesome-terraform)** - Curated list of resources on HashiCorp's Terraform.
- **[CDK Snippets](https://towardsthecloud.com/blog/autocomplete-aws-cdk-constructs-vscode)** - This extension adds L1 construct snippets from CDK into Visual Studio Code.
- **[CloudFormation Snippets](https://towardsthecloud.com/blog/autocomplete-cloudformation-resources-vscode)** - This extension adds snippets for all the AWS CloudFormation resources into Visual Studio Code.
- **[Former2](https://github.com/iann0036/former2)** - Generate CloudFormation / Terraform / Troposphere templates from your existing AWS resources.
- **[Open CDK Guide](https://github.com/kevinslin/open-cdk)** - This guide is an opinionated set of tips and best practices for working with the AWS Cloud Development Kit.

### Lambda Tools
- **[AWS Lambda Power Tuning](https://github.com/alexcasalboni/aws-lambda-power-tuning)** - AWS Lambda Power Tuning is a state machine powered by AWS Step Functions that helps you optimize your Lambda functions for cost and/or performance in a data-driven way.
- **[Serverless Cost Calculator Comparison](http://serverlesscalc.com)** - Calculating the cost for AWS Lambda, Azure Functions, Google Cloud Functions. Providing good comparison or prediction on how the cost can vary depending on the memory, execution time, and number of executions on different cloud providers.
- **[Serverless Cost Calculator](https://cost-calculator.bref.sh)** - Estimate AWS costs when running serverless applications on AWS Lambda.

### S3 Tools
- **[s3s3mirror](https://github.com/cobbzilla/s3s3mirror)** - A lightning-fast and highly concurrent utility for mirroring content from one S3 bucket to another.

### Security Tools
- **[Leapp](https://github.com/Noovolari/leapp)** - Cross-platform APP to manage Programmatic access in AWS.
- **[Prowler](https://github.com/prowler-cloud/prowler)** - Prowler is an Open Source Security tool to perform Cloud Security best practices assessments, audits, incident response, continuous monitoring, hardening and forensics readiness.
- **[AWS Security Tools](https://github.com/0xVariable/AWS-Security-Tools)** - A curated list of Security tools that you can use on AWS.

### SSM Tools
- **[aws-gate](https://github.com/xen0l/aws-gate)** - A Better AWS SSM Session manager CLI client.
- **[aws-ssm-ec2-proxy-command](https://github.com/qoomon/aws-ssm-ec2-proxy-command)** - Open an SSH connection to your ec2 instances via AWS SSM without the need to open any ssh port in you security groups.
- **[HQarroum/ssm-supercharged](https://github.com/HQarroum/ssm-supercharged)** - AWS SSM integration with OpenSSH + EC2 Instance Connect + sshuttle.

### Other Tools
- **[Steampipe](https://github.com/turbot/steampipe)** - Query AWS resources in a SQL like fashion.
- **[AWS Nuke](https://github.com/rebuy-de/aws-nuke)** - Remove all resources from an AWS account.

---

## Contributors
This project exists thanks to all the people who contribute.

[![Code Contributors](https://contrib.rocks/image?repo=dannysteenman/aws-toolbox)](https://github.com/dannysteenman/aws-toolbox/graphs/contributors)

See how you can [contribute to this repository.](https://github.com/dannysteenman/aws-toolbox/blob/main/.github/CONTRIBUTING.md)

## Author
Danny Steenman

[![](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/dannysteenman)
[![](https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white)](https://twitter.com/dannysteenman)
[![](https://img.shields.io/badge/GitHub-2b3137?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dannysteenman)
