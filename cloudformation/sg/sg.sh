#!/bin/bash

fileName=sg.yaml

echo "Enter Profile Name:"
read -e awsProfile

echo "VPC ID:"
read -e vpcId

# Deploy CloudFormation stack with parameters
aws cloudformation deploy \
  --profile "$awsProfile" \
  --template-file "$fileName" \
  --stack-name "security-groups" \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides \
    VpcId="$vpcId" \
