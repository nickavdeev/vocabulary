from typing import NewType


UserId = NewType("UserId", int)
UserLanguage = NewType("UserLanguage", str)
WordMeaning = tuple[bool, str]
