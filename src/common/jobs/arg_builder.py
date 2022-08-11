from abc import abstractmethod


class ArgBuilder:

    @abstractmethod
    def build(self):
        """
        Responsible for building Job Args
        :return: the Job Args
        """
        pass
