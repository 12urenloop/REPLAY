from app.core.clock import Clock
from app.core.config import settings

state = {}


async def load_state():
    global state
    clock = Clock()
    await clock.reset(settings.START_TIME)
    state["clock"] = clock

    state["connections"] = []
