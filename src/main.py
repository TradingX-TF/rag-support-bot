import asyncio
import random
from typing import TYPE_CHECKING

from answers import ERROR_MSG, FORBIDDEN_PEOPLE, ON_MSG, PRIVATE_MESSAGES
from config import bot
from services import (
    check_auth,
    process_query,
)

if TYPE_CHECKING:
    from telebot.types import Message


# /start
@bot.message_handler(commands=["start"])
async def handle_start(message: "Message") -> None:
    await bot.send_message(message.chat.id, random.choice(ON_MSG))  # noqa: S311


# /info
@bot.message_handler(commands=["info"])
async def handle_info(message: "Message") -> None:
    await bot.send_message(message.chat.id, f"{message.from_user.id}")


# Text handler
@bot.message_handler(content_types=["text"])
async def handle_message(message: "Message") -> None:
    try:
        user = check_auth(message.from_user.id)

        if message.chat.type not in ("group", "supergroup") and not user:
            await bot.send_message(message.chat.id, random.choice(PRIVATE_MESSAGES))  # noqa: S311
            return

        if message.chat.type == "private" and user:
            query = message.text.strip()
            await process_query(message=message, query=query)
            return

        if " " not in message.text:
            return

        username = await bot.get_me()
        bot_username, query = message.text.strip().split(" ", maxsplit=1)
        if bot_username == f"@{username.username}":
            if not user:
                await bot.reply_to(message, random.choice(FORBIDDEN_PEOPLE))  # noqa: S311
                return

            if user:
                await process_query(message=message, query=query)

    except Exception:
        await bot.reply_to(message, random.choice(ERROR_MSG))  # noqa: S311


if __name__ == "__main__":
    asyncio.run(bot.polling())
