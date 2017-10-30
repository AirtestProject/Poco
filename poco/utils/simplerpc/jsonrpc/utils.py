""" Utility functions for package."""
import datetime
import decimal
import inspect
import json
from abc import ABCMeta, abstractmethod

from . import six


class JSONSerializable(six.with_metaclass(ABCMeta, object)):

    """ Common functionality for json serializable objects."""

    serialize = staticmethod(json.dumps)
    deserialize = staticmethod(json.loads)

    @abstractmethod
    def json(self):
        raise NotImplementedError()

    @classmethod
    def from_json(cls, json_str):
        data = cls.deserialize(json_str)

        if not isinstance(data, dict):
            raise ValueError("data should be dict")

        return cls(**data)


class DatetimeDecimalEncoder(json.JSONEncoder):

    """ Encoder for datetime and decimal serialization.

    Usage: json.dumps(object, cls=DatetimeDecimalEncoder)
    NOTE: _iterencode does not work

    """

    def default(self, o):
        """ Encode JSON.

        :return str: A JSON encoded string

        """
        if isinstance(o, decimal.Decimal):
            return float(o)

        if isinstance(o, (datetime.datetime, datetime.date)):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


def is_invalid_params(func, *args, **kwargs):
    """ Check, whether function 'func' accepts parameters 'args', 'kwargs'.

    NOTE: Method is called after funct(*args, **kwargs) generated TypeError,
    it is aimed to destinguish TypeError because of invalid parameters from
    TypeError from inside the function.

    .. versionadded: 1.9.0

    """
    # For builtin functions inspect.getargspec(funct) return error. If builtin
    # function generates TypeError, it is because of wrong parameters.
    if not inspect.isfunction(func):
        return True

    funcargs, varargs, varkwargs, defaults = inspect.getargspec(func)
    if defaults:
        funcargs = funcargs[:-len(defaults)]

    if args and len(args) != len(funcargs):
            return True
    if kwargs and set(kwargs.keys()) != set(funcargs):
        return True

    if not args and not kwargs and funcargs:
        return True

    return False
