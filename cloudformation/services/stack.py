from typing import Dict

from botocore.exceptions import ClientError

from cloudformation.services.client import get_client
from cloudformation.services.store import CFArgs
from cloudformation.services.util import print_params
from tgen.common.util.file_util import FileUtil

file2stack = {
    "td.yaml": "task-definitions",
    "policies.yaml": "managed-policies"
}


def stack_exists(cloudformation_client, stack_name):
    try:
        # Try to describe the stack
        cloudformation_client.describe_stacks(StackName=stack_name)
        return True
    except ClientError as e:
        # If the error code is 'ValidationError', the stack doesn't exist
        if e.response["Error"]["Code"] == "ValidationError":
            return False
        else:
            # Handle other errors
            raise


def create_stack(args: CFArgs, params: Dict):
    stack_name = file2stack[args["file_name"]]
    file_path = args["file_path"]

    print_params(params, stack_name=stack_name, file_path=file_path)
    if "n" in input("Confirm?(y/n)"):
        return

    cloudformation_client = get_client("cloudformation")
    params = [{"ParameterKey": k, "ParameterValue": str(v)} for k, v in params.items()]

    # Check if the stack exists
    if stack_exists(cloudformation_client, stack_name):
        # Update the stack
        response = cloudformation_client.update_stack(
            StackName=stack_name,
            TemplateBody=FileUtil.read_file(file_path),
            Capabilities=['CAPABILITY_NAMED_IAM'],
            Parameters=params
        )
        print(response)
    else:
        # Create the stack
        response = cloudformation_client.create_stack(
            StackName=stack_name,
            TemplateBody=FileUtil.read_file(file_path),
            Capabilities=['CAPABILITY_NAMED_IAM'],
            Parameters=params
        )
        print(response)
