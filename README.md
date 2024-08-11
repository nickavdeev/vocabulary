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
3. Install dependencies: `pip install -r requirements.txt`
4. Set up Alembic: `alembic init alembic` and edit `sqlalchemy.url` in `alembic.ini`
5. Migrate the database: `alembic upgrade head`
6. Run the bot: `python src/bot/main.py`
7. Run the scheduler: `python src/scheduler.py`
