#!/bin/bash

# PROFILE
echo "Enter your AWS CLI profile:"
#read -e awsProfile
awsProfile=development


echo "Enter Github Connection Name:"
#read -e connectionName
connectionName=safa

query_str="Connections[?ConnectionName=='$connectionName'].ConnectionArn"
echo "Query: $query_str"
# Get the GitHub connection ARN using AWS CLI
githubConnectionArn=$(aws codestar-connections list-connections \
    --profile "$awsProfile" \
    --provider-type GitHub \
    --query "$query_str" \
    --output text)
aws codestar-connections list-connections \
    --profile "$awsProfile" \
    --provider-type GitHub \
    --query "$query_str" \
    --output text

echo "H: $githubConnectionArn"