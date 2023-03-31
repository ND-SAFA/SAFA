from abc import abstractmethod


class ICloudStorage:
    """
    Defines interface with a cloud storage solution.
    """

    @staticmethod
    @abstractmethod
    def exists(path: str) -> bool:
        """
        Returns whether given path exists in the cloud.
        :param path: The path to file or folder.
        :return: True if path contains file or folder.
        """

    @staticmethod
    @abstractmethod
    def copy(src: str, dest: str) -> None:
        """
        Copies file or directory into destination path.
        :param src: The path to cloud object.
        :param dest: The destination to copy object to in local machine.
        :return: None. Error thrown if failure occurs.
        """
  