from cloudformation.services.client import get_client

from tgen.common.constants.deliminator_constants import NEW_LINE


def get_cluster_name() -> str:
    """
    Shows user available clusters and prompts user to select one.
    :return:
    """
    ecs_client = get_client("ecs")
    clusters = ecs_client.list_clusters()['clusterArns']
    prompt = f"{NEW_LINE.join(clusters)}{NEW_LINE}Cluster Name:"
    cluster_name = input(prompt)
    return cluster_name


def get_task_definitions(profile: str) -> str:
    """
    Prompts user to select a task definition available in profile.
    :param profile: The profile to search task definitions in.
    :return: ARN.
    """
    ecs_client = get_client("ecs", profile)
    task_definitions = ecs_client.list_task_definitions()['taskDefinitionArns']
    prompt = f"{NEW_LINE.join(task_definitions)}{NEW_LINE}Task Definition ARNs:"
    task_definition_arn = input(prompt)
    return task_definition_arn
