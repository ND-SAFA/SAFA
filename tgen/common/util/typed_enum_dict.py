import sys

from typing import _type_check, _TypedDictMeta, TypedDict

from tgen.common.util.enum_util import EnumUtil, EnumDict


class _TypedEnumDictMeta(_TypedDictMeta):

    def __new__(cls, name, bases, ns, keys):
        """Create new typed dict class object based on the EnumDict.

        This method is called when TypedEnumDict is subclassed,
        or when TypedEnumDict is instantiated. This way
        TypedEnumDict supports all three syntax forms described in its docstring.
        Subclasses and instances of TypedEnumDict return EnumDict.
        """
        annotations = ns['__annotations__']
        updated_annotations = {}
        for key, val in annotations.items():
            try:
                enum_key = keys[key.upper()]
                updated_annotations[enum_key] = val
            except KeyError:
                continue
        annotations.update(updated_annotations)
        tp_dict = _TypedDictMeta.__new__(cls, name, (), ns, False)
        etp_dict = type.__new__(_TypedEnumDictMeta, name, (EnumDict,), ns)
        for k, v in vars(tp_dict).items():
            try:
                setattr(etp_dict, k, v)
            except AttributeError:
                continue
        return etp_dict

    __call__ = EnumDict  # static method


def TypedEnumDict(typename, fields=None, /, *, total=False, **kwargs):
    """
    TypedDict creates an EnumDict type that expects all of its
    instances to have a certain set of keys, where each key is
    associated with a value of a consistent type.
    """
    if fields is None:
        fields = kwargs
    elif kwargs:
        raise TypeError("TypedEnumDict takes either a dict or keyword arguments,"
                        " but not both")

    ns = {'__annotations__': dict(fields)}
    try:
        # Setting correct module is necessary to make typed dict classes pickleable.
        ns['__module__'] = sys._getframe(1).f_globals.get('__name__', '__main__')
    except (AttributeError, ValueError):
        pass
    return _TypedEnumDictMeta(typename, (), ns, total=total)


_TypedEnumDict = type.__new__(_TypedEnumDictMeta, 'TypedEnumDict', (), {})
TypedEnumDict.__mro_entries__ = lambda bases: (_TypedEnumDict,)
