from transformers import Trainer

from results.base_results import BaseResults


# TODO
class LMTrainer(Trainer):

    def __init__(self, args, model, dataset):
        pass

    def train(self, **kwargs) -> BaseResults:
        pass

    def predict(self) -> BaseResults:
        pass
