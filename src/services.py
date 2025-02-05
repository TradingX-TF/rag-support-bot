import asyncio
from typing import TYPE_CHECKING

from google.genai import types
from ragie import Ragie
from telebot.util import smart_split
from telegramify_markdown import markdownify

from config import (
    GEMINI_MODEL,
    SAFETY_SETTINGS,
    bot,
    client,
    settings,
)
from exceptions import EmptyRetrievalError
from prompts import QUERY_REWRITE_SYSTEM_INSTRUCTION, RAG_SYSTEM_INSTRUCTION

if TYPE_CHECKING:
    from telebot.types import Message


async def rewrite_prompt(query: str) -> str:
    query_rewrite_prompt = f"""
    Return only rewritten query and only one.
    Original query: {query}
    """
    response = await client.aio.models.generate_content(
        model="gemini-2.0-flash",
        contents=query_rewrite_prompt,
        config=types.GenerateContentConfig(
            system_instruction=QUERY_REWRITE_SYSTEM_INSTRUCTION,
            safety_settings=SAFETY_SETTINGS,
            response_mime_type="text/plain",
            max_output_tokens=8192,
        ),
    )
    if response.text is None:
        msg = "Empty response"
        raise ValueError(msg)
    return response.text


async def retrieve_data(query: str) -> list:
    async with Ragie(auth=settings.RAGIE_API_KEY) as s:
        res = s.retrievals.retrieve(
            request={
                "query": query,
                "rerank": True,
            },
        )
    chunk_text = []
    for _i, text in enumerate(res.scored_chunks):
        chunk_text.append(text.text)
    if not chunk_text:
        msg = "No retrievals for query"
        raise EmptyRetrievalError(msg)
    return chunk_text


async def answer_question(query: str, retrievals: list) -> str:
    prompt = f"""
    User asks: {query}

    Here is all of the information available to answer the user:
    ===
    {"".join(retrievals)}
    ===
    """
    response = await client.aio.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=RAG_SYSTEM_INSTRUCTION,
            safety_settings=SAFETY_SETTINGS,
            response_mime_type="text/plain",
            max_output_tokens=8192,
        ),
    )
    if response.text is None:
        msg = "Empty response"
        raise ValueError(msg)
    return response.text


async def send_answer(message: "Message", answer: str) -> None:
    answer_md = markdownify(answer)
    if len(answer_md) > 4096:  # 4096 limit # noqa: PLR2004
        chunks = smart_split(answer, 4096)
        for text in chunks:
            text_md = markdownify(text)
            await bot.reply_to(message, text_md, parse_mode="MarkdownV2")
            await asyncio.sleep(1)
    else:
        await bot.reply_to(message, answer_md, parse_mode="MarkdownV2")


async def process_query(message: "Message", query: str) -> None:
    if settings.REWRITE_PROMPT:
        query = await rewrite_prompt(query)
    retrievals = await retrieve_data(query)  # Какую биржу выбрать?
    answer = await answer_question(query=query, retrievals=retrievals)
    await send_answer(message=message, answer=answer)


def check_auth(user_id: int) -> bool:
    return str(user_id) in settings.AUTH_LIST
