import logging
import os
import re
import sys
from logging import FileHandler, Formatter, Handler, Logger, StreamHandler
from pathlib import Path
from typing import Any, Callable, Optional, TextIO

def stream_supports_colour(stream: Any) -> bool:
    # Pycharm and Vscode support colour in their inbuilt editors
    reg: re.Pattern[str] = re.compile("^.*(vscode|pycharm).*$", flags=re.IGNORECASE)

    if reg.search(str(os.environ)):
        return True

    is_a_tty: Any | bool = hasattr(stream, "isatty") and stream.isatty()
    if sys.platform != "win32":
        return is_a_tty

    # ANSICON checks for things like ConEmu
    # WT_SESSION checks if this is Windows Terminal
    return is_a_tty and ("ANSICON" in os.environ or "WT_SESSION" in os.environ)


class _ColourFormatter(Formatter):
    # https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
    # ANSI codes are a bit weird to decipher if you're unfamiliar with them, so here's a refresher
    # It starts off with a format like \x1b[XXXm where XXX is a semicolon separated list of commands
    # The important ones here relate to colour.
    # 30-37 are black, red, green, yellow, blue, magenta, cyan and white in that order
    # 40-47 are the same except for the background
    # 90-97 are the same but "bright" foreground
    # 100-107 are the same as the bright ones but for the background.
    # 1 means bold, 2 means dim, 0 means reset, and 4 means underline.

    LEVEL_COLOURS: list[tuple[int, str]] = [
        (logging.DEBUG, "\x1b[32;1m"),
        (logging.INFO, "\x1b[34;1m"),
        (logging.WARNING, "\x1b[33;1m"),
        (logging.ERROR, "\x1b[31;1m"),
        (logging.CRITICAL, "\x1b[41m;1m"),
    ]

    FORMATS: dict[int, Formatter] = {
        level: Formatter(
            f"\x1b[30;1m%(asctime)s\x1b[0m {colour}%(levelname)s\x1b[0m \x1b[35m%(name)s - %(funcName)s - \x1b[95;1m%(lineno)d: \x1b[37;0m%(message)s",
            "%Y-%m-%d %H:%M:%S",
        )
        for level, colour in LEVEL_COLOURS
    }

    # format: str = (
    #     "%(asctime)s - %(levelname)s - [%(name)s - %(funcName)s - %(lineno)d]:  %(message)s"
    # )

    def format(self, record) -> str:
        formatter: Formatter | None = self.FORMATS.get(record.levelno)
        if formatter is None:
            formatter = self.FORMATS[logging.DEBUG]

        # Override the traceback to always print in red
        if record.exc_info:
            text: str = formatter.formatException(record.exc_info)
            record.exc_text = f"\x1b[31m{text}\x1b[0m"

        output: str = formatter.format(record)

        # Remove the cache layer
        record.exc_text = None
        return output


class FlaskHandler(FileHandler):
    def __init__(
        self,
        filename: Path,
        mode: str = "a",
        encoding: str | None = None,
        delay: bool = False,
        errors: str | None = None,
        emitter: Callable | None = None,
        emitter_args: tuple | None = None,
    ) -> None:
        super().__init__(filename, mode, encoding, delay, errors)
        self.emitter = emitter
        self.emitter_args: tuple = emitter_args or ()

    def emit(self, record) -> None:
        """
        Standard emit behavior for FileHander with additional custom emit.
        """
        if self.stream is None and (self.mode != "w" or not self._closed):
            self.stream = self._open()
        if self.stream:
            StreamHandler.emit(self, record)
        if isinstance(self.emitter, Callable):
            msg: str = self.format(record)
            self.emitter(*self.emitter_args, msg)


def logdef(
    name: Optional[str] = None,
    handler: Optional[Handler] = None,
    file_handler: Optional[FileHandler] = None,
    formatter: Optional[Formatter] = None,
    level: Optional[int] = None,
    emitter: Callable | None = None,
    emitter_args: tuple | None = None,
) -> Logger:
    """A helper function to setup logging.

    Parameters
    -----------

    handler: :class:`logging.Handler`
        The log handler to use for the library's logger.
        The default log handler if not provided is :class:`logging.StreamHandler`.

    formatter: :class:`logging.Formatter`
        The formatter to use with the given log handler. If not provided then it
        defaults to a colour based logging formatter (if available). If colour
        is not available then a simple logging formatter is provided.

    level: :class:`int`
        The default log level for the library's logger. Defaults to ``logging.INFO``.

    root: :class:`bool`
        Whether to set up the root logger rather than the library logger.
    """
    emitter_args: tuple = emitter_args or ()

    loggerpath: Path = (
        Path.cwd() / "logs" / (f"{name if name is not None else 'root'}.log")
    )
    if not loggerpath.exists():
        loggerpath.parent.mkdir(parents=True, exist_ok=True)

    if level is None:
        level: int = logging.DEBUG

    handlers = []
    if handler is None and name:
        handler: StreamHandler[TextIO] = logging.StreamHandler()
        handlers += [handler]

    if file_handler is None:
        # file_handler: FileHandler = FileHandler(filename=loggerpath, encoding="utf-8")
        file_handler: FlaskHandler = FlaskHandler(
            filename=loggerpath,
            encoding="utf-8",
            emitter=emitter,
            emitter_args=emitter_args,
        )
        handlers += [file_handler]

    if formatter is None:
        if isinstance(handler, logging.StreamHandler) and stream_supports_colour(
            handler.stream
        ):
            formatter: _ColourFormatter = _ColourFormatter()
        else:
            dt_fmt: str = "%Y-%m-%d %H:%M:%S"
            formatter = Formatter(
                fmt="[{asctime}] [{levelname:<8}] {name}: {message}",
                datefmt=dt_fmt,
                style="{",
            )

    logger: Logger = logging.getLogger(name)
    logger.setLevel(level)

    for hndlr in handlers:
        hndlr.setFormatter(formatter)
        logger.addHandler(hndlr)

    return logger
