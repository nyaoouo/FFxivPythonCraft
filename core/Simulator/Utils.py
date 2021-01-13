def CallOrVar(prop, *args):
    if callable(prop):
        return prop(*args)
    else:
        return prop
