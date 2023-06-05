import json
from asyncio import AbstractEventLoop, get_running_loop
from concurrent.futures import ThreadPoolExecutor
from contextvars import Context, copy_context
from functools import partial
from inspect import currentframe
from logging import Logger
from pathlib import Path
from typing import Any, Optional

import plotly.graph_objects as go
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from joblib import dump, load
from plotly.utils import PlotlyJSONEncoder
from starlette.status import HTTP_403_FORBIDDEN
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


async def parse_body(request: Request):
    data = {}
    body: bytes = await request.body()
    # print(f"{body=}")
    if isinstance(body, bytes):
        # decode the bytes to a string
        body_str: str = body.decode("utf-8")
        # print(f"{body_str=}")
    if "&" in body_str:
        # parse the string as a dictionary using parse_qs
        data = parse_qs(body_str)
    else:
        try:
            data = json.loads(body_str)
        except json.JSONDecodeError:
            print("data is not json object")
    # print(f"{data=}")
    return data


def save_object(obj, filepath):
    # Convert the filepath to a Path object
    path = Path(filepath)

    # Create the parent directories if they don't exist
    path.parent.mkdir(parents=True, exist_ok=True)

    # Save the object using joblib
    try:
        dump(obj, path)
    except Exception as e:
        log.error(e)


def load_object(filepath):
    # Convert the filepath to a Path object
    path = Path(filepath)

    # Load the object using joblib
    try:
        return load(path)
    except Exception as e:
        log.error(e)


async def check_localhost(request: Request):
    client_host = request.client.host
    if client_host not in ("localhost", "127.0.0.1", "::1"):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Access allowed only from localhost.",
        )


def load_data(choice):
    if choice=='quiz':
        path = config.DATA_QUIZ_PATH   
    elif choice=='roadsigns':
        path = config.DATA_ROADSIGNS_PATH
    
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)


def get_chapters(choice) -> str:
    chapters = [list(k.keys())[0] for k in load_data(choice)[0]]
    return json.dumps(chapters)


def get_chapter_items(chapter: str, choice):
    data = load_data(choice)[0]  # Assuming the data is a list of dictionaries
    items = [chaptr[chapter] for chaptr in data if chaptr.get(chapter) is not None]
    return items


def save_content_to_notes(content, question):
    try:
        with open("data/notes.json", "r", encoding="utf-8") as file:
            notes = json.load(file)
    except FileNotFoundError:
        notes = {}

    notes[question] = content

    with open("data/notes.json", "w", encoding="utf-8") as file:
        json.dump(notes, file)

    print("Content saved successfully.")


def load_notes(question=None):
    try:
        with open("data/notes.json", "r", encoding="utf-8") as file:
            notes = json.load(file)
    except FileNotFoundError:
        notes = {}

    if question is None:
        return notes
    elif question in notes:
        return notes[question]
    else:
        return ''
