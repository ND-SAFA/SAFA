from tqdm import tqdm


def the_tqdm(*args: object, **kwargs: object) -> tqdm:
    """
    Decorates tqdm with log capture to store logs.
    :param args: Positional arguments to tqdm.
    :param kwargs: Keyword arguments to tqdm.
    :return: Constructed tqdm iterable.
    """
    return tqdm(*args, **kwargs)
