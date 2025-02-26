import asyncio
from typing import Any, Callable
from astage._internal.internal import AskMessage

class ActorHandle[T]:
    def __init__(
            self, 
            msg_queue: asyncio.Queue[T | AskMessage[T]], 
            task: asyncio.Task[None],
            stop_func: Callable[[], None]
    ):
        self.msg_queue = msg_queue
        self.task = task
        self.stop_func = stop_func

    async def tell(self, message: T) -> None:
        await self.msg_queue.put(message)

    async def ask(self, message: T) -> Any:
        response_queue: asyncio.Queue[Any] = asyncio.Queue()
        ask_message = AskMessage[T](message, response_queue)
        await self.msg_queue.put(ask_message)
        response = await response_queue.get()
        return response

    def __del__(self) -> None:
        pass

    async def kill(self) -> None:
        self.task.cancel()
        try:
            await self.task
        except asyncio.CancelledError:
            pass

    def stop(self) -> None:
        self.stop_func()
