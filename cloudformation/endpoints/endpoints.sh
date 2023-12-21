#!/bin/bash

fileName=endpoints.yaml

echo "Enter Profile Name:"
read -e awsProfile

echo "VPC ID:"
read -e vpcId

echo "Subnet ID 1:"
read -e subnet1

echo "Subnet ID 2:"
read -e subnet2

echo "Subnet ID 3:"
read -e subnet3

echo "Instance Security Group Id:"
read -e securityGroup

# Deploy CloudFormation stack with parameters
aws cloudformation deploy \
  --profile "$awsProfile" \
  --template-file "$fileName" \
  --stack-name "endpoints" \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides \
    VpcId="$vpcId" \
    SubnetId1="$subnet1" \
    SubnetId2="$subnet2" \
    SubnetId3="$subnet3" \
    SecurityGroupId="$securityGroup"