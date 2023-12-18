#!/bin/bash

fileName=task-definition.yaml
stackName=gen

echo "Enter Account ID:"
read -e accountId

echo "Enter Profile:"
read -e profile

# Deploy CloudFormation stack with parameters
aws cloudformation deploy \
  --profile "$profile" \
  --template-file "$fileName" \
  --stack-name "$stackName-task-definition" \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides \
    StackName="$stackName" \
    AccountID="$accountId" \
    FileSystemName="$stackName"
