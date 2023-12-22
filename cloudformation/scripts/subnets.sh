#!/bin/bash

fileName=subnets.yaml
stackName=gen

echo "Enter Profile:"
read -e profile

echo "VPC ID:"
read -e vpc

echo "CIDR A Number: (172.31.X.0/22)"
read -e cidrA
cidrA="172.31.$cidrA.0/22"

echo "CIDR B Number: (172.31.X.0/22)"
read -e cidrB
cidrB="172.31.$cidrB.0/22"

echo "CIDR C Number: (172.31.X.0/22)"
read -e cidrC
cidrC="172.31.$cidrC.0/22"

# Deploy CloudFormation stack with parameters
aws cloudformation deploy \
  --profile "$profile" \
  --template-file "$fileName" \
  --stack-name "subnets" \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides \
    VPC="$vpc" \
    CIDRBlockA="$cidrA" \
    CIDRBlockB="$cidrB" \
    CIDRBlockC="$cidrC" \
