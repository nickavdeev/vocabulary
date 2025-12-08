# @VocabMateBot
[Telegram bot](https://t.me/VocabMateBot) for repeating words based on the [forgetting curve](https://en.wikipedia.org/wiki/Forgetting_curve).

## Installation
1. Clone this repository:
    ```bash
    git clone https://github.com/nickavdeev/vocabulary.git
    ```
2. Create `.env` file in the root of the project and fill it with the variables from `.env.example`:
    ```bash
    cp .env.example .env
    ```
3. Install dependencies using UV:
    ```bash
    uv sync
    ```
4. Create `alembic.ini` in root and set up `sqlalchemy.url`
5. Migrate the database: `alembic upgrade head`
6. Run the bot: `uv run python src/bot/main.py`
7. Run the scheduler: `uv run python src/scheduler.py`

## How to Create New Migrations
1. Add or edit fields in `db.models`
2. Create a new migration: `alembic revision -m "<your comment>"`
3. Define your changes in `upgrade()` and `downgrade()`
4. Apply the changes: `alembic upgrade head`
