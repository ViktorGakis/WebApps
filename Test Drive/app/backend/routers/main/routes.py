from logging import Logger

from fastapi import Request
from fastapi.responses import HTMLResponse, JSONResponse

from ...config import APISettings, get_api_settings
from ...logger import logdef
from ..data_utils import (
    get_chapter_items,
    get_chapters,
    get_questions_by_note,
    load_notes,
    save_content_to_notes,
)
from ..utils import exec_block, jsonResp, parse_body
from . import router

log: Logger = logdef(__name__)
config: APISettings = get_api_settings()


@router.get("/")
def main_index() -> HTMLResponse:
    index_path = config.REACT_PATH / "index.html"
    with index_path.open("r") as file:
        html_content: str = file.read()
    return HTMLResponse(content=html_content, status_code=200)


@router.get("/api/test", response_class=HTMLResponse)
async def api_test(request: Request):
    return "dummy", 200


@router.get("/api/chapters/quiz", response_class=HTMLResponse)
async def api_chapters_quiz(request: Request):
    return await exec_block(get_chapters, "quiz")


@router.get("/api/chapters/roadsigns", response_class=HTMLResponse)
async def api_chapters_roadsigns(request: Request):
    return await exec_block(get_chapters, "roadsigns")


@router.get("/api/chapters/quiz/questions", response_class=JSONResponse)
async def api_chapter_quiz_questions(request: Request) -> JSONResponse:
    chapter = request.query_params._dict.get("chapter")
    questions = await exec_block(get_chapter_items, chapter, "quiz")
    return jsonResp({"data": questions})


@router.get("/api/chapters/roadsigns/signs", response_class=JSONResponse)
async def api_chapter_roadsigns_questions(request: Request) -> JSONResponse:
    chapter = request.query_params._dict.get("chapter")
    roadsigns = await exec_block(get_chapter_items, chapter, "roadsigns")
    print("roadsigns:", roadsigns)
    return jsonResp({"data": roadsigns})


@router.post("/api/save/note", response_class=JSONResponse)
async def api_save_note(request: Request) -> JSONResponse:
    payload = await parse_body(request)
    question: str = payload["question"]
    content: str = payload["content"]
    await exec_block(save_content_to_notes, content, question)
    return jsonResp({"data": "ok"})


@router.get("/api/load/note", response_class=JSONResponse)
async def api_load_note(request: Request) -> JSONResponse:
    question: str = (request.query_params._dict)["question"]
    note = await exec_block(load_notes, question)
    return jsonResp({"note": note})


@router.post("/api/retrieve/questions", response_class=JSONResponse)
async def api_retrieve_questions(request: Request) -> JSONResponse:
    # text: str = (request.query_params._dict)["text"]
    payload = await parse_body(request)
    text: str = payload["data"]
    print(f'text: {text}')
    questions = await exec_block(get_questions_by_note, text)
    print(f'questions: {questions}')
    return jsonResp({"data": questions})



