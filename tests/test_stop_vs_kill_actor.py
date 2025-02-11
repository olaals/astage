import asyncio
import pytest
from astage import Actor, handler

class SlowActor(Actor):
    def __init__(self):
        super().__init__()
        self.finished_processing = False

    @handler
    async def long_task(self, _: int) -> str:
        await asyncio.sleep(0.5)
        self.finished_processing = True
        return "done"

@pytest.mark.asyncio
async def test_stop_allows_current_task_to_finish():
    """
    When stop() is used, the actor should complete the currently processing task.
    """
    actor = SlowActor()
    handle = await actor.start()

    ask_task = asyncio.create_task(handle.ask(1))
    await asyncio.sleep(0.1)
    handle.stop()
    result = await asyncio.wait_for(ask_task, timeout=1.0)
    assert result == "done"
    assert actor.finished_processing is True

@pytest.mark.asyncio
async def test_kill_interrupts_current_task():
    """
    When kill() is used, the actor should be terminated immediately,
    interrupting any ongoing task.
    """
    actor = SlowActor()
    handle = await actor.start()
    ask_task = asyncio.create_task(handle.ask(1))
    await asyncio.sleep(0.1)
    await handle.kill() 
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(ask_task, timeout=0.2)
    assert actor.finished_processing is False
