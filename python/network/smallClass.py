# basic python classes to test sending data over json

import json
import importlib

class OuterClass(object):
    """docstring for OuterClass."""
    def __init__(self):
        self.insides = 42
        # self.insides = InnerClass(42)

    def __str__(self):
        return "Number: {}".format(self.insides)


class InnerClass(object):
    """docstring for InnerClass."""
    def __init__(self, arg):
        self.num = arg

    def __str__(self):
        return str(self.num)


# https://medium.com/python-pandemonium/json-the-python-way-91aac95d4041
def obj_to_dict(obj):
    obj_dict = {
        "__class__" : obj.__class__.__name__,
        "__module__" : obj.__module__
    }

    obj_dict.update(obj.__dict__)

    return obj_dict

def dict_to_obj(d):
    if "__class__" in d:
        class_name = d.pop("__class__")
        module_name = d.pop("__module__")
        module = importlib.import_module(module_name)
        class_ = getattr(module, class_name)
        obj = class_(**d)
    else:
        obj = d
    return obj
