# RAG knowledge bot

![Python](https://img.shields.io/badge/Python-3.12-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue)

## Usage

### General settings

1. Get API keys: [@BotFather](https://t.me/BotFather), [Gemini](https://ai.google.dev/), [Ragie](https://www.ragie.ai/), [Sentry](https:/sentry.io/)
2. Connect knowledge base at [Ragie.ai](https://www.ragie.ai/)
3. Connect database.
4. Edit `.env`
5. Edit config.py
6. Deploy

Example of `.env` file:

```text
GOOGLE_API_KEY=
RAGIE_API_KEY=
TG_API_TOKEN=
SENTRY_DSN=
DATABASE_URL=postgresql+psycopg://
CHAT_IDS=-100,-101
```

After starting, you need to manually use `/start` to initiate the bot and approve, and edit roles in the database.

Settings to edit in `config.py`

`REWRITE_PROMPT` set to True if you want improve quality of questions.

### Bot usage

1. Add `@your_telegram_bot` to the group
2. Bot only answer if you mention him.

Example: `@your_telegram_bot Какую биржу выбрать?`

## Docs

[pyTelegramBotAPI](https://pytba.readthedocs.io/en/latest/) \
[Google Gen AI SDK](https://github.com/googleapis/python-genai) \
[telegramify_markdown](https://github.com/sudoskys/telegramify-markdown) \
[Ragie](https://github.com/ragieai/ragie-python), [Rate limits](https://docs.ragie.ai/docs/rate-limits) \
[Sentry](https://docs.sentry.io/platforms/python/) \
[Tenacity](https://tenacity.readthedocs.io/en/latest/) \
[limits](https://limits.readthedocs.io/en/stable/async.html) \
[SQLAlchemy](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)

## Useful links

### Low-cost cloud

[Fly.io](https://fly.io/) \
[Render](https://render.com/) \
[Railway](https://railway.com/) \
[porter](https://cloud.porter.run/) \
[DigitalOcean](https://m.do.co/c/58a27c657ed8)

### Vector DB

[Qdrant](https://qdrant.tech/) \
[LanceDB](https://lancedb.com/) \
[supabase](https://supabase.com/modules/vector) \
[Pinecone](https://www.pinecone.io/) \
[Chroma](https://www.trychroma.com/) \
[Neon x pgvector](https://neon.tech/)

### RAG

[Advanced RAG Techniques](https://github.com/NirDiamant/RAG_Techniques) \
[Massive Multilingual Text Embedding Benchmark](https://huggingface.co/spaces/mteb/leaderboard) \
[All RAG Techniques](https://github.com/FareedKhan-dev/all-rag-techniques)
