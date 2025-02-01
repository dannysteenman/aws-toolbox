# [![AWS Toolbox header](./icons/github-header-image.png)](https://towardsthecloud.com)

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

| Category       | Script Name                                                                                       | Description                                                        |
| -------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| AppStream      | [appstream_delete_image.py](appstream/appstream_delete_image.py)                                  | Unshares AppStream image, then deletes it                          |
| CloudFormation | [cfn_delete_stackset.py](cloudformation/cfn_delete_stackset.py)                                   | Deletes stackset and associated instances                          |
| CloudWatch     | [cw_count_log_groups.py](cloudwatch/cw_count_log_groups.py)                                       | Counts the total number of CloudWatch log groups in an AWS account |
| CloudWatch     | [cw_delete_log_groups.py](cloudwatch/cw_delete_log_groups.py)                                     | Deletes log groups based on age                                    |
| CloudWatch     | [cw_fetch_log_groups_with_creation_date.py](cloudwatch/cw_fetch_log_groups_with_creation_date.py) | Fetches log groups with creation date                              |
| CloudWatch     | [cw_set_retention_policy.py](cloudwatch/cw_set_retention_policy.py)                               | Sets retention policy for log groups                               |
| CodePipeline   | [cp_slack_notifications.py](codepipeline/cp_slack_notifications.py)                               | Enables notifications on Slack                                     |
| EC2            | [ec2_delete_unattached_volumes.py](ec2/ec2_delete_unattached_volumes.py)                          | Deletes unattached EBS volumes                                     |
| EC2            | [ec2_delete_orphaned_snapshots.py](ec2/ec2_delete_orphaned_snapshots.py)                          | Deletes snapshots that are not associated with any volumes         |
| EC2            | [ec2_delete_ssh_access_security_groups.py](ec2/ec2_delete_ssh_access_security_groups.py)          | Deletes SSH (port 22) inbound rules from all security groups       |
| EC2            | [ec2_delete_unused_amis.py](ec2/ec2_delete_unused_amis.py)                                        | Deletes unused AMIs (Amazon Machine Images) in an AWS account      |
| EC2            | [ec2_delete_unused_eips.py](ec2/ec2_delete_unused_eips.py)                                        | Deletes unused Elastic IPs                                         |
| EC2            | [ec2_delete_unused_keypairs_all_regions.py](ec2/ec2_delete_unused_keypairs_all_regions.py)        | Deletes unused EC2 keypairs in all regions                         |
| EC2            | [ec2_delete_unused_keypairs_single_region.py](ec2/ec2_delete_unused_keypairs_single_region.py)    | Deletes unused EC2 keypairs in a single region                     |
| EC2            | [ec2_delete_tagged_security_groups.py](ec2/ec2_delete_tagged_security_groups.py)                  | Deletes tagged security groups                                     |
| EC2            | [ec2_find_unattached_volumes.py](ec2/ec2_find_unattached_volumes.py)                              | Finds unattached EBS volumes                                       |
| EC2            | [ec2_asg_ssh.sh](ec2/ec2_asg_ssh.sh)                                                              | SSH wrapper for Auto Scaling group instances                       |
| EC2            | [ec2_list_available_eips.sh](ec2/ec2_list_available_eips.sh)                                      | Lists unassociated Elastic IPs                                     |
| EC2            | [ec2_request_spot_instances.sh](ec2/ec2_request_spot_instances.sh)                                | Requests spot instances                                            |
| EC2            | [ec2_resize_volume.sh](ec2/ec2_resize_volume.sh)                                                  | Resizes EBS volume                                                 |
| ECS            | [ecs_delete_inactive_task_definitions.py](ecs/ecs_delete_inactive_task_definitions.py)            | Deletes inactive ECS task definitions                              |
| ECS            | [ecs_publish_ecr_image.sh](ecs/ecs_publish_ecr_image.sh)                                          | Publishes Docker image to ECR                                      |
| EFS            | [efs_delete_tagged_filesystems.py](efs/efs_delete_tagged_filesystems.py)                          | Deletes tagged EFS and mount targets                               |
| IAM            | [iam_delete_user.py](iam/iam_delete_user.py)                                                      | Deletes IAM users                                                  |
| IAM            | [iam_identity_center_create_users.py](iam/iam_identity_center_create_users.py)                    | Create IAM Identity Center (SSO) users                             |
| IAM            | [iam_rotate_access_keys.py](iam/iam_rotate_access_keys.py)                                        | Rotates IAM user keys                                              |
| IAM            | [iam_assume_role.sh](iam/iam_assume_role.sh)                                                      | Assumes IAM role                                                   |
| Organizations  | [org_assign_sso_access_by_ou.py](organizations/org_assign_sso_access_by_ou.py)                    | Assigns SSO access for accounts in an OU                           |
| Organizations  | [org_import_users_to_sso.py](organizations/org_import_users_to_sso.py)                            | Imports users/groups to AWS SSO                                    |
| Organizations  | [org_list_accounts_by_ou.py](organizations/org_list_accounts_by_ou.py)                            | Lists accounts in an OU                                            |
| Organizations  | [org_list_sso_assignments.py](organizations/org_list_sso_assignments.py)                          | Lists SSO assignments for accounts                                 |
| Organizations  | [org_remove_sso_access_by_ou.py](organizations/org_remove_sso_access_by_ou.py)                    | Removes SSO access for accounts in an OU                           |
| S3             | [s3_create_tar.py](s3/s3_create_tar.py)                                                           | Creates tar files                                                  |
| S3             | [s3_delete_empty_buckets.py](s3/s3_delete_empty_buckets.py)                                       | Deletes empty S3 buckets                                           |
| S3             | [s3_list_old_files.py](s3/s3_list_old_files.py)                                                   | Lists old files in S3                                              |
| S3             | [s3_search_bucket_and_delete.py](s3/s3_search_bucket_and_delete.py)                               | Deletes S3 bucket and its contents                                 |
| S3             | [s3_search_bucket_and_download.py](s3/s3_search_bucket_and_download.py)                           | Finds S3 bucket and download all its content                       |
| S3             | [s3_search_file.py](s3/s3_search_file.py)                                                         | Searches for files in S3 bucket                                    |
| S3             | [s3_search_key.py](s3/s3_search_key.py)                                                           | Searches for a key in S3 bucket                                    |
| S3             | [s3_search_multiple_keys.py](s3/s3_search_multiple_keys.py)                                       | Searches for multiple keys in S3 bucket                            |
| S3             | [s3_search_subdirectory.py](s3/s3_search_subdirectory.py)                                         | Searches subdirectories in S3                                      |
| SSM            | [ssm_delete_parameters.sh](ssm/ssm_delete_parameters.sh)                                          | Deletes SSM parameters                                             |
| SSM            | [ssm_import_parameters.sh](ssm/ssm_import_parameters.sh)                                          | Imports SSM parameters                                             |
| General        | [delete_unused_security_groups.py](general/delete_unused_security_groups.py)                      | Deletes unused security groups                                     |
| General        | [aws_cli_aliases.sh](cli/aws_cli_aliases.sh)                                                      | AWS CLI command aliases                                            |
| General        | [tag_secrets_manager_secrets.py](general/tag_secrets_manager_secrets.py)                          | Tags Secrets Manager secrets                                       |
| General        | [set-alternate-contact.py](general/set-alternate-contact.py)                                      | Sets alternate contacts for all accounts in an organization        |
| General        | [multi_account_command_executor.py](general/multi_account_command_executor.py)                    | Runs commands across multiple AWS accounts                         |


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
- [AWS CDK Starterkit](https://github.com/dannysteenman/aws-cdk-starterkit) - Rapid AWS CDK app deployment via GitHub actions.
- [AWS CloudFormation Starterkit](https://github.com/dannysteenman/aws-cloudformation-starterkit) - Rapid AWS CloudFormation stack deployment via GitHub actions.
- [Awesome CDK](https://github.com/kolomied/awesome-cdk) - Curated list of AWS CDK resources.
- [Awesome CloudFormation](https://github.com/aws-cloudformation/awesome-cloudformation) - Curated CloudFormation resources.
- [Awesome Terraform](https://github.com/shuaibiyy/awesome-terraform) - Curated Terraform resources.
- [Former2](https://github.com/iann0036/former2) - Template generator from existing AWS resources.
- [Open CDK Guide](https://github.com/kevinslin/open-cdk) - Opinionated AWS CDK best practices guide.
- [VSCode IAM Actions Snippets](https://github.com/dannysteenman/vscode-iam-actions-snippets) - Adds autocompletion in VS Code for AWS IAM policy actions.
- [VSCode IAM Service Principal Snippets](https://github.com/dannysteenman/vscode-iam-service-principal-snippets) - Adds autocompletion in VS Code for AWS service principals.
- [VSCode CDK Snippets](https://marketplace.visualstudio.com/items?itemName=dannysteenman.cdk-snippets) - VS Code extension for CDK construct snippets.
- [VSCode CloudFormation Snippets](https://marketplace.visualstudio.com/items?itemName=dannysteenman.cloudformation-yaml-snippets) - VS Code extension for CloudFormation resource snippets.
- [VSCode SAM Snippets](https://marketplace.visualstudio.com/items?itemName=dannysteenman.sam-snippets) - VS Code extension for CloudFormation resource snippets.

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
- [Cloud Custodian](https://github.com/cloud-custodian/cloud-custodian) - Cloud governance platform for AWS.
- [Service Screener](https://github.com/aws-samples/service-screener-v2) - Tool to evaluate your AWS service configurations based on AWS and community best practices.
- [Steampipe](https://github.com/turbot/steampipe) - SQL-like querying for AWS resources.
- [AWS Nuke](https://github.com/rebuy-de/aws-nuke) - AWS account resource removal tool.

---

## Contributors
This project exists thanks to all the people who contribute.

[![Code Contributors](https://contrib.rocks/image?repo=dannysteenman/aws-toolbox)](https://github.com/dannysteenman/aws-toolbox/graphs/contributors)

See how you can [contribute to this repository.](https://github.com/dannysteenman/aws-toolbox/blob/main/.github/CONTRIBUTING.md)

## Author
[Danny Steenman](https://towardsthecloud.com/about)

[![](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/dannysteenman)
[![](https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white)](https://twitter.com/dannysteenman)
[![](https://img.shields.io/badge/GitHub-2b3137?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dannysteenman)
