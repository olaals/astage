import asyncio
from dataclasses import dataclass
from astage import Actor, handler

@dataclass
class IncrementMessage:
    value: int

@dataclass
class EchoMessage:
    text: str

class CounterActor(Actor):
    def __init__(self):
        super().__init__()
        self.count = 0

    @handler
    async def increment(self, message: IncrementMessage):
        self.count += message.value
        print(f"Count is now: {self.count}")

    @handler
    async def echo(self, message: EchoMessage):
        return f"Echo: {message.text}"

async def main():
    actor = CounterActor()

    # start the actor which will run in a non-blocking asyncio.Task
    handle = await actor.start()

    # tell: send a message without waiting for a response
    await handle.tell(IncrementMessage(5))
    # Expected: Count is now: 5
    await handle.tell(IncrementMessage(5))
    # Expected: Count is now: 10

    # ask: send a message and wait for a response
    result = await handle.ask(EchoMessage("Hello, Actor!"))
    print(result)  # Expected: Echo: Hello, Actor!

    # it is possible to use tell and ask on all @handler methods
    # the return value of the ask will be the return value of the handler
    response = await handle.ask(IncrementMessage(5))
    print(response)  # Expected: None

if __name__ == "__main__":
    asyncio.run(main())
