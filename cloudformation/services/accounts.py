import os
import re
from typing import Optional, TypedDict

from cloudformation.services.client import get_client


class AccountInfo(TypedDict):
    UserId: str
    Account: str
    Arn: str


ACCOUNT_ID_KEY = "Account"


def get_account_info() -> AccountInfo:
    """
    Returns the account associated with current profile.
    :return:
    """
    profile = os.environ["AWS_PROFILE"]
    if len(profile.strip()) == 0:
        raise Exception("AWS Profile is not set.")
    sts_client = get_client("sts")
    account_info = sts_client.get_caller_identity()
    return account_info


def get_account_id() -> Optional[str]:
    """
    Returns the account id associated with given profile.
    :return: Account ID.
    """
    account_info = get_account_info()
    account_id = account_info[ACCOUNT_ID_KEY]
    return account_id


def extract_account_id(account_info: str) -> Optional[str]:
    """
    Extracts the account ID from the account information text.
    :param account_info: Text representing account info.
    :return: Account ID.
    """
    regex = r"Account: '([0-9]+)'"
    match = re.search(regex, account_info)
    if match:
        return match.group(1)
    else:
        raise Exception(f"Unable to extract account ID: {account_info}")
