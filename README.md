![AWS Toolbox](aws-toolbox-header.jpg)

# AWS Toolbox 🧰

A collection of DevOps tools including shell & python scripts that automate the boring stuff in AWS.

## Table of Contents

- [AWS Toolbox 🧰](#aws-toolbox-)
  - [Table of Contents](#table-of-contents)
  - [Contributing](#contributing)
  - [Getting started](#getting-started)
  - [Scripts categorized by AWS Service](#scripts-categorized-by-aws-service)
  - [List of useful DevOps tools & resources](#list-of-useful-devops-tools--resources)
    - [API](#api)
    - [CI/CD](#cicd)
    - [Cloud Access](#cloud-access)
    - [EC2](#ec2)
    - [ECS](#ecs)
    - [Infra as Code](#infra-as-code)
    - [Lambda](#lambda)
    - [S3](#s3)
  - [Author](#author)

## Contributing

Contributions are welcome!

Review the [Contributing Guidelines](https://github.com/dannysteenman/aws-toolbox/blob/main/.github/CONTRIBUTING.md).

## Getting started

- [What is the AWS Command Line Interface?](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)
- [How to install the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- [Configure the AWS CLI for usage](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
- [Some examples on how to use the AWS CLI to work with AWS Services](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-services.html)

## Scripts categorized by AWS Service

| **General scripts**                                                              | **Functionality**                                                                                                           |
| -------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **[alias](cli/alias)**                                                           | This file contains a bunch of easy to remember aliases that runs complex AWS CLI commands.                                  |
| **[boto3_multi_account_execution.py](general/boto3_multi_account_execution.py)** | Gives you the ability to run Boto3 commands on all accounts which are specified in the aws_account_list.                    |
| **CloudWatch scripts**                                                           |                                                                                                                             |
| **[cloudwatch_retention_policy.py](cloudwatch/cloudwatch_retention_policy.py)**  | Sets a CloudWatch Logs Retention Policy to x number of days for all log groups in the region that you exported in your cli. |
| **EC2 scripts**                                                                  |                                                                                                                             |
| **[ec2_asg_ssh.sh](ec2/ec2_asg_ssh.sh)**                                         | A ssh wrapper for connecting quickly to EC2 instances in an Auto Scaling group.                                             |
| **[ec2_available_eip.sh](ec2/ec2_available_eip.sh)**                             | Shows Elastic IP addresses which haven't been associated yet.                                                               |
| **SSM scripts**                                                                  |                                                                                                                             |
| **[ssm_parameter_delete.sh](ssm/ssm_parameter_delete.sh)**                       | Allows you to delete ssm parameters through a json file.                                                                    |
| **[ssm_parameter_register.sh](ssm/ssm_parameter_register.sh)**                   | Allows you to import ssm parameters through a json file.                                                                    |

## List of useful DevOps tools & resources

### API

- **[steampipe](https://github.com/turbot/steampipe)** - Query AWS resources in a SQL like fashion.

### CI/CD

- **[Awesome CI](https://github.com/ligurio/awesome-ci)** - List of Continuous Integration services.

### Cloud Access

- **[Leapp](https://github.com/Noovolari/leapp)** - Cross-platform APP to manage Programmatic access in AWS.

### EC2

- **[AutoSpotting](https://github.com/AutoSpotting/AutoSpotting)** - AutoSpotting is the leading open source spot market automation tool, optimized towards quick/easy/frictionless adoption of the EC2 spot market at any scale.

### ECS

- **[Awesome ECS](https://github.com/nathanpeck/awesome-ecs)** - A curated list of awesome ECS guides, development tools, and resources.
- **[AWS Copilot CLI](https://github.com/aws/copilot-cli)** - The AWS Copilot CLI is a tool for developers to build, release and operate production ready containerized applications on Amazon ECS and AWS Fargate.

### Infra as Code

- **[Awesome CDK](https://github.com/kolomied/awesome-cdk)** - Curated list of awesome AWS Cloud Development Kit (AWS CDK) open-source projects, guides, blogs and other resources.
- **[Awesome CloudFormation](https://github.com/aws-cloudformation/awesome-cloudformation)** - A curated list of resources and projects for working with AWS CloudFormation.
- **[Awesome Terraform](https://github.com/shuaibiyy/awesome-terraform)** - Curated list of resources on HashiCorp's Terraform.
- **[CloudFormation Snippets](https://github.com/dannysteenman/cloudformation-yaml-snippets)** - This VS Code extension adds autocompletion for all the resources that AWS CloudFormation supports.
- **[Open CDK Guide](https://github.com/kevinslin/open-cdk)** - This guide is an opinionated set of tips and best practices for working with the AWS Cloud Development Kit.

### Lambda

- **[AWS Lambda Power Tuning](https://github.com/alexcasalboni/aws-lambda-power-tuning)** - AWS Lambda Power Tuning is a state machine powered by AWS Step Functions that helps you optimize your Lambda functions for cost and/or performance in a data-driven way.
- **[Serverless Cost Calculator Comparison](http://serverlesscalc.com)** - Calculating the cost for AWS Lambda, Azure Functions, Google Cloud Functions. Providing good comparison or prediction on how the cost can vary depending on the memory, execution time, and number of executions on different cloud providers.
- **[Serverless Cost Calculator](https://cost-calculator.bref.sh)** - Estimate AWS costs when running serverless applications on AWS Lambda.

### S3

- **[s3s3mirror](https://github.com/cobbzilla/s3s3mirror)** - A lightning-fast and highly concurrent utility for mirroring content from one S3 bucket to another.

## Author

**[Danny Steenman](https://dannys.cloud)**
