# Curry a given function.
# If the definition uses *args, specify the amount given in a specific case
def curry(f: callable, arity=None):
    if arity is None:
        arity = f.__code__.co_argcount
    elif arity < 0:
        raise Exception("negative arity")
    elif arity < f.__code__.co_argcount:
        raise Exception("specified arity is lesser than required")

    if arity == 0:
        return lambda: f()

    def inner(*args):
        if len(args) >= arity:
            return f(*args)

        return lambda arg: inner(*args, arg)

    return lambda arg: inner(arg)


# Uncurry a curried function
def uncurry(f: callable):
    def inner(*args):
        value = f

        for arg in args:
            try:
                value = value(arg)
            except Exception:
                raise Exception("incorrect amount of arguments provided")

        return value

    return inner
