import os

from constants.constants import IS_TEST, MNT_DIR


class SafaStorage:
    """
    Contains utility methods for dealing with the current filesystem.
    """

    @staticmethod
    def save_to_file(content: str, output_file_path: str):
        """
        Soon to be mock function for saving files to storage but using the filesystem instead.
        :param content: The content of the file to create.
        :param output_file_path: The path to save the file to.
        """
        with SafaStorage.safe_open_w(output_file_path) as file:
            file.write(content)

    @staticmethod
    def safe_open_w(path):
        SafaStorage.create_dir(path)
        return open(path, 'w')

    @staticmethod
    def create_dir(dir_path: str):
        if not os.path.exists(os.path.dirname(dir_path)):
            os.makedirs(os.path.dirname(dir_path))

    @staticmethod
    def add_mount_directory(target_path: str = ''):
        """
        Adds mounting directory to given target path.
        :param target_path: The path to add mount directory to.
        """
        if MNT_DIR == "" and not IS_TEST:
            raise Exception("Mounting directory is undefined.")
        return os.path.join(MNT_DIR, target_path) if not IS_TEST else target_path

    @staticmethod
    def remove_mount_directory(target_path: str):
        """
        Removes the mount directory in output path if in development mode.
        :param target_path: Path to remove mount directory if in dev mode.
        """
        return target_path.replace(MNT_DIR + "/", "") if not IS_TEST else target_path
