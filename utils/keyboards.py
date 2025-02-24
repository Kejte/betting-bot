from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def hello_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.button(text='Найти вилку', callback_data='search_vilka')
    
    builder.adjust(1)

    return builder.as_markup()