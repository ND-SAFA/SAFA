import boto3

CLIENT_CACHE = {}
SERVICES = ["sts", "ec2", "ecs", "cloudformation", "efs"]


def get_client(service: str) -> boto3.client:
    """
    Creates client for given service accessing profile.
    :param service: The AWS service.
    :param profile: The profile whose account will be accessed.
    :return: The boto client.
    """
    if service not in SERVICES:
        print(f"Unknown service: {service}")
    service = service.lower()
    if service not in CLIENT_CACHE:
        CLIENT_CACHE[service] = boto3.client(service)
    return CLIENT_CACHE[service]
