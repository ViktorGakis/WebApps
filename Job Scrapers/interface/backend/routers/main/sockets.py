from logging import Logger

from fastapi import WebSocket, WebSocketDisconnect

from ...config import APISettings, get_api_settings
from ...logger import logdef
from ..css_tracker import (
    ConnectionManager,
    CssTracker,
    connect_block,
    start_block,
    stop_block,
)
from . import router

log: Logger = logdef(__name__)

config: APISettings = get_api_settings()

manager: ConnectionManager = ConnectionManager()
css_tracker: CssTracker | None = None

@router.websocket("/ws/css_tracker/")
async def ws_css(websocket: WebSocket) -> None:
    global css_tracker, manager
    await manager.connect(websocket)
    try:
        while True:
            data: str = await websocket.receive_text()
            await manager.broadcast(data)
            log.debug("received: %s", data)

            if "[connect]:" in data.lower():
                css_tracker, manager = await connect_block(css_tracker, manager)

            elif "[start]:" in data.lower():
                css_tracker, manager = await start_block(css_tracker, manager)

            elif "[stop]:" in data.lower() or "[closed]" in data.lower():
                css_tracker, manager = await stop_block(css_tracker, manager)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Disconnected")

