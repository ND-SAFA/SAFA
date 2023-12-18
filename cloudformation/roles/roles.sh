#!/bin/bash

fileName=roles.yaml
executionPolicyArn=arn:aws:iam::238179308728:policy/general-execution-policy

echo "Enter Profile Name:"
read -e awsProfile

echo "File: $fileName"

# Deploy CloudFormation stack with parameters
aws cloudformation deploy \
  --profile "$awsProfile" \
  --template-file "$fileName" \
  --stack-name "roles" \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    ExecutionPolicyArn="$executionPolicyArn" \
