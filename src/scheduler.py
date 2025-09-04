import time
from datetime import timedelta

import schedule
from db.models import UserStatus
from db.utils import get_data_to_repeat, update_user_status, update_word_phase
from settings import bot, logger
from telebot.apihelper import ApiTelegramException

from src.constants import DAYS_BY_PHASES


@schedule.repeat(schedule.every().day.at("10:00", "UTC"))
def send_remember_message():
    """Send a reminder to repeat words"""

    logger.info("Sending a reminder to repeat words")
    data = get_data_to_repeat()
    if not data:
        logger.info("No words to repeat")
        return

    for telegram_id, words_data in data.items():
        if not words_data:
            continue

        logger.info(f"Sending a reminder to {telegram_id}")
        text = "<b>A reminder to repeat words</b>\n\n"
        for i, word_data in enumerate(words_data, start=1):
            date, phase = word_data["next_repetition_on"], word_data["phase"]
            next_repetition_time = date + timedelta(days=DAYS_BY_PHASES[phase])

            text += f"{i}. {word_data['word']}\n"
            update_word_phase(word_data["id"], next_repetition_time)
        try:
            bot.send_message(telegram_id, text, parse_mode="HTML")
        except ApiTelegramException as e:
            if e.error_code == 403:  # Forbidden
                update_user_status(telegram_id, UserStatus.inactive)
            logger.info(
                f"The user {telegram_id} failed to send a reminder: "
                f"{e.error_code}, {e.description}"
            )
            continue
        except Exception as e:
            logger.error(f"Failed to send a reminder: {e}")
            continue

        logger.info(f"Reminder sent to {telegram_id}")


logger.info("Scheduler started")
while True:
    schedule.run_pending()
    wait = int(schedule.idle_seconds())
    if wait is None:
        time.sleep(60)
    else:
        time.sleep(max(1, min(wait, 60)))
