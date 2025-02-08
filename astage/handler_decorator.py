from typing import Callable
from typing import Any
from typing import TypeVar, Awaitable

from astage.actor import Actor

ActorType = TypeVar("ActorType", bound="Actor[Any]")
R = TypeVar("R")

def handler(func: Callable[[ActorType, Any], Awaitable[R]]) -> Callable[[ActorType, Any], Awaitable[R]]:
    """Decorator to mark functions for later registration."""
    func._register_astage_handler = True  # type: ignore[attr-defined]
    return func
