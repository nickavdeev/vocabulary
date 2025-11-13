from db.utils import (
    add_user_if_not_exists,
    add_word_to_vocabulary,
    get_user_language,
    get_user_vocabulary,
    is_word_in_vocabulary,
    session,
    update_user_language,
)
from settings import ADMIN_USER_TELEGRAM_ID, bot, logger
from telebot.types import CallbackQuery, Message

from src.bot.keyboards import (
    MAIN_MENU_BUTTONS,
    get_languages_keyboard,
    get_main_keyboard,
    get_word_keyboard,
)
from src.constants import (
    ADD_TO_VOCABULARY_CALLBACK,
    CHOOSE_LANGUAGE_CALLBACK,
    EMPTY_VOCABULARY_TEXT,
    ERROR_TEXT,
    EXAMPLES_GENERATED_TEXT,
    EXAMPLES_GENERATION_FAILED_TEXT,
    INNER_ERROR_TEXT,
    LANGUAGE_UPDATED_CALLBACK_QUERY,
    LANGUAGE_UPDATED_TEXT,
    PROVIDE_EXAMPLES_CALLBACK,
    START_TEXT,
    STATISTICS_BUTTON,
    STATISTICS_TEXT,
    WELCOME_TEXT,
    WORD_IN_VOCABULARY_TEXT,
)
from src.custom_types import LANGUAGES_DATA, UserId
from src.dictionary import get_word_meaning
from src.utils import get_ai_examples


@bot.message_handler(commands=["start", "statistics"])
@bot.message_handler(func=lambda message: message.text in MAIN_MENU_BUTTONS)
def send_command(message: Message):
    logger.info(f"Received a command from {message.chat.id}: {message.text}")
    chat_id = UserId(message.chat.id)
    if message.text == "/start":
        is_new_user = add_user_if_not_exists(chat_id)
        if is_new_user:
            bot.send_message(
                message.chat.id,
                START_TEXT,
                parse_mode="HTML",
                reply_markup=get_languages_keyboard(),
            )
            return
        bot.send_message(
            message.chat.id,
            WELCOME_TEXT,
            parse_mode="HTML",
            reply_markup=get_main_keyboard(),
            disable_web_page_preview=True,
        )
    elif message.text in {"/statistics", STATISTICS_BUTTON}:
        statistics = get_user_vocabulary(chat_id)
        words_count, next_repetition = (
            statistics["words_count"],
            statistics["next_repetition"],
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
                next_repetition=(
                    f"{next_repetition.day} {next_repetition.strftime('%B')}"
                ),
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
    elif call.data == PROVIDE_EXAMPLES_CALLBACK:
        user_code_language = get_user_language(chat_id)
        language = LANGUAGES_DATA[user_code_language]
        try:
            ai_completion = get_ai_examples(call.message.text, language.name)
            text = f"<b>Examples of today’s words</b>\n\n{ai_completion}"
            callback = EXAMPLES_GENERATED_TEXT
        except Exception as e:
            logger.error(e)
            text = (
                f"{call.message.text}\n\n"
                f"<i>Providing examples is not available at the moment.</i>"
            )
            callback = EXAMPLES_GENERATION_FAILED_TEXT
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            entities=call.message.entities,
            parse_mode="HTML",
        )
        bot.answer_callback_query(callback_query_id=call.id, text=callback)
    elif call.data.startswith(CHOOSE_LANGUAGE_CALLBACK):
        code = call.data.split("-")[1]
        language = LANGUAGES_DATA[code]
        update_user_language(chat_id, language.code)

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=LANGUAGE_UPDATED_TEXT.format(lang=language.interface_name),
            parse_mode="HTML",
        )
        bot.answer_callback_query(
            callback_query_id=call.id,
            text=LANGUAGE_UPDATED_CALLBACK_QUERY,
        )


if __name__ == "__main__":
    logger.info("Bot started")
    bot.infinity_polling()
    logger.info("Bot stopped")
    session.close()
    logger.info("Session closed")
