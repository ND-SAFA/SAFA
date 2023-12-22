#!/bin/bash

fileName=policies.yaml

echo "Enter Profile Name:"
read -e awsProfile

echo "File: $fileName"

# Deploy CloudFormation stack with parameters
aws cloudformation deploy \
  --profile "$awsProfile" \
  --template-file "$fileName" \
  --stack-name "managed-policies" \
  --capabilities CAPABILITY_NAMED_IAM
