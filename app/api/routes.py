from datetime import datetime
from fastapi import APIRouter, WebSocket
import json
import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.clock import Clock
from app.core.state import state
from typing import Annotated
from fastapi import Depends

from app.core.db import get_async_session

router = APIRouter(tags=["api"])


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.websocket("/{path}")
async def ronny(path: str, websocket: WebSocket):
    await websocket.accept()
    clock: Clock = state["clock"]
    state["connections"].append(websocket)

    t = await websocket.receive()  # TODO: receive_json() did not work?
    last_id = json.loads(t["text"])["lastId"]

    with open(f"dumps/{path}.json") as f:
        detections = json.loads(f.read())["detections"]

    before_start = []
    for i in range(len(detections) - 1):
        if detections[i]["detection_timestamp"] > clock.start:
            break

        if detections[i]["id"] >= last_id:
            before_start.append(detections[i])

    if len(before_start) > 0:
        await websocket.send_json(before_start)

    for i in range(len(detections) - 1):
        if detections[i]["id"] >= last_id:
            timestamp = detections[i]["detection_timestamp"]

            while timestamp > clock.get_time():
                await asyncio.sleep(timestamp - clock.get_time())

            await websocket.send_json([detections[i]])


@router.post("/reset")
async def reset(session: SessionDep, time: datetime):
    clock: Clock = state["clock"]
    connections = state["connections"]

    sql = text(f"DELETE FROM detection WHERE timestamp > '{time}'")
    await session.execute(sql)
    sql = text(f"DELETE FROM lap WHERE timestamp > '{time}'")
    await session.execute(sql)
    await session.commit()

    await clock.reset(time.timestamp(), connections)
    state["connections"] = []
