import os
import sys

from dotenv import load_dotenv

load_dotenv()
root_path = os.path.expanduser(os.environ["ROOT_PATH"])
sys.path.append(root_path)

from tgen.scripts.toolset.core.main_menu import select_tool
from tgen.scripts.toolset.core.tool_set import ToolSet
from tgen.scripts.toolset.tools.rq_tools import RQ_TOOLS
from tgen.scripts.toolset.tools.s3_tools import S3_TOOLS

TOOLS = S3_TOOLS + RQ_TOOLS
if __name__ == "__main__":
    select_tool(ToolSet(TOOLS), "train", "~/desktop/safa/eval/dronology")
