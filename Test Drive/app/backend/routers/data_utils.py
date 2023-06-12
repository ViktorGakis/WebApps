import json
from logging import Logger

from ..config import APISettings, get_api_settings
from ..logger import logdef

config: APISettings = get_api_settings()

log: Logger = logdef(__name__)


def load_data(choice):
    if choice == "quiz":
        path = config.DATA_QUIZ_PATH
    elif choice == "roadsigns":
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
        return ""


def filter_questions_by_note(text: str):
    questions_found = []
    for question, note in load_notes().items():
        if isinstance(note, list):
            note = note[0].casefold()
        if text.casefold() in note.casefold():
            questions_found.append((question, note))
    return questions_found


def retrieve_question_info(questions):
    questions_of_interest = []
    data = load_data('quiz')
    for question in questions:
        for chapter_dict in data[0]:
            for chapter_question in list(chapter_dict.values())[0]:
                if chapter_question["question"].casefold() == question[0].casefold():
                    chapter_question["chapter"] = list(chapter_dict.keys())[0]
                    questions_of_interest.append(chapter_question)
    return questions_of_interest


def get_questions_by_note(text: str):
    questions = filter_questions_by_note(text)
    return retrieve_question_info(questions)
