#!/bin/bash

fileName=service.yaml

extract_account_id() {
    local text="$1"
    local regex="Account: '([0-9]+)'"

    if [[ $text =~ $regex ]]; then
        accountId="${BASH_REMATCH[1]}"
        echo "$accountId"
    else
        echo "Unable to extract account ID: $text"
        exit 1
    fi
}

echo "Enter profile"
read -e profile

accountInfo=$(aws sts get-caller-identity --profile $profile 2>&1)
accountId=$(extract_account_id "$accountInfo")
echo "Account ID:$accountId"

echo "Service Name:"
read -e serviceName

aws ecs list-clusters --query "clusterArns" --output table --profile "$profile"
echo "Cluster Name:"
read -e clusterName

aws ecs list-task-definitions --output table --profile "$profile"
echo "Task Definition ARN:"
read -e taskDefinitionArn

aws ec2 describe-security-groups --query "SecurityGroups[*].[GroupId,GroupName]" --output table --profile "$profile"
echo "Security Group Ids:"
read -e securityGroupIds

aws ec2 describe-subnets --query "Subnets[*].[SubnetId,AvailabilityZone,Tags[?Key=='Name'].Value | [0]]" --output table --profile "$profile"
echo "Subnet Ids:"
read -e subnetIds

aws elbv2 describe-target-groups --query "TargetGroups[*].[TargetGroupArn,TargetGroupName]" --output table --profile "$profile"
echo "Target Group Arn:"
read -e targetGroupArn

stackName="$clusterName-service"

echo "Stack: $stackName"
echo "Cluster: $clusterName"
echo "Service Name: $serviceName"
echo "Task Definition Arn: $taskDefinitionArn"
echo "Security Groups: $securityGroupIds"
echo "SubnetIds: $subnetIds"
echo "Target Groups: $targetGroupArn"


# aws cloudformation deploy \
#   --profile "$profile" \
#   --template-file "$fileName" \
#   --stack-name "$stackName" \
#   --capabilities CAPABILITY_NAMED_IAM \
#   --parameter-overrides \
#     ClusterName="$clusterName" \
#     ServiceName="$serviceName"
#     TaskDefinitionARN="$taskDefinitionArn" \
#     SecurityGroupIds="$securityGroupIds" \
#     SubnetIds="$subnetIds" \
#     TargetGroupArn="$targetGroupArn"
