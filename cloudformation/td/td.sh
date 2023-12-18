#!/bin/bash

fileName=td.yaml
stackName=gen

echo "Enter Account ID:"
read -e accountId

echo "Enter Profile:"
read -e profile

echo "Enter Gen File System ID:"
read -e fileSystemId

# Deploy CloudFormation stack with parameters
aws cloudformation deploy \
  --profile "$profile" \
  --template-file "$fileName" \
  --stack-name "task-definitions" \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides \
    AccountID="$accountId" \
    GenFileSystemId="$fileSystemId"
