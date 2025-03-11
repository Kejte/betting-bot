from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
import requests
from core.constants import REGISTRY_PROFILE_URL

class RegisterMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        return None

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        profile_exists = requests.get(REGISTRY_PROFILE_URL + str(event.from_user.id))
        if profile_exists.status_code == 400:
            json = {
                'tg_id': str(event.from_user.id)
            }
            requests.post(
                'http://app:8000/api/profiles/profile/create',
                json=json
            )
        return await handler(event, data)