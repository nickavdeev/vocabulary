ADD_TO_VOCABULARY_CALLBACK = "add_to_vocabulary"

ADDED_TO_VOCABULARY_TEXT = "✔️ Added to vocabulary"
WORD_IN_VOCABULARY_TEXT = "✔️ <i>This word is already in your vocabulary</i>"

WELCOME_MESSAGE = (
    "👋 <b>Welcome to the Vocabulary Bot!</b>\n\n"
    "Send me an English word, and I’ll give you its definitions. "
    "Add it to your list and review it later — I’ll remind you to "
    "practice based on the forgetting curve.\n\n"
    "Use these commands to interact with the bot:\n"
    "/vocabulary — view your vocabulary list"
)

DAYS_BY_PHASES = {
    0: 1,
    1: 2,
    2: 6,
    3: 15,
    4: 39,
    5: 97,
    6: 0,
}

# Button names

STATISTICS_BUTTON = "📊 Statistics"

# Texts

EMPTY_VOCABULARY_TEXT = (
    "🔎 <b>Your vocabulary is empty</b>, but you can expand it: "
    "just send me an English word, and I’ll give you its definitions."
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
    "{words_count} {word_label} added, next repetition is on "
    "{next_repetition}.\n\nKeep going! 🙌"
)
