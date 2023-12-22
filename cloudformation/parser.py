import os

from cloudformation.services.accounts import get_account_id
from cloudformation.services.file_loader import collect_user_inputs
from cloudformation.services.file_system import list_efs_by_account
from cloudformation.services.service import get_file_path
from cloudformation.services.stack import create_stack
from cloudformation.services.store import CFArgs

printables = {
    "genfilesystemid": list_efs_by_account
}


def parse():
    store: CFArgs = {}

    store["file_path"] = get_file_path(store)
    if "profile" not in store:
        store["profile"] = input("Select profile:")

    os.environ["AWS_PROFILE"] = store["profile"]
    store["accountid"] = get_account_id()

    user_inputs = collect_user_inputs(store["file_path"], store, printables)
    create_stack(store, user_inputs)


if __name__ == "__main__":
    parse()
