# astage
[![PyPI version](https://badge.fury.io/py/astage.svg)](https://badge.fury.io/py/astage)
![Python versions](https://img.shields.io/pypi/pyversions/astage)

Initial MVP for Async actor model library for Python

Currently zero external dependencies outside of the Python standard library.

Features:
- Concurrent actor model with asyncio
- Maps message types to handler methods on the actor
- Type hints on ask and tell methods on handler
- Tell and ask methods for sending messages to the actor
- Allows setting backpressure on the actor mailbox

## Installation
The library is available on PyPI and can be installed with for example pip or uv.

With pip:
```bash
pip install astage
```
or uv
```bash
uv add astage
```

## Example 
```python
import asyncio
from dataclasses import dataclass
from astage import Actor, handler

@dataclass
class IncrementMessage:
    value: int

@dataclass
class EchoMessage:
    text: str

CounterActorMsg = IncrementMessage | EchoMessage

# The type hints to the actor class enables type hints on the handlers ask and tell methods
# All message types the actor has handlers for should be specified
class CounterActor(Actor[CounterActorMsg]):
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
```

The message types also works with Pydantic classes, although Pydantic is not a dependency of the library.

```python
import asyncio
from pydantic import BaseModel
from astage import Actor, handler

class IncrementMessage(BaseModel):
    value: int

class CounterActor(Actor[IncrementMessage]):
    def __init__(self):
        super().__init__()
        self.count = 0

    @handler
    async def increment(self, message: IncrementMessage):
        self.count += message.value
        return f"Count is now {self.count}"

async def main():
    actor = CounterActor()
    handle = await actor.start()
    
    # create a message using a Pydantic class
    pydantic_msg = IncrementMessage(value=10)

    # ask: send a message and await a response
    result = await handle.ask(pydantic_msg)
    print(result)  # Expected: Count is now 10

if __name__ == "__main__":
    asyncio.run(main())
```
