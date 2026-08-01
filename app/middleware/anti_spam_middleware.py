import logging
from collections import defaultdict
import time
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from cachetools import TTLCache

logger = logging.getLogger(__name__)


class AntiSpamMiddleware(BaseMiddleware):
    """Adaptive anti-spam middleware with exponential punishment."""

    def __init__(
        self,
        limit_per_second: int = 3,
        base_block: int = 1,
        multiplier: int = 3,
        max_block: int = 300,
    ):
        """
        Args:
            limit_per_second: Allowed messages per second before triggering.
            base_block: Base block time (seconds) for the first violation.
            multiplier: Exponential growth factor for repeated spam.
            max_block: Max possible block time (seconds).
        """
        self.limit_per_second = limit_per_second
        self.base_block = base_block
        self.multiplier = multiplier
        self.max_block = max_block

        self._messages: defaultdict[int, list[float]] = defaultdict(list)
        self._violations: defaultdict[int, int] = defaultdict(int)
        self._blocked = TTLCache(maxsize=10_000, ttl=max_block + 1)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        message = event.message
        if not message or not message.from_user or message.photo:
            return await handler(event, data)

        user_id = message.from_user.id
        now = time.time()

        blocked_until = self._blocked.get(user_id)
        if blocked_until and blocked_until > now:
            return None

        timestamps = self._messages[user_id]
        timestamps.append(now)
        self._messages[user_id] = [t for t in timestamps if now - t <= 1]

        if len(self._messages[user_id]) > self.limit_per_second:
            self._violations[user_id] += 1
            strikes = self._violations[user_id]

            block_time = min(self.base_block * (self.multiplier ** (strikes - 1)), self.max_block)
            unblock_at = now + block_time
            self._blocked[user_id] = unblock_at
            await message.answer(f"⚠️ Слишком быстро! Блокировка на {block_time} сек.")
            logger.warning(
                f"SPAM BLOCKED: user_id={user_id}, strikes={strikes}, block_time={block_time} сек."
            )
            return None

        return await handler(event, data)