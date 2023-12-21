#!/bin/bash

fileName=roles.yaml

echo "Enter Profile Name:"
read -e awsProfile

echo "Acount ID:"
read -e accountId

executionPolicyArn="arn:aws:iam::$accountId:policy/general-execution-policy"

# Deploy CloudFormation stack with parameters
aws cloudformation deploy \
  --profile "$awsProfile" \
  --template-file "$fileName" \
  --stack-name "roles" \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    ExecutionPolicyArn="$executionPolicyArn" \
