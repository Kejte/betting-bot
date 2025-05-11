from aiogram import Bot
from utils.caching import redis_client
import logging
import asyncio
import json
from core.handlers import get_max_money_fork

logger = logging.getLogger(__name__)

class RedisEventBroker:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.redis = redis_client
        self.pubsub = self.redis.pubsub()
        self.handlers = {
            'send_fokrs_to_private_group': self.send_fokrs_to_private_group
        }

    async def connect(self):
        """Подключение к Redis каналу"""
        self.pubsub.subscribe('aiogram_events')
        logger.info("Connected to Redis channel 'aiogram_events'")

    async def listen(self):
        """Основной цикл прослушивания сообщений"""
        try:
            await self.connect()
            while True:
                message = self.pubsub.get_message(
                    ignore_subscribe_messages=True,
                    timeout=1
                )
                if message:
                    await self.process_event(message['data'])
                await asyncio.sleep(5)
        except Exception as e:
            logger.error(f"Redis listener error: {e}")
        finally:
            await self.close()

    async def process_event(self, raw_data):
        """Обработка входящего события"""
        try:
            event = json.loads(raw_data)
            logger.debug(f"Received event: {event}")
            
            handler = self.handlers.get(event.get('type'))
            if handler:
                await handler(event.get('payload', {}))
            else:
                logger.warning(f"No handler for event type: {event.get('type')}")
                
        except json.JSONDecodeError:
            logger.error("Invalid JSON format in message")
        except Exception as e:
            logger.error(f"Error processing event: {e}")

    async def send_fokrs_to_private_group(self, payload: dict):
        """Обработчик для отправки сообщений"""
        try:
            await get_max_money_fork(self.bot)
            logger.info(f"Forks sended to private group")
        except KeyError as e:
            logger.error(f"Missing key in payload: {e}")
        except Exception as e:
            logger.error(f"Failed to send message: {e}")

    async def close(self):
        """Корректное закрытие соединений"""
        try:
            self.pubsub.close()
            self.redis.close()
            logger.info("Redis connections closed")
        except Exception as e:
            logger.error(f"Error closing connections: {e}")
