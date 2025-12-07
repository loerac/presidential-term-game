from enum import StrEnum, auto

FLAG_ART = (
    "|✭ ✭ ✭ ✭ ✭ ✭ ✭ ✭ ✭ ✭ 🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥\n"
    "| ✭ ✭ ✭ ✭ ✭ ✭ ✭ ✭ ✭  ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n"
    "|✭ ✭ ✭ ✭ ✭ ✭ ✭ ✭ ✭ ✭ 🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥\n"
    "| ✭ ✭ ✭ ✭ ✭ ✭ ✭ ✭ ✭  ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n"
    "|✭ ✭ ✭ ✭ ✭ ✭ ✭ ✭ ✭ ✭ 🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥\n"
    "| ✭ ✭ ✭ ✭ ✭ ✭ ✭ ✭ ✭  ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n"
    "|✭ ✭ ✭ ✭ ✭ ✭ ✭ ✭ ✭ ✭ 🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥\n"
    "|⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n"
    "|🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥\n"
    "|⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n"
    "|🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥\n"
    "|⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n"
    "|🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥\n"
)


class ButtonVariant(StrEnum):
    DEFAULT = auto()
    ERROR = auto()
    PRIMARY = auto()
    SUCCESS = auto()


class ButtonId(StrEnum):
    RESTART = auto()
    VIEW_SCOREBOARD = auto()
    QUIT = auto()


CHOICE_BUTTONS = [
    ("A", 0),
    ("B", 1),
    ("C", 2),
    ("D", 3),
]
