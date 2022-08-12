from abc import abstractmethod


class AbstractArgBuilder:

    @abstractmethod
    def build(self):
        """
        Responsible for building Job Args
        :return: the Job Args
        """
        pass
