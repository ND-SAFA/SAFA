from cloudformation.services.client import get_client
from cloudformation.services.store import CFArgs


def list_efs_by_account(store: CFArgs):
    """
    Prints file systems associated with account.
    :param account_id:
    :return:
    """
    efs_client = get_client('efs')
    response = efs_client.describe_file_systems()
    for fs in response['FileSystems']:
        f_name = fs["Name"]
        f_id = fs["FileSystemId"]
        print(f"{f_name}: {f_id}")
