from typing import Callable
import asyncio
from typing import Any, Type

from astage._internal.internal import get_type_of_second_argument, AskMessage
from astage.actor_handle import ActorHandle

class Actor[T]:
    registry: dict[Type[Any], Callable[[Any, Any], Any]]

    def __init__(self, max_queue_size: int = 0):
        self.msg_queue: asyncio.Queue[T | AskMessage[T]] = asyncio.Queue(max_queue_size)
        self.is_running = False
        self.task: asyncio.Task[Any] | None = None

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Ensure each subclass has its own registry."""
        super().__init_subclass__(**kwargs)
        cls.registry = {}

        # Register any methods that have been marked for registration
        for name, func in cls.__dict__.items():
            if getattr(func, "_register_astage_handler", False):
                second_arg_type = get_type_of_second_argument(func)
                if second_arg_type is None:
                    raise ValueError(f"Function {name} must have a second parameter with a type annotation")
                cls.registry[second_arg_type] = func

    async def run(self) -> None:
        try:
            while True:
                message = await self.msg_queue.get()
                msg_type = type(message)
                if isinstance(message, AskMessage):
                    ask_message = message
                    type_ask_msg = type(ask_message.message)
                    func = self.registry[type_ask_msg]
                    result = await func(self, ask_message.message)
                    ask_message.response_queue.put_nowait(result)
                else:
                    if msg_type in self.registry:
                        func = self.registry[msg_type]
                        result = await func(self, message)
                    else:
                        raise ValueError(f"No handler for message {message}, {msg_type}, {self.registry}")
        except asyncio.CancelledError:
            pass

    async def start(self) -> ActorHandle[T]:
        if self.is_running:
            raise RuntimeError("Actor is already running")
        self.is_running = True
        task = asyncio.create_task(self.run())
        self.task = task
        return ActorHandle[T](self.msg_queue, task)

    def __del__(self) -> None:
        if self.task is not None:
            try:
                self.task.cancel()
            except RuntimeError:
                pass
