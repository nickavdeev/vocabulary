from datetime import datetime, timedelta

from db.models import Cards, Status, Users, UserStatus
from settings import engine, logger
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import and_
from collections import defaultdict
from src.constants import ADDED_TO_VOCABULARY_TEXT, DAYS_BY_PHASES
from src.custom_types import UserId, UserLanguage


session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)
logger.info("Session created")


def get_user_language(telegram_id: UserId) -> UserLanguage:
    user = session.query(Users).get(telegram_id)
    return user.language


def update_user_language(telegram_id: UserId, language: str) -> None:
    user = session.query(Users).get(telegram_id)
    user.language = language
    session.commit()


def update_user_status(telegram_id: UserId, status: UserStatus) -> None:
    user = session.query(Users).get(telegram_id)
    user.status = status
    session.commit()


def get_data_to_repeat() -> dict:
    data = (
        session.query(Cards)
        .join(
            Users,
            and_(
                Users.telegram_id == Cards.telegram_id,
                Users.language == Cards.language
            )
        )
        .filter(
            Cards.next_repetition_on <= datetime.now().date(),
            Cards.status.in_([Status.in_progress])
        )
        .order_by(
            Cards.telegram_id,
            Cards.phase,
            Cards.next_repetition_on,
        )
        .all()
    )

    notifications = defaultdict(list)
    for card in data:
        notifications[card.telegram_id].append({
            "id": card.id,
            "phase": card.phase,
            "next_repetition_on": card.next_repetition_on,
            "word": card.word,
        })

    return dict(notifications)


def update_word_phase(card_id: int, next_repetition_on: datetime.date) -> None:
    card = session.query(Cards).get(card_id)
    try:
        card.next_repetition_on = next_repetition_on
        session.flush()
    except Exception as e:
        logger.error(f"Error occurred while updating word phase: {e}")

    card.phase += 1
    card.status = Status.learned if card.phase == 6 else Status.in_progress
    session.commit()


def add_word_to_vocabulary(telegram_id: UserId, word: str) -> tuple[bool, str]:
    try:
        new_card = Cards(
            telegram_id=telegram_id,
            word=word,
            language=get_user_language(telegram_id),
            next_repetition_on=(
                datetime.now().date() + timedelta(days=DAYS_BY_PHASES[0])
            ),
        )
        session.add(new_card)
        session.commit()
        return True, ADDED_TO_VOCABULARY_TEXT
    except Exception as e:
        error_message = "Error occurred while adding a word to vocabulary"
        logger.error(f"{error_message}: {e}")
        return False, error_message


def get_user_vocabulary(telegram_id: UserId) -> dict:
    cards = (
        session.query(Cards)
        .filter_by(
            telegram_id=telegram_id,
            language=get_user_language(telegram_id),
        )
        .order_by(Cards.next_repetition_on)
        .all()
    )
    return {
        "words_count": len(cards),
        "next_repetition": cards[0].next_repetition_on if cards else None,
    }


def is_word_in_vocabulary(
    telegram_id: UserId, word: str, language: UserLanguage
) -> bool:
    return bool(
        session.query(Cards)
        .filter_by(telegram_id=telegram_id, word=word, language=language)
        .first()
    )


def add_user_if_not_exists(telegram_id: UserId) -> bool:
    user = session.query(Users).filter_by(telegram_id=telegram_id)
    if not user.first():
        user = Users(telegram_id=telegram_id)
        session.add(user)
        session.commit()
        return True
    return False
