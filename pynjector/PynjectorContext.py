import inspect
import sys

from pynjector.PynjectorMain import PynjectorMain


def _camel_to_snake(camel: str):
    res = ""
    for char in camel:
        if char.isupper():
            res += '_' + char.lower()
        else:
            res += char
    return res[1:]


class PynjectorContextException(RuntimeError):
    pass


class PynjectorContext:

    @staticmethod
    def _get_dependencies(smth):
        if isinstance(smth, type):
            return inspect.getfullargspec(smth.__init__).args[1:]
        elif inspect.isfunction(smth):
            return inspect.getfullargspec(smth).args

    def __init__(self):
        self._sources = {}
        self._objects = {}

    def get(self, name):
        return self._objects.get(name)

    def _get_args_for_func(self, function, has_self=False):
        trim = 1 if has_self else 0
        required_args = inspect.getfullargspec(function).args[trim:]
        args = [self._objects[arg] for arg in required_args]
        return args

    def _singleton_type(self, typ: type, name: str):
        if name is None:
            name = _camel_to_snake(typ.__name__)
        if name in self._objects:
            raise PynjectorContextException(f"Name collision: {name}")

        args = self._get_args_for_func(typ.__init__, has_self=True)
        new_object = typ(*args)
        self._objects[name] = new_object
        if isinstance(new_object, PynjectorMain):
            new_object.main(sys.argv)

    def _singleton_function(self, function, name):
        if name is None:
            name = function.__name__
        if name in self._objects:
            raise PynjectorContextException(f"Name collision: {name}")

        args = self._get_args_for_func(function, has_self=False)
        new_object = function(*args)
        self._objects[name] = new_object

    def _create_singleton(self, smth, name):
        if isinstance(smth, type):
            self._singleton_type(smth, name)
        elif inspect.isfunction(smth):
            self._singleton_function(smth, name)

    def singleton(self, name: str = None):

        def wrapper(smth):
            nonlocal name
            if name is None:
                if isinstance(smth, type):
                    name = _camel_to_snake(smth.__name__)
                elif inspect.isfunction(smth):
                    name = smth.__name__
                else:
                    raise NotImplementedError(f"{type(smth)} is not supported for singleton()")
            self._sources[name] = smth
            return smth

        return wrapper

    def _init(self, name=None):
        if name is None:
            name = list(self._sources.keys())[0]

        if name in self._objects:
            return

        source = self._sources.get(name)

        if source is None:
            raise PynjectorContextException(f"Couldn't inject `{name}`: no source for init")

        for dep in self._get_dependencies(source):
            self._init(dep)

        self._create_singleton(source, name)

    def init(self):
        for source in self._sources:
            self._init(source)
