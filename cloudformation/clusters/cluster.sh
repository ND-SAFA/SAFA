#!/bin/bash

fileName=cluster.yaml

echo "Enter Profile Name:"
read -e awsProfile

echo "File: $fileName"

# Deploy CloudFormation stack with parameters
aws cloudformation deploy \
  --profile "$awsProfile" \
  --template-file "$fileName" \
  --stack-name "clusters" \
  --capabilities CAPABILITY_NAMED_IAM
