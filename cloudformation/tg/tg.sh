#!/bin/bash

fileName=tg.yaml
vpcId=vpc-0dc18129c0f9083f9

echo "Enter Profile Name:"
read -e awsProfile

echo "File: $fileName"

# Deploy CloudFormation stack with parameters
aws cloudformation deploy \
  --profile "$awsProfile" \
  --template-file "$fileName" \
  --stack-name "target-groups" \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides \
    VPCId="$vpcId" \
