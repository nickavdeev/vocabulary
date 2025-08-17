from db.utils import (
    add_user_if_not_exists,
    add_word_to_vocabulary,
    get_user_language,
    get_user_vocabulary,
    is_word_in_vocabulary,
    session,
)
from settings import ADMIN_USER_TELEGRAM_ID, bot, logger
from telebot.types import CallbackQuery, Message

from src.bot.keyboards import (
    MAIN_MENU_BUTTONS,
    get_main_keyboard,
    get_word_keyboard,
)
from src.constants import (
    ADD_TO_VOCABULARY_CALLBACK,
    EMPTY_VOCABULARY_TEXT,
    ERROR_TEXT,
    INNER_ERROR_TEXT,
    STATISTICS_BUTTON,
    STATISTICS_TEXT,
    WELCOME_MESSAGE,
    WORD_IN_VOCABULARY_TEXT,
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
    elif message.text in {"/statistics", STATISTICS_BUTTON}:
        statistics = get_user_vocabulary(chat_id)
        words_count, next_repetition = (
            statistics["words_count"],
            statistics["next_repetition"]
        )
        if not words_count:
            bot.send_message(
                message.chat.id,
                EMPTY_VOCABULARY_TEXT,
                parse_mode="HTML",
            )
            return

        bot.send_message(
            message.chat.id,
            STATISTICS_TEXT.format(
                words_count=words_count,
                word_label="words" if words_count > 1 else "word",
                next_repetition=next_repetition.strftime("%d %B")
            ),
            parse_mode="HTML",
        )


@bot.message_handler(content_types=["text"])
def send_message(message: Message):
    logger.info(f"Received a message: `{message.text}` from {message.chat.id}")

    chat_id = UserId(message.chat.id)
    user_language = get_user_language(chat_id)
    ok, text = get_word_meaning(message.text, user_language)
    if not ok:
        logger.info(text)
        text = f"Word not found: {message.text}"
    keyboard = get_word_keyboard(message.text) if ok else None

    if is_word_in_vocabulary(chat_id, message.text, user_language):
        text += f"\n{WORD_IN_VOCABULARY_TEXT}"
        keyboard = None

    try:
        bot.send_message(
            message.chat.id,
            text,
            parse_mode="HTML",
            reply_markup=keyboard,
        )
    except Exception as e:
        logger.error(e)
        bot.send_message(message.chat.id, ERROR_TEXT)
        bot.send_message(
            ADMIN_USER_TELEGRAM_ID,
            INNER_ERROR_TEXT.format(
                chat_id=message.chat.id,
                message_text=message.text,
                error_text=e,
            ),
            parse_mode="HTML",
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
            entities=call.message.entities,
        )
        bot.answer_callback_query(callback_query_id=call.id, text=text)


if __name__ == "__main__":
    logger.info("Bot started")
    bot.infinity_polling()
    logger.info("Bot stopped")
    session.close()
    logger.info("Session closed")
