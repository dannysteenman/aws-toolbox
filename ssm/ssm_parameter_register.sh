#!/bin/sh
# This script allows you to import ssm parameters through a json file (see ssm-parameters-dev.json for example).
# Create a json file for each specific environment in which you need parameters.
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
    Type=$(echo $parameter | jq -r .Type)
    Name=$(echo $parameter | jq -r .Name)
    Value=$(echo $parameter | jq -r .Value)

    aws ssm put-parameter --type $Type --name $Name --value $Value
done
