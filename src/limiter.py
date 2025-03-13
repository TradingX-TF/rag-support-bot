import asyncio
import time

from limits import parse
from limits.aio.storage import MemoryStorage
from limits.aio.strategies import MovingWindowRateLimiter

from exceptions import LimitExceededError

limits_storage = MemoryStorage()
moving_window = MovingWindowRateLimiter(limits_storage)

# 2 RPM 1000 req/day for gemini-1.5-pro
# 15 RPM 1500 req/day for gemini-2.0-flash
two_per_minute = parse("2/minute")
thousand_per_day = parse("1000/day")

# 10 / m for Developer Plan and 500 / m for Starter Plan
ten_per_minute = parse("10/minute")


async def check_ai_quota() -> bool:
    if not await moving_window.test(thousand_per_day, "AI_RPD"):
        msg = "Daily limit has been exceeded, try again tomorrow."
        raise LimitExceededError(msg)
    if not await moving_window.test(two_per_minute, "AI_RPM"):
        asyncio.sleep(
            moving_window.get_window_stats(two_per_minute, "AI_RPM").reset_time
            - time.time(),
        )
    await moving_window.hit(thousand_per_day, "AI_RPD")
    await moving_window.hit(two_per_minute, "AI_RPM")
    return True


async def check_retrievals_quota() -> bool:
    if not await moving_window.test(ten_per_minute, "RETRIEVALS_RPD"):
        asyncio.sleep(
            moving_window.get_window_stats(ten_per_minute, "RETRIEVALS_RPD").reset_time
            - time.time(),
        )
    await moving_window.hit(ten_per_minute, "RETRIEVALS_RPD")
    return True
