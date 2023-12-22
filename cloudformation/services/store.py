from typing import Optional, TypedDict


class CFArgs(TypedDict):
    accountid: str
    file_name: Optional[str]
    file_path: Optional[str]
    profile: Optional[str]
