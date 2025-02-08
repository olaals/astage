import pytest
import asyncio
from astage import Actor, handler
from pydantic import BaseModel


class Message(BaseModel):
    value: int


class StringMessage(BaseModel):
    text: str


class ActorUnderTest(Actor):
    def __init__(self):
        super().__init__()
        self.state = 0

    @handler
    async def increment(self, message: Message):
        self.state += message.value
        return f"Incremented by {message.value}, new state: {self.state}"

    @handler
    async def echo(self, message: StringMessage):
        return f"Echo: {message.text}"


@pytest.fixture
async def actor_handle():
    actor = ActorUnderTest()
    handle = await actor.start()
    yield handle
    handle.stop()
    await asyncio.sleep(0.1)  # Allow time for cancellation


@pytest.mark.asyncio
async def test_actor_can_receive_messages(actor_handle):
    response = await actor_handle.ask(Message(value=5))
    assert response == "Incremented by 5, new state: 5"

    response = await actor_handle.ask(Message(value=10))
    assert response == "Incremented by 10, new state: 15"


@pytest.mark.asyncio
async def test_actor_echo(actor_handle):
    response = await actor_handle.ask(StringMessage(text="Hello"))
    assert response == "Echo: Hello"


@pytest.mark.asyncio
async def test_tell_does_not_return(actor_handle):
    await actor_handle.tell(Message(value=5))
    await asyncio.sleep(0.1)  # Allow time for processing

    response = await actor_handle.ask(Message(value=0))  # Get current state
    assert response == "Incremented by 0, new state: 5"
