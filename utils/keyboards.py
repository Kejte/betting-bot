from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.constants import BOOKERS_LIST, MANAGER


def hello_keyboard(tg_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.button(text='💲 Найти денежную вилку', callback_data='search_money_fork')
    builder.button(text='🎁 Найти фрибетную вилку', callback_data='search_freebet_fork')
    builder.button(text='🗓 Настройки подписки', callback_data='payments')

    builder.button(text='🧑‍💻 Обратная связь', callback_data='feedback')
    builder.button(text='🆕 Что нового?', callback_data='update_log')

    if tg_id == MANAGER:
        builder.button(text='Админ панель', callback_data='admin')
    
    builder.adjust(1)

    return builder.as_markup()

def bookers_list_keyboard(fork_type: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for booker in BOOKERS_LIST:
        builder.button(text=booker, callback_data=f'required_{fork_type}_{booker}')
    
    builder.button(text='⬅️ Назад в меню', callback_data='main_menu')
    
    builder.adjust(1)

    return builder.as_markup()

def optional_bookers_list_keyboard(fork_type: str, first_booker: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for booker in BOOKERS_LIST:
        if booker == first_booker:
            continue
        builder.button(text=booker, callback_data=f'selected_{fork_type}_{first_booker}_{booker}')
    
    builder.button(text='Любой', callback_data=f'selected_{fork_type}_{first_booker}_any')

    builder.button(text='🔁 Изменить выбранного букмекера', callback_data=f'search_{fork_type}_fork')
    
    builder.adjust(1)

    return builder.as_markup()
    

def money_fork_keyboard(first_booker: str, first_coef: float, second_booker: str, second_coef: float, profit: float, index: int, lenght: int, bookers: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    if index + 1 != lenght:
        builder.button(text='➡️ Следующая', callback_data=f'paginate_money_next_fork_{index+1}_{bookers}')
    if index != 0:
        builder.button(text='⬅️ Предыдущая', callback_data=f'paginate_money_previous_fork_{index-1}_{bookers}')
    builder.button(text='🧮 Рассчитать вилку', callback_data=f'calculate_money_fork_{first_booker}_{first_coef}_{second_booker}_{second_coef}_{profit}')
    builder.button(text='⬅️ Назад в меню', callback_data='main_menu')

    builder.adjust(1)

    return builder.as_markup()

def freebet_fork_keyboard(index: int, lenght: int, bookers: str, max_coeff: float, freebet: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    if index + 1 != lenght:
        builder.button(text='➡️ Следующая', callback_data=f'paginate_freebet_next_fork_{max_coeff}_{int(freebet)}_{index+1}_{bookers}')
    if index != 0:
        builder.button(text='⬅️ Предыдущая', callback_data=f'paginate_freebet_previous_fork_{max_coeff}_{int(freebet)}_{index-1}_{bookers}')
    builder.button(text='⬅️ Назад в меню', callback_data='main_menu')

    builder.adjust(1)

    return builder.as_markup()

def money_fork_calculating_keyboard(first_booker: str, first_coef: float, second_booker: str, second_coef: float, profit: float):
    builder = InlineKeyboardBuilder()

    builder.button(text='🧮 Пересчитать',callback_data=f'calculate_money_fork_{first_booker}_{first_coef}_{second_booker}_{second_coef}_{profit}')
    builder.button(text='⬅️ Назад к выбору бк', callback_data='search_freebet_fork')
    builder.button(text='⬅️ Назад в меню', callback_data='main_menu')

    builder.adjust(1)

    return builder.as_markup()

def cancel_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text='⬅️ Назад в меню', callback_data='main_menu')

    builder.adjust(1)

    return builder.as_markup()

def tariffs_keyboard(tariffs: list[dict]):
    builder = InlineKeyboardBuilder()
    
    for tariff in tariffs:
        builder.button(text=tariff['title'], callback_data=f'tariff_{tariff['id']}_{tariff['title']}')
    
    builder.button(text='⬅️ Назад в меню', callback_data='main_menu')
    
    builder.adjust(1)

    return builder.as_markup()

def payments_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text='🗓 Моя подпискa', callback_data='actual_subscribe')
    builder.button(text='📋 Тарифы', callback_data='tariffs')
    builder.button(text='⬅️ Назад в меню', callback_data='main_menu')

    builder.adjust(1)

    return builder.as_markup()

def tariff_keyboard(id: int):
    builder = InlineKeyboardBuilder()

    builder.button(text='💳 Купить', callback_data=f'pre_purchase_tariff_{id}')
    # if check_trial(tg_id,id):
    #     builder.button(text='Активировать пробный период', callback_data=f'activate_trial_{id}')
    builder.button(text='💥 Промокоды', callback_data=f'promocodes_{id}')
    builder.button(text='⬅️ Назад к тарифам', callback_data='tariffs')
    builder.button(text='⬅️ Назад в меню', callback_data='main_menu')

    builder.adjust(1)

    return builder.as_markup()

def pre_purchace_keyboard(id: int,amount: int):
    builder = InlineKeyboardBuilder()

    builder.button(text='💰 Перейти к оплате', callback_data=f'purchase_tariff_{amount}_{id}')
    builder.button(text='⬅️ Назад к тарифам', callback_data='tariffs')
    builder.button(text='⬅️ Назад в меню', callback_data='main_menu')
    
    builder.adjust(1)

    return builder.as_markup()

def feedback_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text='🧑‍💻 Тех.поддержка', callback_data='tech_support')
    builder.button(text='🆕 Предложить обновление', callback_data='update_ticket')
    builder.button(text='⬅️ Назад в меню', callback_data='main_menu')

    builder.adjust(1)

    return builder.as_markup()

def purchase_request_keyboard(payment_id: int, tg_id: int):
    builder = InlineKeyboardBuilder()

    builder.button(text='Подтвердить оплату', callback_data=f'upd_payment_accept_{tg_id}_{payment_id}')
    builder.button(text='Закрыть заявку', callback_data=f'upd_payment_cancel_{tg_id}_{payment_id}')

    builder.adjust(1)

    return builder.as_markup()

def back_to_payment_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text='⬅️ Назад', callback_data='payments')
    builder.button(text='Главное меню', callback_data='main_menu')

    builder.adjust(1)

    return builder.as_markup()

def back_promocode_keyboard(tariff):
    builder = InlineKeyboardBuilder()

    builder.button(text='⬅️ Назад', callback_data=f'tariff_{tariff['id']}_{tariff['title']}')

    builder.adjust(1)

    return builder.as_markup()

def promocodes_keyboard(promocodes, tariff):
    builder = InlineKeyboardBuilder()

    for promocode in promocodes:
        builder.button(text=f'{promocode['promo']}', callback_data=f'promocode_{promocode['id']}')

    builder.button(text='⬅️ Назад', callback_data=f'tariff_{tariff['id']}_{tariff['title']}')

    builder.adjust(1)

    return builder.as_markup()

def activate_promocode_keyboard(promo_id: int, tariff_id: int):
    builder = InlineKeyboardBuilder()

    builder.button(text='🧨 Активировать', callback_data=f'activate_promo_{tariff_id}_{promo_id}')
    builder.button(text='⬅️ Назад', callback_data=f'promocodes_{tariff_id}')

    builder.adjust(1)

    return builder.as_markup()

def activated_promocode_keyboard(tariff_id: int):
    builder = InlineKeyboardBuilder()

    builder.button(text='💳 Перейти к оплате', callback_data=f'pre_purchase_tariff_{tariff_id}')
    builder.button(text='⬅️ Назад в меню', callback_data='main_menu')

    builder.adjust(1)

    return builder.as_markup()
