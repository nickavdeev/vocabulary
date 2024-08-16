from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.constants import ADD_TO_VOCABULARY_CALLBACK


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
    keyboard.add(
        InlineKeyboardButton(
            text="🇬🇧 English",
            callback_data="en",
        ),
        InlineKeyboardButton(
            text="🇩🇪 German",
            callback_data="de",
        ),
    )
    return keyboard
