# expense-bot

## Installation

1. Clone the repository
```bash
git clone https://github.com/Moses-93/expense-bot.git
cd expense-bot
```

2. Create .env file
```bash
touch .env
```

3. Add your Telegram API token to the `.env` file

Open `.env` and paste the following:

```env
TELEGRAM_API_TOKEN=your_token_here
```

4. Create and activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

5. Install dependencies
```bash
pip install -r requirements.txt
```

6. Start the server
```bash
python -m src.main
```