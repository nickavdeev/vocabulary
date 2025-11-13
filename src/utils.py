from settings import GPT

from src.constants import PROMPT_GETTING_EXAMPLES
from src.custom_types import UserLanguage


def get_ai_examples(content: str, language: UserLanguage) -> str:
    completion = GPT.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": PROMPT_GETTING_EXAMPLES.format(
                    language=language,
                    content=content,
                ),
            }
        ],
        temperature=0.3,
        n=1,
    )
    return completion.choices[0].message.content.strip()
