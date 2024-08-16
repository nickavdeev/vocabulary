from datetime import datetime, timedelta

from db.models import Cards, Status, Users
from settings import engine, logger
from sqlalchemy.orm import Session

from src.constants import ADDED_TO_VOCABULARY, DAYS_BY_PHASES
from src.types import UserId, UserLanguage


def get_user_language(telegram_id: UserId) -> UserLanguage:
    with Session(engine) as session:
        user = session.query(Users).get(telegram_id)
        return user.language


def update_user_language(telegram_id: UserId, language: str) -> None:
    with Session(engine) as session:
        user = session.query(Users).get(telegram_id)
        user.language = language
        session.commit()


def get_data_to_repeat() -> dict:
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


def update_word_phase(card_id: int, next_repetition_on: datetime.date) -> None:
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


def add_word_to_vocabulary(telegram_id: UserId, word: str) -> tuple[bool, str]:
    with Session(engine) as session:
        try:
            new_card = Cards(
                telegram_id=telegram_id,
                word=word,
                language=get_user_language(telegram_id),
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


def get_user_vocabulary(telegram_id: UserId) -> dict:
    with Session(engine) as session:
        cards = (
            session.query(Cards)
            .filter(
                Cards.telegram_id == telegram_id,  # noqa
            )
            .order_by(
                Cards.language,
                Cards.next_repetition_on,
            )
            .all()
        )
    data_by_languages = {}
    for card in cards:
        data_by_languages[card.language] = data_by_languages.get(
            card.language, []
        )
        data_by_languages[card.language].append(
            {
                "word": card.word,
                "status": card.status,
                "next_repetition": card.next_repetition_on,
            }
        )
    return data_by_languages


def is_word_in_vocabulary(
    telegram_id: UserId, word: str, language: UserLanguage
) -> bool:
    with Session(engine) as session:
        return bool(
            session.query(Cards)
            .filter(
                Cards.telegram_id == telegram_id,
                Cards.word == word,  # noqa
                Cards.language == language,
            )
            .first()
        )


def add_user_if_not_exists(telegram_id: UserId) -> None:
    with Session(engine) as session:
        user = session.query(Users).filter(Users.telegram_id == telegram_id)
        if not user.first():
            user = Users(telegram_id=telegram_id)
            session.add(user)
            session.commit()
