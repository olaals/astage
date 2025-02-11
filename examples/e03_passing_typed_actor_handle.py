import asyncio
from dataclasses import dataclass
from astage import Actor, ActorHandle, handler

@dataclass
class IncrementMessage:
    value: int

CounterActorMsg = IncrementMessage

class CounterActor(Actor[CounterActorMsg]):
    def __init__(self):
        super().__init__()
        self.count = 0

    @handler
    async def increment(self, message: IncrementMessage):
        self.count += message.value
        print(f"Count is now: {self.count}")

# For the tell and ask methods to provide type hints,
# the actor's message types must be defined on the handle
async def process_actor(
        handle: ActorHandle[CounterActorMsg] # Type hint for the actor handle
    ):
    """Async function that takes an ActorHandle and interacts with the actor."""
    await handle.tell(IncrementMessage(3))

async def main():
    actor = CounterActor()
    handle = await actor.start()

    await process_actor(handle)

if __name__ == "__main__":
    asyncio.run(main())

