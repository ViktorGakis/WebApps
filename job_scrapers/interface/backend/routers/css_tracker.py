import asyncio
from logging import Logger
from pathlib import Path
from typing import List

from fastapi import WebSocket

from ..config import APISettings, get_api_settings
from ..logger import logdef

log: Logger = logdef(__name__)

config: APISettings = get_api_settings()


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket) -> None:
        await websocket.send_text(message)

    async def broadcast(self, message: str) -> None:
        for connection in self.active_connections:
            await connection.send_text(message)


class CssTracker:
    """Tracks changes in the size of the css file and emits message through the connection manager to the socket"""

    switch: bool = False
    path_css: Path = config.BASE_DIR / Path("static/css/jobs.css")
    path_js: Path = config.BASE_DIR / Path("static/scripts/jobs/script.js")

    def __init__(self, manager: ConnectionManager, timeout: float = 1) -> None:
        self.manager: ConnectionManager = manager
        self.timeout: float = timeout

    async def fileCheck(self) -> None:
        mtime0: List[float] = [self.path_css.stat().st_mtime, self.path_js.stat().st_mtime]
        await asyncio.sleep(self.timeout)
        mtime: List[float] = [self.path_css.stat().st_mtime, self.path_js.stat().st_mtime]
        if mtime0 != mtime:
            await self.manager.broadcast("[update]: css")

    async def start(self) -> None:
        if not self.switch:
            self.switch = True
            log.debug("Css tracker started!")
            while self.switch:
                await self.fileCheck()
            log.debug("Css tracker stopped!")

    async def stop(self) -> None:
        if self.switch:
            self.switch = False


# socket blocks
async def connect_block(
    css_tracker: CssTracker | None, manager: ConnectionManager
) -> tuple[CssTracker | None, ConnectionManager]:
    # log.info("ENTERED CONNECT")
    if isinstance(css_tracker, CssTracker):
        await manager.broadcast("CssTracker: ALREADY INSTANTIATED!")
    elif css_tracker is None:
        css_tracker = CssTracker(manager, timeout=0.1)
        await manager.broadcast("CssTracker: INSTANTIATED!")
    return css_tracker, manager

async def start_block(
    css_tracker: CssTracker | None, manager: ConnectionManager
) -> tuple[CssTracker | None, ConnectionManager]:
    # log.info("ENTERED START")
    if not isinstance(css_tracker, CssTracker):
        await manager.broadcast("CssTracker: IS NOT INSTANTIATED!")
    elif css_tracker.switch:
        await manager.broadcast("CssTracker: ALREADY STARTED!")
    else:
        loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        loop.run_in_executor(None, lambda: asyncio.run(css_tracker.start()))
        await manager.broadcast("CssTracker: STARTED!")
    return css_tracker, manager

async def stop_block(
    css_tracker: CssTracker | None, manager: ConnectionManager
) -> tuple[CssTracker | None, ConnectionManager]:
    # log.info("ENTERED STOP")
    if not isinstance(css_tracker, CssTracker):
        await manager.broadcast("CssTracker: IS NOT INSTANTIATED!")
    elif not css_tracker.switch:
        await manager.broadcast("CssTracker: ALREADY STOPPED!")
    else:
        await css_tracker.stop()
        await manager.broadcast("CssTracker: STOPPED!")
    return css_tracker, manager