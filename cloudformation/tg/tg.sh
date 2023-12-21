#!/bin/bash

fileName=tg.yaml

echo "Enter Profile Name:"
read -e awsProfile

echo "VPC ID:"
read -e vpcId

# Deploy CloudFormation stack with parameters
aws cloudformation deploy \
  --profile "$awsProfile" \
  --template-file "$fileName" \
  --stack-name "target-groups" \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides \
    VPCId="$vpcId" \
