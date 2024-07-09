# [![AWS Toolbox header](https://raw.githubusercontent.com/dannysteenman/aws-toolbox/main/icons/github-header-image.png)](https://towardsthecloud.com)

# AWS Toolbox 🧰

Scripts and tools for AWS cloud automation.

## Overview

This repository contains scripts for AWS Developers, DevOps Engineers, and Cloud Architects. Tools focus on task automation and infrastructure management.

## Usage

Navigate to the relevant AWS service section. Click on the script name in the table below to open the content and usage instructions.


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

## AWS Service Management Scripts

This collection includes Python and Bash scripts for managing various AWS services. The scripts are organized by service for easy navigation.

| Service             | Script Name                                                                            | Description                                     |
| ------------------- | -------------------------------------------------------------------------------------- | ----------------------------------------------- |
| CloudFormation      | [delete_stackset.py](cloudformation/delete_stackset.py)                                | Deletes stackset and associated stack instances |
| CloudWatch          | [delete_cloudwatch_log_groups.py](cloudwatch/delete_cloudwatch_log_groups.py)          | Deletes CloudWatch log groups based on age      |
| CloudWatch          | [set_cloudwatch_logs_retention.py](cloudwatch/set_cloudwatch_logs_retention.py)        | Sets retention policy for CloudWatch log groups |
| CodePipeline        | [slack_notification.py](codepipeline/slack_notification.py)                            | Enables CodePipeline notifications on Slack     |
| EC2                 | [delete_all_unattached_volumes.py](ec2/delete_all_unattached_volumes.py)               | Deletes unattached EBS volumes                  |
| EC2                 | [delete_all_unused_elastic_ips.py](ec2/delete_all_unused_elastic_ips.py)               | Deletes unused Elastic IPs                      |
| EC2                 | [delete_all_unused_keypairs.py](ec2/delete_all_unused_keypairs.py)                     | Deletes unused EC2 keypairs                     |
| EC2                 | [delete_unused_keypairs.py](ec2/delete_unused_keypairs.py)                             | Deletes unused EC2 keypairs in a single region  |
| EC2                 | [delete_tagged_security_groups.py](ec2/delete_tagged_security_groups.py)               | Deletes tagged security groups                  |
| EC2                 | [find_all_unattached_volumes.py](ec2/find_all_unattached_volumes.py)                   | Finds unattached EBS volumes                    |
| EC2                 | [find_all_unused_keypairs.py](ec2/find_all_unused_keypairs.py)                         | Finds all EC2 keypairs                          |
| EC2                 | [find_unused_keypairs.py](ec2/find_unused_keypairs.py)                                 | Finds EC2 keypairs in a single region           |
| EC2                 | [asg_ssh.sh](ec2/asg_ssh.sh)                                                           | SSH wrapper for Auto Scaling group instances    |
| EC2                 | [available_eip.sh](ec2/available_eip.sh)                                               | Lists unassociated Elastic IPs                  |
| EC2                 | [req_spot_instances.sh](ec2/req_spot_instances.sh)                                     | Requests spot instances                         |
| EC2                 | [resize_volume.sh](ec2/resize_volume.sh)                                               | Resizes EBS volume                              |
| ECS                 | [delete_all_inactive_task_definitions.py](ecs/delete_all_inactive_task_definitions.py) | Deletes inactive ECS task definitions           |
| ECS                 | [publish_ecr_image.sh](ecs/publish_ecr_image.sh)                                       | Publishes Docker image to ECR                   |
| EFS                 | [delete_tagged_efs.py](efs/delete_tagged_efs.py)                                       | Deletes tagged EFS and mount targets            |
| IAM                 | [delete_iam_user](iam/delete_iam_user.py)                                              | Deletes IAM users                               |
| IAM                 | [key_rotator](iam/key_rotator.py)                                                      | Rotates IAM user keys                           |
| IAM                 | [assume_role.sh](iam/assume_role.sh)                                                   | Assumes IAM role                                |
| IAM Identity Center | [assign_sso_access_by_ou.py](organizations/assign_sso_access_by_ou.py)                 | Assigns SSO access for accounts in an OU        |
| IAM Identity Center | [import_users_to_aws_sso.py](organizations/import_users_to_aws_sso.py)                 | Imports users/groups to AWS SSO                 |
| Organizations       | [list_accounts_sso_assignments.py](organizations/list_accounts_sso_assignments.py)     | Lists SSO assignments for accounts              |
| Organizations       | [list_accounts_by_ou.py](organizations/list_accounts_by_ou.py)                         | Lists accounts in an OU                         |
| Organizations       | [remove_sso_access_by_ou.py](organizations/remove_sso_access_by_ou.py)                 | Removes SSO access for accounts in an OU        |
| S3                  | [create_tar_file.py](s3/create_tar_file.py)                                            | Creates tar files                               |
| S3                  | [delete_empty_buckets.py](s3/delete_empty_buckets.py)                                  | Deletes empty S3 buckets                        |
| S3                  | [list_file_older_than_number_of_days.py](s3/list_file_older_than_number_of_days.py)    | Lists old files in S3                           |
| S3                  | [search_bucket_and_delete.py](s3/search_bucket_and_delete.py)                          | Deletes S3 bucket and its contents              |
| S3                  | [search_file_in_bucket.py](s3/search_file_in_bucket.py)                                | Searches for files in S3 bucket                 |
| S3                  | [search_key_bucket.py](s3/search_key_bucket.py)                                        | Searches for a key in S3 bucket                 |
| S3                  | [search_multiple_keys_bucket.py](s3/search_multiple_keys_bucket.py)                    | Searches for multiple keys in S3 bucket         |
| S3                  | [search_subdirectory.py](s3/search_subdirectory.py)                                    | Searches subdirectories in S3                   |
| SSM                 | [parameter_delete.sh](ssm/parameter_delete.sh)                                         | Deletes SSM parameters                          |
| SSM                 | [parameter_register.sh](ssm/parameter_register.sh)                                     | Imports SSM parameters                          |
| Other               | [delete_unused_security_groups.py](general/delete_unused_security_groups.py)           | Deletes unused security groups                  |
| Other               | [find_unused_security_groups.py](general/find_unused_security_groups.py)               | Finds unused security groups                    |
| Other               | [alias](cli/alias)                                                                     | AWS CLI command aliases                         |
| Other               | [tag_secrets.py](general/tag_secrets.py)                                               | Tags Secrets Manager secrets                    |
| Other               | [multi_account_execution.py](general/multi_account_execution.py)                       | Runs commands across multiple AWS accounts      |


---

## AWS Tools and Utilities

This section lists tools that enhance AWS usage across console, CLI, and APIs.

### EC2
- [AutoSpotting](https://github.com/AutoSpotting/AutoSpotting) - Open-source spot market automation tool for easy adoption at scale.

### ECS
- [Awesome ECS](https://github.com/nathanpeck/awesome-ecs) - Curated list of ECS guides and resources.
- [AWS Copilot CLI](https://github.com/aws/copilot-cli) - CLI for building and operating containerized applications on ECS and Fargate.
- [ECS Compose-X](https://github.com/compose-x/ecs_composex) - Tool to generate CFN templates from docker-compose files with added AWS resource definitions.

### IAM
- [AWS IAM Actions](https://www.awsiamactions.io) - Comprehensive IAM action listing and policy generator.
- [IAM Floyd](https://github.com/udondan/iam-floyd) - Fluent interface for IAM policy statement generation.
- [IAM Zero](https://iamzero.dev) - Automated least-privilege policy suggestion tool.

### Infrastructure as Code
- [Awesome CDK](https://github.com/kolomied/awesome-cdk) - Curated list of AWS CDK resources.
- [AWS CDK Starterkit](https://github.com/dannysteenman/aws-cdk-starterkit) - Rapid AWS CDK app deployment via GitHub actions.
- [Awesome CloudFormation](https://github.com/aws-cloudformation/awesome-cloudformation) - Curated CloudFormation resources.
- [Awesome Terraform](https://github.com/shuaibiyy/awesome-terraform) - Curated Terraform resources.
- [VSCode CDK Snippets](https://marketplace.visualstudio.com/items?itemName=dannysteenman.cdk-snippets) - VS Code extension for CDK construct snippets.
- [VSCode CloudFormation Snippets](https://marketplace.visualstudio.com/items?itemName=dannysteenman.cloudformation-yaml-snippets) - VS Code extension for CloudFormation resource snippets.
- [VSCode SAM Snippets](https://marketplace.visualstudio.com/items?itemName=dannysteenman.sam-snippets) - VS Code extension for CloudFormation resource snippets.
- [Former2](https://github.com/iann0036/former2) - Template generator from existing AWS resources.
- [Open CDK Guide](https://github.com/kevinslin/open-cdk) - Opinionated AWS CDK best practices guide.

### Lambda
- [AWS Lambda Power Tuning](https://github.com/alexcasalboni/aws-lambda-power-tuning) - Step Functions-based Lambda optimization tool.
- [Serverless Cost Calculator Comparison](http://serverlesscalc.com) - Cost comparison tool for serverless functions across cloud providers.
- [Serverless Cost Calculator](https://cost-calculator.bref.sh) - AWS Lambda cost estimation tool.

### S3
- [s3s3mirror](https://github.com/cobbzilla/s3s3mirror) - High-performance S3 bucket mirroring utility.

### Security
- [Leapp](https://github.com/Noovolari/leapp) - Cross-platform AWS programmatic access manager.
- [Prowler](https://github.com/prowler-cloud/prowler) - Open-source security assessment and auditing tool.
- [AWS Security Tools](https://github.com/0xVariable/AWS-Security-Tools) - Curated list of AWS security tools.

### SSM
- [aws-gate](https://github.com/xen0l/aws-gate) - Enhanced AWS SSM Session Manager CLI.
- [aws-ssm-ec2-proxy-command](https://github.com/qoomon/aws-ssm-ec2-proxy-command) - SSH to EC2 via SSM without open ports.
- [ssm-supercharged](https://github.com/HQarroum/ssm-supercharged) - SSM integration with OpenSSH, EC2 Instance Connect, and sshuttle.

### Miscellaneous
- [Steampipe](https://github.com/turbot/steampipe) - SQL-like querying for AWS resources.
- [AWS Nuke](https://github.com/rebuy-de/aws-nuke) - AWS account resource removal tool.

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
