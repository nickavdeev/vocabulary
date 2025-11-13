ADD_TO_VOCABULARY_CALLBACK = "add_to_vocabulary"
PROVIDE_EXAMPLES_CALLBACK = "provide_examples"
CHOOSE_LANGUAGE_CALLBACK = "choose_language"

LANGUAGE_UPDATED_CALLBACK_QUERY = "✔️ Language updated"
ADDED_TO_VOCABULARY_TEXT = "✔️ Added to vocabulary"
WORD_IN_VOCABULARY_TEXT = "✔️ <i>This word is already in your vocabulary</i>"
EXAMPLES_GENERATED_TEXT = "✔️ Examples generated"
EXAMPLES_GENERATION_FAILED_TEXT = "Examples generation failed"

DAYS_BY_PHASES = {
    0: 1,
    1: 2,
    2: 6,
    3: 15,
    4: 39,
    5: 97,
    6: 0,
}

# Prompts

PROMPT_GETTING_EXAMPLES = """
You are given a list of words in the {language} language.
For each word, write one short and simple example sentence in the given 
language that helps to recall its meaning. The output format must strictly 
follow this structure:

1. word
<i>Example: [your sentence]</i>
2. word
<i>Example: [your sentence]</i>
...

If there is only one word:
1. word
<i>Example: [your sentence]</i>

Here is the list of words:
{content}"
"""

# Button names

STATISTICS_BUTTON = "📊 Statistics"

# Texts

START_TEXT = (
    "👋 <b>Welcome to the Vocabulary Bot!</b>\n\n"
    "Before we begin, please choose the language you want to learn:"
)

WELCOME_TEXT = (
    "🌐 <b>Welcome to the Vocabulary Bot!</b>\n\n"
    "Send me a word, and I'll give you its definitions."
    "You can add it to your list and review it later — "
    "I'll remind you to practice based on the forgetting curve.\n\n"
    "To learn more about Vocabulary Bot, please visit "
    "<a href='https://avdeev.me/vocabulary/'>our website</a>."
)

LANGUAGE_UPDATED_TEXT = (
    "Great! Chosen language to learn:\n<b>{lang}</b>\n\n"
    "To get started, just send me a word you'd like to learn, "
    "and I’ll give you its definitions. "
    "Add it to your list and review it later — I'll remind you to "
    "practice based on the forgetting curve.\n\n"
)

EMPTY_VOCABULARY_TEXT = (
    "🔎 <b>Your vocabulary is empty</b>, but you can expand it: "
    "just send me a word, and I’ll give you its definitions."
)
ERROR_TEXT = (
    "👀 Sorry, something went wrong on my side. Please try again later."
)
INNER_ERROR_TEXT = (
    "💥 <b>New error</b>\n\n"
    "User: <i>{chat_id}</i>\n"
    "Message: <i>{message_text}</i>\n"
    "Error text: <pre>{error_text}</pre>"
)
STATISTICS_TEXT = (
    "<b>Here is your vocabulary statistics:</b>\n\n"
    "{words_count} {word_label} added. The next repetition is scheduled "
    "for {next_repetition}.\n\nKeep going! 🙌"
)
