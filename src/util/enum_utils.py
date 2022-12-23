SEP_SYM = "_"


def get_enum_from_name(enum_class, enum_name):
    enum_name = enum_name.upper()
    if SEP_SYM not in enum_name:
        for e in enum_class:
            name_removed_sep = "".join(e.name.split(SEP_SYM))
            if name_removed_sep == enum_name:
                return e
    return enum_class[enum_name]
