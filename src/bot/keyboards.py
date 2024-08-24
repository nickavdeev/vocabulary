from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from src.constants import (
    ADD_TO_VOCABULARY_CALLBACK,
    BUTTON_LANGUAGE,
    BUTTON_VOCABULARY,
    VISIBLE_LANGUAGES,
)


MAIN_MENU_BUTTONS = [BUTTON_VOCABULARY, BUTTON_LANGUAGE]


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


def get_language_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        row_width=2,
    )
    for language_code, visible_name in VISIBLE_LANGUAGES.items():
        keyboard.add(
            InlineKeyboardButton(
                text=visible_name,
                callback_data=language_code,
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
