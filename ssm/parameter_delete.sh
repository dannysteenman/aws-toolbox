#!/bin/zsh
# This script allows you to delete ssm parameters through a json file (see ssm-parameters-dev.json for example).
# Create a json file for each specific environment in which you need to delete parameters.
# NOTE: This script uses jq, make sure it is installed on your system

env=$1
if [ -z "$env" ]; then
    echo "env required"
    exit
fi

script_dir=$(
    cd $(dirname $0)
    pwd
)
parameters=$(cat $script_dir/ssm-parameters-$env.json)
len=$(echo $parameters | jq length)
for i in $(seq 0 $(($len - 1))); do
    parameter=$(echo $parameters | jq .[$i])
    Name=$(echo $parameter | jq -r .Name)

    aws ssm delete-parameter --name $Name
done
