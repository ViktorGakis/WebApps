import json
from asyncio import AbstractEventLoop, get_running_loop
from concurrent.futures import ThreadPoolExecutor
from contextvars import Context, copy_context
from functools import partial
from inspect import currentframe
from logging import Logger
from typing import Any, Optional

import plotly.graph_objects as go
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from plotly.utils import PlotlyJSONEncoder
from starlette.templating import _TemplateResponse

from ..config import APISettings, get_api_settings
from ..logger import logdef

config: APISettings = get_api_settings()

log: Logger = logdef(__name__)


def jsonify_plotly(fig: go.Figure) -> str:
    return json.dumps(fig, cls=PlotlyJSONEncoder)


def get_outer_scope_var(var_type: Any) -> Any | None:
    """Returns the first var of type var_type from the outerscope."""
    frame = currentframe().f_back.f_back
    if vars := [v for k, v in frame.f_locals.items() if isinstance(v, var_type)]:
        return vars[0]


def jsonResp(d: dict, media_type="application/json") -> JSONResponse:
    return JSONResponse(content=jsonable_encoder(d), media_type=media_type)


def render_html(
    template: str, context_vars: Optional[dict] = None
) -> _TemplateResponse:
    request: Request = get_outer_scope_var(Request)
    context_dict: dict[str, Request] = dict(request=request) | (context_vars or {})
    return request.app.state.templates.TemplateResponse(template, context_dict)


async def exec_block(func, /, *args, **kwargs) -> Any:
    loop: AbstractEventLoop = get_running_loop()
    with ThreadPoolExecutor() as pool:
        ctx: Context = copy_context()
        func_call: partial = partial(ctx.run, func, *args, **kwargs)
        return await loop.run_in_executor(pool, func_call)

async def parse_body(request: Request) -> dict[str, list[str]]:
    data = {}
    body: bytes = await request.body()
    print(f"{body=}")
    if isinstance(body, bytes):
        # decode the bytes to a string
        body_str: str = body.decode("utf-8")
        print(f"{body_str=}")
    if "&" in body_str:
        # parse the string as a dictionary using parse_qs
        data: dict[str, list[str]] = parse_qs(body_str)
    else:
        try:
            data = json.loads(body_str)
        except json.JSONDecodeError:
            print("data is not json object")
    print(f"{data=}")
    return data