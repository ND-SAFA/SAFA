#!/bin/bash

fileName=td.yaml

echo "Enter Account ID:"
read -e accountId

echo "Enter Profile:"
read -e profile

echo "Enter Gen File System ID:"
read -e fileSystemId

echo "Enter ENV (staging,development,production):"
read -e stage

# Deploy CloudFormation stack with parameters
aws cloudformation deploy \
  --profile "$profile" \
  --template-file "$fileName" \
  --stack-name "task-definitions" \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides \
    AccountID="$accountId" \
    GenFileSystemId="$fileSystemId" \
    BendEnvFile="$stage/api.env" \
    GenEnvFile="$stage/gen.env"
