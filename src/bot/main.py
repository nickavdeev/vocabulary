from db.utils import (
    add_user_if_not_exists,
    add_word_to_vocabulary,
    get_user_language,
    get_user_vocabulary,
    is_word_in_vocabulary,
    update_user_language,
)
from settings import bot, logger

from src.bot.keyboards import get_language_keyboard, get_word_keyboard
from src.constants import (
    ADD_TO_VOCABULARY_CALLBACK,
    WELCOME_MESSAGE,
    WORD_IN_VOCABULARY,
)
from src.dictionary import get_word_meaning


@bot.message_handler(commands=["start", "vocabulary", "language"])
def send_command(message):
    logger.info(f"Received a command: {message.text}")
    if message.text == "/start":
        add_user_if_not_exists(message.chat.id)
        bot.send_message(
            message.chat.id,
            WELCOME_MESSAGE,
            parse_mode="HTML",
        )
    elif message.text == "/vocabulary":
        words = get_user_vocabulary(message.chat.id)
        if not words:
            bot.send_message(
                message.chat.id,
                "Your vocabulary is empty",
            )
            return

        text = "<b>Your vocabulary</b>\n\n"
        for i, word in enumerate(words, start=1):
            additional_text = "learned"
            if word["status"] == "in_progress":
                next_repetition = word["next_repetition"].strftime("%d %b %Y")
                additional_text = f"next repetition on {next_repetition}"
            text += f"{i}. <b><i>{word['word']}</i></b>, {additional_text}\n"

        bot.send_message(
            message.chat.id,
            text,
            parse_mode="HTML",
        )
    elif message.text == "/language":
        bot.send_message(
            message.chat.id,
            "Choose the language you want to learn",
            reply_markup=get_language_keyboard(),
        )


@bot.message_handler(content_types=["text"])
def send_message(message):
    logger.info(f"Received a message: {message.text} from {message.chat.id}")

    user_language = get_user_language(message.chat.id)
    ok, text = get_word_meaning(message.text, user_language)
    keyboard = get_word_keyboard(message.text) if ok else None

    if is_word_in_vocabulary(message.chat.id, message.text, user_language):
        text += f"\n{WORD_IN_VOCABULARY}"
        keyboard = None

    bot.send_message(
        message.chat.id,
        text,
        parse_mode="HTML",
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    logger.info(f"Received a callback: {call.data}")
    if call.data.startswith(ADD_TO_VOCABULARY_CALLBACK):
        word = call.data.split("-")[1]

        _, text = add_word_to_vocabulary(call.message.chat.id, word)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"{call.message.text}\n\n{text}",
        )
    elif call.data in ("en", "de"):
        update_user_language(call.message.chat.id, call.data)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Language successfully updated",
            parse_mode="HTML",
        )


if __name__ == "__main__":
    logger.info("Bot started")
    bot.infinity_polling()
