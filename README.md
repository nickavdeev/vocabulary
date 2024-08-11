# @VocabMateBot
[Telegram bot](https://t.me/VocabMateBot) for repeating words, according to the [forgetting curve](https://en.wikipedia.org/wiki/Forgetting_curve).

## Installation
1. Clone this repository:
    ```bash
    git clone https://github.com/nickavdeev/vocabulary.git
    ```
2. Create `.env` file in the root of the project and fill it with the variables from `.env.example`:
    ```bash
    cp .env.example .env
    ```
3. Crate virtual environment and activate it:
    ```bash
    python -m venv .venv
   source .venv/bin/activate
    ```
4. Install dependencies: `pip install -r requirements.txt`
5. Set up Alembic: edit `sqlalchemy.url` in `alembic.ini`
6. Migrate the database: `alembic upgrade head`
7. Run the bot: `python src/bot/main.py`
8. Run the scheduler: `python src/scheduler.py`
