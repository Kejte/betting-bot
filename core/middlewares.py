from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
import requests
from core.constants import REGISTRY_PROFILE_URL, CREATE_PROFILE_URL, SECRET_KEY, UPDATE_PROFILE_URL, PERMISSION_URL
from utils.keyboards import cancel_keyboard

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
        match profile_exists.status_code:
            case 400:
                json = {
                    'tg_id': str(event.from_user.id),
                    'username': '@'+str(event.from_user.username)
                }
                requests.post(
                    CREATE_PROFILE_URL,
                    json=json,
                    headers={'Secret-Key': SECRET_KEY}
                )
            case 200:
                if profile_exists.json()['username'][1:] != event.from_user.username:
                    json = {
                        'username': '@' + str(event.from_user.username),
                        'tg_id': event.from_user.id
                    }
                    req = requests.put(
                        UPDATE_PROFILE_URL + str(event.from_user.id),
                        json=json,
                        headers={'Secret-Key': SECRET_KEY}
                    )
        return await handler(event, data)

class PermissionMiddleware(BaseMiddleware):
    
    def __init__(self):
        return None
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]):
        has_permitted = requests.get(PERMISSION_URL + str(event.from_user.id),  headers={'Secret-Key': SECRET_KEY})
        if has_permitted.status_code == 200:
            return await handler(event,data)
        try:
            return await event.reply(
                'У вас нет доступа к данной функции, для его получения перейдите по кнопке настройки подписки и преобретите соответствующий тариф/активируйте пробный период',
                reply_markup=cancel_keyboard()
            )
        except AttributeError:
            return await event.answer(
                'У вас нет доступа к данной функции, для его получения перейдите по кнопке настройки подписки и преобретите соответствующий тариф/активируйте пробный период',
                True
            )