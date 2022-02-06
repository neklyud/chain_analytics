from inspect import ismethod, getmembers
from typing import Callable


def decorate(object_for_update, decorator: Callable):
    methods = [i_method for i_method in getmembers(object_for_update, ismethod) if not i_method[0].startswith("__")]
    list(map(lambda x: setattr(object_for_update, x[0], decorator(x[1])), methods))
    return object_for_update
