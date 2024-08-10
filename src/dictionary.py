import requests


API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en"


def get_word_meaning(word):
    word = word.strip().lower().replace("/", "").replace(" ", "%20")

    result = requests.get(f"{API_URL}/{word}").json()
    if not isinstance(result, list):
        return False, "Word not found"

    text = ""
    for item in result[0].get("meanings", []):
        part_of_speech = item.get("partOfSpeech", "")
        text += f"\n<b>{part_of_speech}</b>\n"

        definitions = item.get("definitions", [])
        for definition in definitions:
            text += f"• {definition.get('definition', '')}\n"
            example = definition.get("example", "")
            if example:
                text += f"<i>Example: {example}</i>\n"

    return True, text
