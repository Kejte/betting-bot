from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
import requests
from core.constants import REGISTRY_PROFILE_URL, CREATE_PROFILE_URL, SECRET_KEY

class RegisterMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        return None

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        profile_exists = requests.get(REGISTRY_PROFILE_URL + str(event.from_user.id), headers={'Secret-Key': SECRET_KEY})
        if profile_exists.status_code == 400:
            json = {
                'tg_id': str(event.from_user.id)
            }
            requests.post(
                CREATE_PROFILE_URL,
                json=json,
                headers={'Secret-Key': SECRET_KEY}
            )
        return await handler(event, data)