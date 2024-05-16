def overrides(interface_class):
    """
    Decorator for checking that method is actually overriding a parent class.
    :param interface_class: The class that is being overriden.
    :return: Wrapped class.
    """

    def overrider(method):
        """
        Asserts that method being overridden is contained in parent class.
        :param method: The method to check existence for.
        :return: Method.
        """
        method_name = method.__name__
        assert (method_name in dir(interface_class)), f"{interface_class} does not have method: {method_name}"
        return method

    return overrider
