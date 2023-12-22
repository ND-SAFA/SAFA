#!/bin/bash

fileName=roles.yaml

echo "Enter Profile Name:"
read -e awsProfile

aws sts get-caller-identity --profile "$awsProfile"
echo "Acount ID: $accountId"
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
