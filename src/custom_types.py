from enum import Enum as StrEnum  # to avoid conflict with Python versions
from typing import NewType


UserId = NewType("UserId", int)
UserLanguage = NewType("UserLanguage", str)
WordMeaning = tuple[bool, str]


class LanguageCode(str, StrEnum):
    EN = "en"
    DE = "de"

    def __str__(self):
        return self.value


class Language:
    def __init__(self, code: str, emoji: str, name: str) -> None:
        self.code = code
        self.emoji = emoji
        self.name = name

    @property
    def interface_name(self) -> str:
        return f"{self.emoji} {self.name}"


LANGUAGES_DATA = {
    LanguageCode.EN: Language(LanguageCode.EN, "🇬🇧", "English"),
    LanguageCode.DE: Language(LanguageCode.DE, "🇩🇪", "Deutsch"),
}
