from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.constants import ADD_TO_VOCABULARY_CALLBACK


def get_word_keyboard(word) -> InlineKeyboardMarkup:
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
