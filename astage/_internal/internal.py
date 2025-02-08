from dataclasses import dataclass
import asyncio
from typing import Any, Callable, Type
import inspect

@dataclass
class AskMessage[T]:
    message: T
    response_queue: asyncio.Queue[Any]

def get_type_of_second_argument(func: Callable[..., Any]) -> Type[Any] | None:
    sig = inspect.signature(func)
    params = list(sig.parameters.values())
    if len(params) < 2:
        raise ValueError("Function must have at least two parameters.")
    second_param = params[1]
    if second_param.annotation is inspect.Parameter.empty:
        raise ValueError("Second parameter does not have a type annotation.")
    second_param_type: Type[Any] = second_param.annotation
    return second_param_type

