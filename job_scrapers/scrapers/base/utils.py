
import json
from logging import Logger
from pathlib import Path
from typing import Optional, Union

from bs4 import BeautifulSoup, NavigableString, ResultSet, Tag
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from interface.backend.logger import logdef

log: Logger = logdef(__name__)

def read_from_file(filepath: Path, parser: str) -> BeautifulSoup:
    with filepath.open(mode="r", encoding="utf-8") as file:
        return BeautifulSoup(file.read(), features=parser)


def write_to_file(filepath: Path, data: Union[str, dict], data_format: str = "text"):
    try:
        # Create a Path object from the provided file path
        path = Path(filepath)

        # Create parent directories if they don't exist
        path.parent.mkdir(parents=True, exist_ok=True)

        if data_format == "text":
            # If data is BeautifulSoup, convert it to a prettified string
            if isinstance(data, BeautifulSoup):
                data = str(data.prettify())

            # Write the content to the file as text
            with path.open(mode="w", encoding="utf-8") as file:
                file.write(data)
        elif data_format == "json":
            # If data is a dictionary, convert it to a JSON-formatted string
            if isinstance(data, dict):
                data = json.dumps(data, indent=4)

            # Write the JSON content to the file
            with path.open(mode="w", encoding="utf-8") as file:
                file.write(data)
        else:
            raise ValueError("Invalid data format. Use 'text' or 'json'.")

        log.info(f"Successfully wrote the data to '{filepath}' in {data_format} format.")
    except Exception as e:
        log.error(f"An error occurred: {e}")


def soup(
    source: Union[
        BeautifulSoup, NavigableString, ResultSet, Tag, WebElement, WebDriver, str, Path
    ],
    parser="html.parser",
    filepath: Optional[Path | str] = "temp.html",
) -> BeautifulSoup:
    soupen = None

    if isinstance(source, (BeautifulSoup, NavigableString, ResultSet, Tag)):
        soupen = source
    elif isinstance(source, Path) and source.exists():
        soupen = read_from_file(source, parser)
    elif isinstance(source, str):
        path = Path(source)
        if path.exists():
            soupen = read_from_file(path, parser)
        else:
            soupen = BeautifulSoup(source, features=parser)
    elif isinstance(source, WebElement):
        source_html: str = source.get_attribute("innerHTML")
        soupen = BeautifulSoup(source_html, features=parser)
    elif isinstance(source, WebDriver):
        source_html: str = source.page_source
        soupen = BeautifulSoup(source_html, features=parser)

    if filepath and soupen is not None:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        write_to_file(path, soupen)

    return soupen
