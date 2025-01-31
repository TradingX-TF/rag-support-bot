import asyncio
from typing import TYPE_CHECKING

from config import REWRITE_PROMPT, bot
from services import (
    answer_question,
    check_auth,
    retrieve_data,
    rewrite_prompt,
    send_answer,
)

if TYPE_CHECKING:
    from telebot.types import Message


# /start
@bot.message_handler(commands=["start"])
async def handle_start(message: "Message") -> None:
    await bot.send_message(
        message.chat.id,
        "You are good to go!",
    )


# /info
@bot.message_handler(commands=["info"])
async def handle_info(message: "Message") -> None:
    await bot.send_message(message.chat.id, f"{message.from_user.id}")


# Text handler
@bot.message_handler(content_types=["text"])
async def handle_message(message: "Message") -> None:
    if message.chat.type not in ("group", "supergroup"):
        await bot.send_message(message.chat.id, "Я не веду приватных бесед.")
        return

    if " " not in message.text:
        return

    username = await bot.get_me()
    bot_username, query = message.text.strip().split(" ", maxsplit=1)
    if bot_username == f"@{username.username}":
        user = check_auth(message.from_user.id)
        if not user:
            await bot.reply_to(
                message,
                "Мне не разрешают общаться c незнакомыми людьми.",
            )
            return

        if user:
            if REWRITE_PROMPT:
                query = await rewrite_prompt(query)
            retrievals = await retrieve_data(query)  # Какую биржу выбрать?
            answer = await answer_question(query=query, retrievals=retrievals)
            await send_answer(message=message, answer=answer)


if __name__ == "__main__":
    asyncio.run(bot.polling())
