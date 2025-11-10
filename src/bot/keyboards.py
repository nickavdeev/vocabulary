from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from src.constants import (
    ADD_TO_VOCABULARY_CALLBACK,
    CHOOSE_LANGUAGE_CALLBACK,
    PROVIDE_EXAMPLES_CALLBACK,
    STATISTICS_BUTTON,
)
from src.custom_types import LANGUAGES_DATA


MAIN_MENU_BUTTONS = [STATISTICS_BUTTON]
EXAMPLES_KEYBOARD = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(
        text="Provide examples",
        callback_data=PROVIDE_EXAMPLES_CALLBACK,
    ),
)


def get_word_keyboard(word: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        row_width=1,
    )
    keyboard.add(
        InlineKeyboardButton(
            text="Add to vocabulary",
            callback_data=f"{ADD_TO_VOCABULARY_CALLBACK}-{word}",
        ),
    )
    return keyboard


def get_main_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        row_width=1,
        resize_keyboard=True,
    )
    for button in MAIN_MENU_BUTTONS:
        keyboard.add(
            KeyboardButton(text=button),
        )
    return keyboard


def get_languages_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    for language in LANGUAGES_DATA.values():
        keyboard.add(
            InlineKeyboardButton(
                text=language.interface_name,
                callback_data=f"{CHOOSE_LANGUAGE_CALLBACK}-{language.code}",
            ),
        )
    return keyboard
