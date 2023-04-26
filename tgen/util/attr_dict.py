class AttrDict(dict):
    """
    Allows attribute access using . notation
    """

    def __getattr__(self, item):
        if item in self:
            return self[item]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")
