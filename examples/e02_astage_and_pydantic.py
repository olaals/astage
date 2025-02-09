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
