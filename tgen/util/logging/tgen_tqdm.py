from tqdm import tqdm

from tgen.util.logging.log_capture import log_capture


def tgen_tqdm(*args, **kwargs) -> tqdm:
    """
    Decorates tqdm with log capture to store logs.
    :param args: Positional arguments to tqdm.
    :param kwargs: Keyword arguments to tqdm.
    :return: Constructed tqdm iterable.
    """
    return tqdm(*args, **kwargs, file=log_capture)
