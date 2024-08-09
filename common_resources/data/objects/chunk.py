from typing import Optional

from common_resources.tools.constants.symbol_constants import UNDERSCORE
from common_resources.tools.util.str_util import StrUtil


class Chunk:

    @staticmethod
    def get_chunk_num(chunk_id: str, base_id: str) -> Optional[int]:
        """
        Gets the chunk number from the id.
        :param chunk_id: The id of the chunk.
        :param base_id: The id of the full artifact.
        :return: The number of the chunk.
        """
        try:
            chunk_num = int(StrUtil.remove_substrings(chunk_id, [base_id, UNDERSCORE]))
            return chunk_num
        except ValueError:
            raise NameError("Chunk does not exist")

    @staticmethod
    def get_chunk_id(orig_id: str, chunk_num: int) -> str:
        """
        Creates an id for an artifact chunk.
        :param orig_id: The id of the whole artifact.
        :param chunk_num: The number of the chunk.
        :return: An id for an artifact chunk.
        """
        return f"{orig_id}{UNDERSCORE}{chunk_num}"

    @staticmethod
    def get_base_id(c_id: str) -> str:
        """
        Gets the id of the whole artifact.
        :param c_id: The id of the artifact/chunk.
        :return: The id of the whole artifact.
        """
        split_id = c_id.split(UNDERSCORE)
        if len(split_id) > 1:
            orig_id = UNDERSCORE.join(split_id[:-1])
            return orig_id
        raise NameError("Unknown artifact")
