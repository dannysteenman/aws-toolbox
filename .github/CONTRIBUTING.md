# Contribution Guidelines

Thank you for your interest in contributing to the [AWS Toolbox.](https://github.com/dannysteenman/aws-toolbox)

Please read through this document before submitting any issues or pull requests to ensure we have all the necessary information to effectively respond to your issue or contribution.

## Reporting Bugs or Feature Requests

We welcome you to use the GitHub issue tracker to report bugs or suggest features.

When filing an issue, please check [existing open](https://github.com/dannysteenman/aws-toolbox/issues), or [recently closed](https://github.com/dannysteenman/aws-toolbox/issues?utf8=%E2%9C%93&q=is%3Aissue%20is%3Aclosed%20), issues to make sure somebody else hasn't already reported the issue. Please try to include as much information as you can.

## Contributing new scripts via Pull Requests

Contributions via pull requests are much appreciated. Before sending us a pull request, please ensure that:

1. You are working against the latest source on the _main_ branch.
2. You check existing open, and recently merged, pull requests to make sure someone else hasn't made a similar request already.
3. You open an issue to discuss any significant work - we would hate for your time to be wasted.

To send us a pull request, please:

1. Fork the repository.
2. Modify the source, focusing on the specific change you are contributing. 
3. Reformat all the code, for Python scripts we use Black and for linting we use Flake8 with the following arguments: "--ignore=E203,E266,E501,F401,W503"
4. If you commit and push the changes in your fork it will automatically trigger a linter action in GitHub Actions to validate the change.
5. Commit to your fork using clear commit messages.
6. Send us a pull request, answering any default questions in the pull request interface.
7. Stay involved in the conversation.

GitHub provides additional documentation on [forking a repository](https://help.github.com/articles/fork-a-repo/) and
[creating a pull request](https://help.github.com/articles/creating-a-pull-request/).

## Updating your PR

If the maintainers notice anything that we'd like changed, we'll ask you to edit your PR before we merge it. There's no need to open a new PR, just edit the existing one. If you're not sure how to do that, [then here is a guide](https://github.com/RichardLitt/knowledge/blob/master/github/amending-a-commit-guide.md) on the different ways you can update your PR so that we can merge it.

## Criteria for accepting scripts

We want to keep the quality of the scripts in our list as high as possible. In most cases, we will check for things like the following:

- Whether the script solves a repetitive task.
- Whether the script can give better insights on AWS Resources.
- Whether the script contains docstrings/comments at the top to explain it's functionality.
- Consider if the script is significantly useful for both new and experienced AWS CLI users.

## Licensing

See the [LICENSE](https://github.com/dannysteenman/aws-toolbox/blob/main/LICENSE) file for our project's licensing. We will ask you to confirm the licensing of your contribution.
