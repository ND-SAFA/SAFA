from dotenv import load_dotenv

from tgen.scripts.toolset.core.main_menu import select_tool
from tgen.scripts.toolset.core.tool_set import ToolSet
from tgen.scripts.toolset.tools.rq_tools import RQ_TOOLS
from tgen.scripts.toolset.tools.s3_tools import S3_TOOLS

TOOLS = S3_TOOLS + RQ_TOOLS
if __name__ == "__main__":
    load_dotenv()
    select_tool(ToolSet(TOOLS))
