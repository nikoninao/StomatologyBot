from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
import time


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: int = 10):
        self.rate_limit = rate_limit
        self.users: Dict[int, float] = {}

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        current_time = time.time()

        if user_id in self.users:
            last_time = self.users[user_id]
            if current_time - last_time < 60 / self.rate_limit:
                return await event.reply("Слишком много сообщений. Подожди немного.")

        self.users[user_id] = current_time
        return await handler(event, data)