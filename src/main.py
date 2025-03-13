import asyncio
import random
from typing import TYPE_CHECKING

import sentry_sdk

from answers import (
    EMPTY_RETRIEVAL,
    ERROR_MSG,
    FORBIDDEN_PEOPLE,
    ON_MSG,
    PRIVATE_MESSAGES,
)
from config import bot, settings
from db import get_user, register_user
from exceptions import EmptyRetrievalError, LimitExceededError
from services import process_query

if TYPE_CHECKING:
    from telebot.types import Message


sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    send_default_pii=True,
    traces_sample_rate=1.0,
    enable_tracing=True,
)


# /start
@bot.message_handler(commands=["start"])
async def handle_start(message: "Message") -> None:
    if await register_user(
        message.from_user.id,
        message.from_user.first_name,
        message.from_user.last_name,
        message.from_user.username,
        ["default"],
    ):
        await bot.send_message(chat_id=message.chat.id, text=random.choice(ON_MSG))
    else:
        await bot.send_message(chat_id=message.chat.id, text=random.choice(ON_MSG))


# /info
@bot.message_handler(commands=["info"])
async def handle_info(message: "Message") -> None:
    await bot.send_message(chat_id=message.chat.id, text=message.from_user.id)


# /id
@bot.message_handler(commands=["id"])
async def handle_id(message: "Message") -> None:
    await bot.send_message(chat_id=message.chat.id, text=message.chat.id)


# Text handler
@bot.message_handler(content_types=["text"])
async def handle_message(message: "Message") -> None:  # noqa: C901
    try:
        user = await get_user(message.from_user.id)
        user_approved = user.approved if user is not None else False

        if message.chat.type != "supergroup" and not user_approved:
            await bot.send_message(message.chat.id, random.choice(PRIVATE_MESSAGES))
            return

        if message.chat.type == "private" and user_approved:
            query = message.text.strip()
            await process_query(message=message, query=query, partition=user.roles)
            return

        if str(message.chat.id) not in settings.CHAT_IDS:
            await bot.send_message(message.chat.id, random.choice(FORBIDDEN_PEOPLE))
            return

        if " " not in message.text:
            return

        username = await bot.get_me()
        bot_username, query = message.text.strip().split(" ", maxsplit=1)
        if bot_username == f"@{username.username}":
            if not user_approved:
                # await bot.reply_to(message, random.choice(FORBIDDEN_PEOPLE))  # noqa: E501, ERA001
                await process_query(message=message, query=query, partition=None)
                return

            if user_approved:
                await process_query(message=message, query=query, partition=None)
    except EmptyRetrievalError:
        await bot.reply_to(message, random.choice(EMPTY_RETRIEVAL))
    except LimitExceededError:
        await bot.reply_to(
            message,
            "Daily limit has been exceeded, try again tomorrow.",
        )
    except Exception as e:
        sentry_sdk.capture_exception(e)
        await bot.reply_to(message, random.choice(ERROR_MSG))


if __name__ == "__main__":
    asyncio.run(bot.polling())
