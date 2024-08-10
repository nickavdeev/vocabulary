from datetime import datetime, timedelta

from db.models import Cards, Status
from settings import engine, logger
from sqlalchemy.orm import Session

from src.constants import ADDED_TO_VOCABULARY, DAYS_BY_PHASES


def get_data_to_repeat():
    with Session(engine) as session:
        data = (
            session.query(Cards)
            .filter(Cards.next_repetition_on <= datetime.now().date())
            .filter(Cards.status.in_([Status.in_progress]))
            .order_by(
                Cards.telegram_id,
                Cards.phase,
                Cards.next_repetition_on,
            )
            .all()
        )

    notifications = {}
    for card in data:
        telegram_id = card.telegram_id
        notifications[telegram_id] = notifications.get(telegram_id, [])
        notifications[telegram_id].append(
            {
                "id": card.id,
                "phase": card.phase,
                "next_repetition_on": card.next_repetition_on,
                "word": card.word,
            }
        )
    return notifications


def update_word_phase(card_id, next_repetition_on):
    with Session(engine) as session:
        try:
            card = session.query(Cards).get(card_id)
            card.next_repetition_on = next_repetition_on
            session.flush()
        except Exception as e:
            logger.error(f"Error occurred while updating word phase: {e}")

        card.phase += 1
        card.status = Status.learned if card.phase == 6 else Status.in_progress
        session.commit()


def add_word_to_vocabulary(telegram_id, word):
    with Session(engine) as session:
        card = (
            session.query(Cards)
            .filter(
                Cards.telegram_id == telegram_id,
                Cards.word == word,
            )
            .first()
        )
        if card:
            return False, "Word already exists in your /vocabulary"

        try:
            new_card = Cards(
                telegram_id=telegram_id,
                word=word,
                next_repetition_on=datetime.now().date()
                + timedelta(days=DAYS_BY_PHASES[0]),
            )
            session.add(new_card)
            session.commit()
            return True, ADDED_TO_VOCABULARY
        except Exception as e:
            error_message = "Error occurred while adding a word to vocabulary"
            logger.error(f"{error_message}: {e}")
            return False, error_message


def get_user_vocabulary(telegram_id):
    with Session(engine) as session:
        cards = (
            session.query(Cards)
            .filter(Cards.telegram_id == telegram_id)
            .order_by(
                Cards.status.desc(),
                Cards.phase,
                Cards.next_repetition_on,
            )
            .all()
        )
    return [
        {
            "word": card.word,
            "status": card.status,
            "next_repetition": card.next_repetition_on,
        }
        for card in cards
    ]


def is_word_in_vocabulary(telegram_id, word):
    with Session(engine) as session:
        return bool(
            session.query(Cards)
            .filter(
                Cards.telegram_id == telegram_id,
                Cards.word == word,
            )
            .first()
        )
