from db.utils import (
    add_user_if_not_exists,
    add_word_to_vocabulary,
    get_user_language,
    get_user_vocabulary,
    is_word_in_vocabulary,
    update_user_language,
)
from settings import bot, logger
from telebot.types import CallbackQuery, Message

from src.bot.keyboards import (
    MAIN_MENU_BUTTONS,
    get_language_keyboard,
    get_main_keyboard,
    get_word_keyboard,
)
from src.constants import (
    ADD_TO_VOCABULARY_CALLBACK,
    BUTTON_LANGUAGE,
    BUTTON_VOCABULARY,
    VISIBLE_LANGUAGES,
    WELCOME_MESSAGE,
    WORD_IN_VOCABULARY,
)
from src.custom_types import UserId
from src.dictionary import get_word_meaning


@bot.message_handler(commands=["start", "vocabulary", "language"])
@bot.message_handler(func=lambda message: message.text in MAIN_MENU_BUTTONS)
def send_command(message: Message):
    logger.info(f"Received a command: {message.text}")
    chat_id = UserId(message.chat.id)
    if message.text == "/start":
        add_user_if_not_exists(chat_id)
        bot.send_message(
            message.chat.id,
            WELCOME_MESSAGE,
            parse_mode="HTML",
            reply_markup=get_main_keyboard(),
        )
    elif message.text in ["/vocabulary", BUTTON_VOCABULARY]:
        words = get_user_vocabulary(chat_id)
        if not words:
            bot.send_message(
                message.chat.id,
                "Your vocabulary is empty",
            )
            return

        with_language_title = len(words) > 1
        text = "<b>Your vocabulary</b>\n"
        for language in words:
            text += (
                f"\n{VISIBLE_LANGUAGES[language]}\n"
                if with_language_title
                else "\n"
            )
            for i, word in enumerate(words[language], start=1):
                additional_text = "learned"
                if word["status"] == "in_progress":
                    next_repetition = word["next_repetition"].strftime(
                        "%d %b %Y"
                    )
                    additional_text = f"next repetition on {next_repetition}"
                text += (
                    f"{i}. <b><i>{word['word']}</i></b>, {additional_text}\n"
                )

        bot.send_message(
            message.chat.id,
            text,
            parse_mode="HTML",
        )
    elif message.text in ["/language", BUTTON_LANGUAGE]:
        bot.send_message(
            message.chat.id,
            "Choose the language you want to learn",
            reply_markup=get_language_keyboard(),
        )


@bot.message_handler(content_types=["text"])
def send_message(message: Message):
    logger.info(f"Received a message: {message.text} from {message.chat.id}")

    chat_id = UserId(message.chat.id)
    user_language = get_user_language(chat_id)
    ok, text = get_word_meaning(message.text, user_language)
    if not ok:
        logger.info(text)
        text = f"Word not found: {message.text}"
    keyboard = get_word_keyboard(message.text) if ok else None

    if is_word_in_vocabulary(chat_id, message.text, user_language):
        text += f"\n{WORD_IN_VOCABULARY}"
        keyboard = None

    bot.send_message(
        message.chat.id,
        text,
        parse_mode="HTML",
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call: CallbackQuery):
    logger.info(f"Received a callback: {call.data}")
    chat_id = UserId(call.message.chat.id)

    if call.data.startswith(ADD_TO_VOCABULARY_CALLBACK):
        word = call.data.split("-")[1]

        _, text = add_word_to_vocabulary(chat_id, word)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"{call.message.text}\n\n{text}",
            parse_mode="HTML",
        )
    elif call.data in ("en", "de"):
        update_user_language(chat_id, call.data)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=(
                "Language successfully updated:\n"
                f"<b>{VISIBLE_LANGUAGES[call.data]}</b>"
            ),
            parse_mode="HTML",
        )


if __name__ == "__main__":
    logger.info("Bot started")
    bot.infinity_polling()
