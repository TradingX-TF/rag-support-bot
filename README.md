# RAG knowledge bot

![Python](https://img.shields.io/badge/Python-3.12-blue)

## Usage

### General settings

1. Get API keys: [@BotFather](https://t.me/BotFather), [Gemini](https://ai.google.dev/), [Ragie](https://www.ragie.ai/), [Sentry](https:/sentry.io/)
2. Connect knowledge base at [Ragie.ai](https://www.ragie.ai/)
3. Edit `.env`
4. Edit config.py
5. Deploy

Example of `.env` file:

```text
GOOGLE_API_KEY=
RAGIE_API_KEY=
TG_API_TOKEN=
SENTRY_DSN=
AUTH_LIST=123,456
```

`AUTH_LIST` comma-separated id's, who can talk to the bot.

Settings to edit in `config.py`

`REWRITE_PROMPT` set to True if you want improve quality of questions.

### Bot usage

1. Disable `/setprivacy` in [@BotFather](https://t.me/BotFather)
2. Add [@tradingx_knowledge_bot](https://t.me/tradingx_knowledge_bot) to the group
3. Bot only answer if you mention him.

Example: `@tradingx_knowledge_bot Какую биржу выбрать?`

## Docs

[pyTelegramBotAPI](https://pytba.readthedocs.io/en/latest/) \
[Google Gen AI SDK](https://github.com/googleapis/python-genai) \
[telegramify_markdown](https://github.com/sudoskys/telegramify-markdown) \
[Ragie](https://github.com/ragieai/ragie-python)

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
[Chroma](https://www.trychroma.com/)

### RAG

[Advanced RAG Techniques](https://github.com/NirDiamant/RAG_Techniques) \
[Massive Multilingual Text Embedding Benchmark](https://huggingface.co/spaces/mteb/leaderboard)
