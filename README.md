![AWS Toolbox](aws-toolbox-header.jpg)

# AWS Toolbox 🧰

A collection of useful Shell & Python scripts that make your DevOps life easier in AWS. Furthermore you'll also find a list of links that point to awesome DevOps tools from other creators.

## Table of Contents

- [AWS Toolbox 🧰](#aws-toolbox-)
  - [Table of Contents](#table-of-contents)
  - [Contributing](#contributing)
  - [Getting started](#getting-started)
  - [Shell & Python scripts categorized by AWS Service](#shell--python-scripts-categorized-by-aws-service)
    - [General scripts](#general-scripts)
    - [CloudWatch scripts](#cloudwatch-scripts)
    - [EC2 scripts](#ec2-scripts)
    - [IAM scripts](#iam-scripts)
    - [S3 scripts](#s3-scripts)
    - [SSM scripts](#ssm-scripts)
  - [DevOps tools & Resources](#devops-tools--resources)
    - [General](#general)
    - [Authentication](#authentication)
    - [CI/CD](#cicd)
    - [EC2](#ec2)
    - [ECS](#ecs)
    - [IAM](#iam)
    - [Infra as Code](#infra-as-code)
    - [Lambda](#lambda)
    - [S3](#s3)
    - [SSM](#ssm)
  - [Blogroll](#blogroll)
  - [Author](#author)

## Contributing

Contributions are welcome!

Review the [Contributing Guidelines](https://github.com/dannysteenman/aws-toolbox/blob/main/.github/CONTRIBUTING.md).

## Getting started

- [What is the AWS Command Line Interface?](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)
- [How to install the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- [Configure the AWS CLI for usage](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
- [Some examples on how to use the AWS CLI to work with AWS Services](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-services.html)

## Shell & Python scripts categorized by AWS Service

### General scripts

- **[alias](cli/alias)** - This file contains a bunch of easy to remember aliases that runs complex AWS CLI commands.
- **[boto3_multi_account_execution.py](general/boto3_multi_account_execution.py)** - Gives you the ability to run Boto3 commands on all accounts which are specified in the aws_account_list.

### CloudWatch scripts
- **[cloudwatch_retention_policy.py](cloudwatch/cloudwatch_retention_policy.py)** - Sets a CloudWatch Logs Retention Policy to x number of days for all log groups in the region that you exported in your cli.

### EC2 scripts

- **[ec2_asg_ssh.sh](ec2/ec2_asg_ssh.sh)** - A ssh wrapper for connecting quickly to EC2 instances in an Auto Scaling group.
- **[ec2_available_eip.sh](ec2/ec2_available_eip.sh)** - Shows Elastic IP addresses which haven't been associated yet.
- **[ec2_req_spot_instances.sh](ec2/ec2_req_spot_instances.sh)** - Enables you to run a request for spot instances.
- **[ec2_resize_volume.sh](ec2/ec2_resize_volume.sh)** - specifies the desired volume size in GiB as a command line argument. If not specified, default to 20 GiB.

### IAM scripts

- **[iam_assume_role.sh](iam/iam_assume_role.sh)** - This script uses Simple Token Service (sts) to assume a role (on the destination account).
- **[iam_tag_secrets.py](iam/iam_tag_secrets.py)** - This script allows you to tag all your secrets in AWS Secrets Manager quickly.

### S3 scripts
- **[s3_create_tar_file.py](s3/s3_create_tar_file.py)** - Allows you to create tar file creation.
- **[s3_list_file_older_than_number_of_days.py](s3/s3_list_file_older_than_number_of_days.py)** - Allows you to list all files older than N numbers of days.
- **[s3_search_file_in_bucket.py](s3/s3_search_file_in_bucket.py)** - Allows you to search file in S3 bucket.
- **[s3_search_subdirectory.py](s3/s3_search_subdirectory.py)** - Allows you to search subdirectory under nested folder structure.
### SSM scripts
- **[ssm_parameter_delete.sh](ssm/ssm_parameter_delete.sh)** - Allows you to delete ssm parameters through a json file.
- **[ssm_parameter_register.sh](ssm/ssm_parameter_register.sh)** - Allows you to import ssm parameters through a json file.

## DevOps tools & Resources

This list contains links to tools that automate or simplify the usage of AWS in the console, CLI or API's.

### General

- **[Steampipe](https://github.com/turbot/steampipe)** - Query AWS resources in a SQL like fashion.
- **[AWS Nuke](https://github.com/rebuy-de/aws-nuke)** - Remove all resources from an AWS account.
- **[AWS Security Tools](https://github.com/0xVariable/AWS-Security-Tools)** - A curated list of Security tools that you can use on AWS.

### Authentication

- **[Leapp](https://github.com/Noovolari/leapp)** - Cross-platform APP to manage Programmatic access in AWS.

### CI/CD

- **[Awesome CI](https://github.com/ligurio/awesome-ci)** - List of Continuous Integration services.

### EC2

- **[AutoSpotting](https://github.com/AutoSpotting/AutoSpotting)** - AutoSpotting is the leading open source spot market automation tool, optimized towards quick/easy/frictionless adoption of the EC2 spot market at any scale.

### ECS

- **[Awesome ECS](https://github.com/nathanpeck/awesome-ecs)** - A curated list of awesome ECS guides, development tools, and resources.
- **[AWS Copilot CLI](https://github.com/aws/copilot-cli)** - The AWS Copilot CLI is a tool for developers to build, release and operate production ready containerized applications on Amazon ECS and AWS Fargate.

### IAM

- **[IAM Floyd](https://github.com/udondan/iam-floyd)** - AWS IAM policy statement generator with fluent interface.
- **[IAM Zero](https://iamzero.dev)** - IAM Zero detects identity and access management issues and automatically suggests least-privilege policies.

### Infra as Code

- **[Awesome CDK](https://github.com/kolomied/awesome-cdk)** - Curated list of awesome AWS Cloud Development Kit (AWS CDK) open-source projects, guides, blogs and other resources.
- **[Awesome CloudFormation](https://github.com/aws-cloudformation/awesome-cloudformation)** - A curated list of resources and projects for working with AWS CloudFormation.
- **[Awesome Terraform](https://github.com/shuaibiyy/awesome-terraform)** - Curated list of resources on HashiCorp's Terraform.
- **[CDK Snippets](https://dannys.cloud/autocomplete-aws-cdk-l1-constructs-vs-code)** - This extension adds L1 construct snippets from CDK into Visual Studio Code.
- **[CloudFormation Snippets](https://dannys.cloud/autocomplete-cloudformation-resources-vs-code)** - This extension adds snippets for all the AWS CloudFormation resources into Visual Studio Code.
- **[Former2](https://github.com/iann0036/former2)** - Generate CloudFormation / Terraform / Troposphere templates from your existing AWS resources.
- **[Open CDK Guide](https://github.com/kevinslin/open-cdk)** - This guide is an opinionated set of tips and best practices for working with the AWS Cloud Development Kit.

### Lambda

- **[AWS Lambda Power Tuning](https://github.com/alexcasalboni/aws-lambda-power-tuning)** - AWS Lambda Power Tuning is a state machine powered by AWS Step Functions that helps you optimize your Lambda functions for cost and/or performance in a data-driven way.
- **[Serverless Cost Calculator Comparison](http://serverlesscalc.com)** - Calculating the cost for AWS Lambda, Azure Functions, Google Cloud Functions. Providing good comparison or prediction on how the cost can vary depending on the memory, execution time, and number of executions on different cloud providers.
- **[Serverless Cost Calculator](https://cost-calculator.bref.sh)** - Estimate AWS costs when running serverless applications on AWS Lambda.

### S3

- **[s3s3mirror](https://github.com/cobbzilla/s3s3mirror)** - A lightning-fast and highly concurrent utility for mirroring content from one S3 bucket to another.

### SSM

- **[aws-gate](https://github.com/xen0l/aws-gate)** - A Better AWS SSM Session manager CLI client.
- **[aws-ssm-ec2-proxy-command](https://github.com/qoomon/aws-ssm-ec2-proxy-command)** - Open an SSH connection to your ec2 instances via AWS SSM without the need to open any ssh port in you security groups.

## Blogroll

A collection of AWS blogs that contain helpful tips and tricks.

| RSS                                                                                                                                      | Blog title                                                | Description                                                                                                     |
| ---------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| <a href="http://blogs.aws.amazon.com/security/blog/feed/recentPosts.rss"> <img src="rss.png" width="22" height="22" > </a>               | **[AWS Security](https://aws.amazon.com/blogs/security)** | The latest AWS security, identity, and compliance launches, announcements, and how-to posts.                    |
| <a href="http://blogs.aws.amazon.com/application-management/blog/feed/recentPosts.rss"> <img src="rss.png" width="22" height="22" > </a> | **[AWS DevOps](https://aws.amazon.com/blogs/devops)**     | The latest AWS DevOps announcements, and how-to posts.                                                          |
| <a href="http://techblog.netflix.com/feeds/posts/default"> <img src="rss.png" width="22" height="22" > </a>                              | **[Netflix Techblog](http://techblog.netflix.com)**       | Learn about Netflix’s world class engineering efforts, company culture, product developments and more.          |
| <a href="https://www.lastweekinaws.com/feed/"> <img src="rss.png" width="22" height="22" > </a>                                          | **[Last week in AWS](https://www.lastweekinaws.com)**     | We’re the internet’s only snarky, sarcastic resource for literally anything and everything AWS… and we know it. |

---

## Author

**[Danny Steenman](https://dannys.cloud)**

<p align="left">
  <a href="https://dannys.cloud/twitter"><img src="https://img.shields.io/twitter/follow/dannysteenman?label=%40dannysteenman&style=social"></a>
</p>
