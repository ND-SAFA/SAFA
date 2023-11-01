from dotenv import load_dotenv

from tgen.scripts.toolset.core.main_menu import select_tool
from tgen.scripts.toolset.core.tool_set import ToolSet


def a(b: str):
    """
    Prints input to screen.
    :param b: The input to print.
    :return: None
    """
    print(b)


TOOLS = [a]
if __name__ == "__main__":
    load_dotenv()
    select_tool(ToolSet(TOOLS))
