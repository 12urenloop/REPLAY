import time
from typing import List

from fastapi import WebSocket


class Clock:
    start: float
    real_start: float

    async def reset(self, start_time: float, connections: List[WebSocket] = []):
        self.start = start_time
        self.real_start = time.time()
        try:  # TODO: could be cleaner?
            for connection in connections:
                await connection.close()
        finally:
            pass

    def get_time(self) -> float:
        return time.time() - self.real_start + self.start
