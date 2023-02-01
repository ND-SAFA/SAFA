def overrides(interface_class):
    """
    Decorator for checking that method is actually overriding a parent class.
    :param interface_class: The class that is being overriden.
    :return: Wrapped class.
    """

    def overrider(method):
        assert (method.__name__ in dir(interface_class))
        return method

    return overrider
