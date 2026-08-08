import logging
import time
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware


class UserActionLoggingMiddleware(BaseMiddleware):
    def __init__(self):
        self.logger = logging.getLogger("user_actions")

    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user") or getattr(event, "from_user", None)

        user_id = getattr(user, "id", None)
        username = getattr(user, "username", None)
        full_name = getattr(user, "full_name", None)

        event_type = type(event).__name__

        self.logger.info(
            "USER ACTION | user_id=%s | username=%s | full_name=%s | event=%s",
            user_id,
            username,
            full_name,
            event_type,
        )

        start = time.monotonic()

        try:
            result = await handler(event, data)
            duration = time.monotonic() - start

            self.logger.info(
                "HANDLED OK | user_id=%s | event=%s | duration=%.3fs",
                user_id,
                event_type,
                duration,
            )

            return result

        except Exception:
            self.logger.exception(
                "HANDLED ERROR | user_id=%s | event=%s",
                user_id,
                event_type,
            )
            raise