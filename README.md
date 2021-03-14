<br/>
<p align="center">
  <img src="https://raw.githubusercontent.com/dannysteenman/aws-toolbox/main/images/aws-toolbox-logo.png">
</p>
<br/>

# AWS Toolbox

A collection of AWS tools like Shell & Python scripts that make your DevOps life a little easier.

## Table of Contents

- [AWS Toolbox](#aws-toolbox)
  - [Table of Contents](#table-of-contents)
  - [Contributing](#contributing)
  - [Getting started](#getting-started)
  - [Scripts sorted on AWS Service](#scripts-sorted-on-aws-service)
  - [List of useful DevOps tools:](#list-of-useful-devops-tools)
    - [API](#api)
    - [Infra as Code](#infra-as-code)
    - [CI/CD](#cicd)
  - [Creator](#creator)
  - [Contributors](#contributors)

## Contributing

Contributions are welcome!

Review the [Contributing Guidelines](https://github.com/dannysteenman/aws-toolbox/blob/main/.github/CONTRIBUTING.md).

## Getting started

- [What is the AWS Command Line Interface?](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)
- [How to install the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- [Configure the AWS CLI for usage](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
- [Some examples on how to use the AWS CLI to work with AWS Services](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-services.html)

## Scripts sorted on AWS Service

| General scripts                                                                  | Functionality                                                                                                        |
| -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **[boto3-multi-account-execution.py](general/boto3-multi-account-execution.py)** | This script gives you the ability to run Boto3 commands on all accounts which are specified in the aws_account_list. |

| EC2 scripts                                          | Functionality                                                                   |
| ---------------------------------------------------- | ------------------------------------------------------------------------------- |
| **[ec2-asg-ssh.sh](ec2/ec2-asg-ssh.sh)**             | A ssh wrapper for connecting quickly to EC2 instances in an Auto Scaling group. |
| **[ec2-available-eip.sh](ec2/ec2-available-eip.sh)** | Shows Elastic IP addresses which haven't been associated yet.                   |

| SSM scripts                                                    | Functionality                                                        |
| -------------------------------------------------------------- | -------------------------------------------------------------------- |
| **[ssm-parameter-delete.sh](ssm/ssm-parameter-delete.sh)**     | This script allows you to delete ssm parameters through a json file. |
| **[ssm-parameter-register.sh](ssm/ssm-parameter-register.sh)** | This script allows you to import ssm parameters through a json file. |

## List of useful DevOps tools:

### API

- **[steampipe](https://github.com/turbot/steampipe)** - Query AWS resources in a SQL like fashion.

### Infra as Code

- **[Awesome CDK](https://github.com/kolomied/awesome-cdk)** - Curated list of awesome AWS Cloud Development Kit (AWS CDK) open-source projects, guides, blogs and other resources.
- **[Awesome CloudFormation](https://github.com/aws-cloudformation/awesome-cloudformation)** - A curated list of resources and projects for working with AWS CloudFormation.

### CI/CD

- **[Awesome CI](https://github.com/ligurio/awesome-ci)** - List of Continuous Integration services
## Creator

**[Danny Steenman](https://dannys.cloud)**

## Contributors
