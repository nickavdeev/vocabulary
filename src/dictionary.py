from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

from src.custom_types import WordMeaning


EN_API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en"
DE_API_URL = "https://en.wiktionary.org/api/rest_v1/page/definition"


def decode_string(encoded_string: str) -> str:
    soup = BeautifulSoup(encoded_string, "html.parser")
    final_string = soup.get_text()
    return final_string


def get_en_word_meaning(word: str) -> WordMeaning:
    word = quote(word.strip().lower().replace("/", ""))

    result = requests.get(f"{EN_API_URL}/{word}").json()
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


def get_de_word_meaning(word: str) -> WordMeaning:
    prepared_word = quote(word.strip().replace("/", ""))

    result = requests.get(f"{DE_API_URL}/{prepared_word}").json()
    if not result.get("de"):
        capitalized_word = quote(word.strip().capitalize().replace("/", ""))
        result = requests.get(f"{DE_API_URL}/{capitalized_word}").json()
        if not result.get("de"):
            return False, "Word not found"

    text = ""
    for item in result["de"]:
        part_of_speech = item.get("partOfSpeech", "")
        text += f"\n<b>{part_of_speech}</b>\n"

        definitions = item.get("definitions", [])
        for definition in definitions:
            text += f"• {decode_string(definition.get('definition', ''))}\n"
            examples = definition.get("examples", [])
            if examples:
                text += f"<i>Example: {decode_string(examples[0])}</i>\n"
    return True, text


def get_word_meaning(word: str, language: str) -> WordMeaning:
    try:
        if language == "en":
            return get_en_word_meaning(word)
        elif language == "de":
            return get_de_word_meaning(word)
    except Exception as e:
        return False, f"Error occurred: {e}"
