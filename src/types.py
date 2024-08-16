from typing import NewType


type UserId = NewType("UserId", int)
type UserLanguage = NewType("UserLanguage", str)
type WordMeaning = tuple[bool, str]
