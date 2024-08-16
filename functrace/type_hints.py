import collections
import typing

__all__ = ('CallableType', 'ArgsType', 'KwargsType')

CallableType = collections.abc.Callable[..., typing.Any]
ArgsType = tuple[typing.Any, ...]
KwargsType = dict[str, typing.Any]
