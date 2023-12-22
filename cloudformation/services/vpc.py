import boto3

from cloudformation.services.client import get_client


def get_security_groups(profile: str):
    ec2_client = get_client("ec2", profile)
    security_groups = ec2_client.describe_security_groups()['SecurityGroups']
    print("Security Group Ids:")
    for group in security_groups:
        print(f"{group['GroupId']} - {group['GroupName']}")
    security_group_ids = input()
    return security_group_ids


def get_subnet_ids(profile: str):
    subnets = get_client("ec2", profile).describe_subnets()['Subnets']
    print("Subnet Ids:")
    for subnet in subnets:
        print(f"{subnet['SubnetId']} - {subnet['AvailabilityZone']} - {subnet.get('Tags', [{'Value': ''}])[0]['Value']}")
    subnet_ids = input()
    return subnet_ids


def get_target_groups(profile: str):
    elbv2_client = boto3.client('elbv2', profile_name=profile)
    target_groups = elbv2_client.describe_target_groups()['TargetGroups']
    print("Target Group Arn:")
    for target_group in target_groups:
        print(f"{target_group['TargetGroupArn']} - {target_group['TargetGroupName']}")
    target_group_arn = input()
    return target_group_arn
