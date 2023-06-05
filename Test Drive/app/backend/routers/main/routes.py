import json
from logging import Logger

from fastapi import Depends, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from starlette.templating import _TemplateResponse

from ...config import APISettings, get_api_settings
from ...logger import logdef
from ..utils import check_localhost, exec_block, get_chapters, jsonResp, load_notes, parse_body, render_html, get_chapter_questions, save_content_to_notes
from . import router

log: Logger = logdef(__name__)
config: APISettings = get_api_settings()


@router.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    return FileResponse(config.FAV_ICON_PATH)
    # return "dummy", 200


@router.get("/", response_class=HTMLResponse)
def main_index(request: Request) -> _TemplateResponse:
    return render_html(
        "index.html",
    )


@router.get("/debug", response_class=HTMLResponse)
def main_index_debug(
    request: Request, dependencies=[Depends(check_localhost)]
) -> _TemplateResponse:
    return render_html(
        "index_debug.html",
    )


@router.get("/api/test", response_class=HTMLResponse)
async def api_test(request: Request):
    return "dummy", 200


@router.get("/api/chapters", response_class=HTMLResponse)
async def api_chapters(request: Request):
    return await exec_block(get_chapters)

@router.get("/api/chapter/questions", response_class=JSONResponse)
async def api_chapter_questions(request: Request) -> JSONResponse:
    chapter = request.query_params._dict.get('chapter')
    questions = await exec_block(get_chapter_questions, chapter)
    return jsonResp({'data': questions})

@router.post("/api/save/note", response_class=JSONResponse)
async def api_save_note(request: Request) -> JSONResponse:
    payload = (await parse_body(request))
    question: str = payload['question']
    content: str = payload['content']
    await exec_block(save_content_to_notes, content, question) 
    return jsonResp({'data':'ok'})

@router.get("/api/load/note", response_class=JSONResponse)
async def api_load_note(request: Request) -> JSONResponse:
    print(request.query_params._dict)
    question: str = (request.query_params._dict)['question']
    note = await exec_block(load_notes, question)
    # await exec_block(save_content_to_notes, content, question) 
    return jsonResp({'note':note})