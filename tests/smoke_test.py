import asyncio
import sys

def test_import():
    """Test that package can be imported."""
    import astage
    from astage import Actor, handler, actor_handle
    print("Import successful")

def test_actor_basic_functionality():
    """Basic sanity test for an actor instance."""
    from astage import Actor, handler
    from dataclasses import dataclass

    @dataclass
    class Message:
        value: int

    class SimpleActor(Actor):
        def __init__(self):
            super().__init__()
            self.state = 0

        @handler
        async def increment(self, message: Message):
            self.state += message.value
            return f"Incremented by {message.value}, new state: {self.state}"

    async def run_test():
        actor = SimpleActor()
        handle = await actor.start()
        
        response = await handle.ask(Message(5))
        assert response == "Incremented by 5, new state: 5"

        handle.stop()
        await asyncio.sleep(0.1)  # Allow cancellation to complete
        print("Actor functionality verified")

    asyncio.run(run_test())

if __name__ == "__main__":
    try:
        test_import()
        test_actor_basic_functionality()
        print("Smoke test passed")
    except Exception as e:
        print(f"Smoke test failed: {e}", file=sys.stderr)
        sys.exit(1)
