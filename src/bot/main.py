from db.utils import (
    add_word_to_vocabulary,
    get_user_vocabulary,
    is_word_in_vocabulary,
)
from settings import bot, logger

from src.bot.keyboards import get_word_keyboard
from src.constants import ADD_TO_VOCABULARY_CALLBACK, WORD_IN_VOCABULARY
from src.dictionary import get_word_meaning


@bot.message_handler(commands=["start", "vocabulary"])
def send_command(message):
    logger.info(f"Received a command: {message.text}")
    if message.text == "/start":
        bot.send_message(
            message.chat.id,
            "Welcome to the Vocabulary bot!\n\n"
            "Send me a word and I'll provide you with its meaning.",
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


@bot.message_handler(content_types=["text"])
def send_message(message):
    logger.info(f"Received a message: {message.text} from {message.chat.id}")
    ok, text = get_word_meaning(message.text)
    keyboard = get_word_keyboard(message.text) if ok else None

    if is_word_in_vocabulary(message.chat.id, message.text):
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


if __name__ == "__main__":
    logger.info("Bot started")
    bot.infinity_polling()
