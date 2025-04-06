from utils.caching import cache_forks, get_cached_fork_data, get_cached_user
from utils.parser import parse_fork
import importlib
from core.constants import TARIFFS_URL, SECRET_KEY, TARIFF_URL, CREATE_TECH_SUPPORT_TICKET_URL, CREATE_UPDATE_TICKET_URL, GET_UPDATE_LOG_URL, CREATE_PURCHASE_REQUEST_URL, UPDATE_PAYMENT_URL, SUBSCRIPTION_URL, ACTIVATE_TRIAL_URL, PROMOCODES_URL, ACTIVATED_PROMOCODES_URL, PROMOCODE_URL, ACTIVATE_PROMOCODE_URL, GET_ACTIVATED_PROMOCODE_URL
import requests

def generate_fork_message(fork: dict):
    return    (f'Событие: {fork['event']}\n\n'  
               f'Вид спорта: {fork['sport']}\n\n' 
               f'Лига/Чемпионат: {fork['championship']}\n\n'
               f'Дата начала события: {fork['start_date']}\n\n'
               f'Возраст вилки: {fork['lifetime']}\n\n'
               f'Прибыль: {fork['profit']}\n\n'
               f'Букмекеры: {fork['first_booker']} - {fork['second_booker']} \n\n'
               f'Ставка на первом букмекере: {fork['bet_on_first_booker']} коэффицент - {fork['coef_on_first_booker']}\n\n'
               f'Ставка на втором букмекере: {fork['bet_on_second_booker']} коэффицент - {fork['coef_on_second_booker']}')

def generate_freebet_fork_message(fork: dict, freebet: int, booker: str):
    booker = booker.split('_')[0].lower()
    money_bet, garanted_profit,percents = calculate_freebet_profit(fork, freebet, booker)
    if booker in fork['first_booker'].lower():
        freebet_bet = f'Событие для фрибета: {fork['bet_on_first_booker']} коэффицент - {fork['coef_on_first_booker'] } ({fork['first_booker']})\n\n'
        fork_bet = f'Противоположная ставка: {fork['bet_on_second_booker']} коэффицент - {fork['coef_on_second_booker']} (){fork['second_booker']}\n\n'
    else:
        freebet_bet = f'Событие для фрибета: {fork['bet_on_second_booker']} коэффицент - {fork['coef_on_second_booker']} ({fork['second_booker']})\n\n'
        fork_bet = f'Противоположная ставка: {fork['bet_on_first_booker']} коэффицент - {fork['coef_on_first_booker']} ({fork['first_booker']})\n\n'
    return    (f'Событие: {fork['event']}\n\n'  
               f'Вид спорта: {fork['sport']}\n\n' 
               f'Лига/Чемпионат: {fork['championship']}\n\n'
               f'Дата начала события: {fork['start_date']}\n\n'
               f'Возраст вилки: {fork['lifetime']}\n\n'
               f'Букмекеры: {fork['first_booker']} - {fork['second_booker']} \n\n'
               f'{freebet_bet}'
               f'{fork_bet}'
               f'Сумма противоположной ставки: {round(money_bet,2)}\n\n'
               f'Доходность в процентах: {round(percents,2)}%\n\n'
               f'Прибыль: {round(garanted_profit,2)} Руб.')

def calculate_freebet_profit(fork: dict, freebet:int, booker: str):
    if booker in fork['first_booker'].lower():
            profit_on_freebet_bet = freebet * (float(fork['coef_on_first_booker'])-1)
            money_bet = profit_on_freebet_bet / float(fork['coef_on_second_booker'])
    else:
            profit_on_freebet_bet = freebet * (float(fork['coef_on_second_booker'])-1)
            money_bet = profit_on_freebet_bet / float(fork['coef_on_first_booker'])
    garanted_profit = profit_on_freebet_bet - money_bet
    percents = garanted_profit/(freebet/100)
    return money_bet,garanted_profit,percents

def get_freebet_forks(bookers: str, max_coeff: float, freebet: int, permission: str):
    freebet_forks = get_cached_fork_data(f'{permission}_FREEBET_{bookers.split('_')[0]}_{max_coeff}')
    if not freebet_forks:
        forks = get_cached_fork_data(f'{permission}_'+bookers)
        if not forks:
            module = importlib.import_module('core.constants')
            url = getattr(module,bookers)
            forks = parse_fork(url, permission=permission)
            cache_forks(forks, f'{permission}_'+bookers)
        booker = bookers.split('_')[0].lower()
        if not 'olimp' in bookers.split('_')[0].lower():
            forks = [fork for fork in forks if (booker in fork['first_booker'].lower() and float(fork['coef_on_first_booker']) > 2.05 and float(fork['coef_on_first_booker']) <= max_coeff) or (booker in fork['second_booker'].lower() and float(fork['coef_on_second_booker'])> 2.05 and float(fork['coef_on_second_booker']) <= max_coeff)] 
        else:
            forks = [fork for fork in forks if (booker in fork['first_booker'].lower() and float(fork['coef_on_first_booker']) > 1.6 and float(fork['coef_on_first_booker']) <= max_coeff) or (booker in fork['second_booker'].lower() and float(fork['coef_on_second_booker'])> 1.6 and float(fork['coef_on_second_booker']) <= max_coeff)] 
        forks = forks = [fork for fork in forks if calculate_freebet_profit(fork,freebet,booker)[-1] >= 50]
        forks = sorted(forks, key=lambda fork: calculate_freebet_profit(fork,freebet,booker), reverse=True)
        if permission == 'free':
            forks = [fork for fork in forks if calculate_freebet_profit(fork,freebet,booker)[-1] <= 60]
        cache_forks(forks, f'{permission}_FREEBET_{bookers.split('_')[0]}_{max_coeff}')
        return forks
    return freebet_forks

def get_tariffs():
    return requests.get(TARIFFS_URL,headers={'Secret-Key': SECRET_KEY}).json()

def get_tariff(id: int):
    return requests.get(TARIFF_URL + str(id),headers={'Secret-Key': SECRET_KEY}).json()

def create_tech_support_ticket(text: str, tg_id: int):
    json = {
        'profile': tg_id,
        'text': text
    }
    requests.post(
        CREATE_TECH_SUPPORT_TICKET_URL,
        json=json,
        headers={'Secret-Key': SECRET_KEY}
    )

def create_update_support_ticket(text: str, tg_id: int):
    json = {
        'profile': tg_id,
        'text': text
    }
    req = requests.post(
        CREATE_UPDATE_TICKET_URL,
        json=json,
        headers={'Secret-Key': SECRET_KEY}
    )

def get_update_log():
    return requests.get(GET_UPDATE_LOG_URL,headers={'Secret-Key': SECRET_KEY}).json()

def create_purchase_tariff(tariff: int, tg_id: int, promo: int = None):
    if promo:
        json = {
            'profile': tg_id,
            'tariff': tariff,
            'promocode': promo
        }
    else: 
         json = {
            'profile': tg_id,
            'tariff': tariff,}
    res = requests.post(CREATE_PURCHASE_REQUEST_URL, headers={'Secret-Key': SECRET_KEY}, json=json)
    return res.json()['id'] if res.status_code == 200 else False

def update_purchase_status(payment_id: int, action: str):
    requests.put(UPDATE_PAYMENT_URL + f'?payment_id={payment_id}&action={action}',headers={'Secret-Key': SECRET_KEY})

def get_subscribe(tg_id: int):
    try:
        return requests.get(SUBSCRIPTION_URL + str(tg_id),headers={'Secret-Key': SECRET_KEY}).json() 
    except requests.exceptions.JSONDecodeError:
        return

def activate_trial(tg_id: int, tariff_id: int):
    json = {
        'profile': tg_id,
        'tariff': tariff_id 
    }
    requests.post(ACTIVATE_TRIAL_URL, headers={'Secret-Key': SECRET_KEY}, json=json)

def check_trial(tg_id: int, tariff_id: int):
    return True if requests.get(ACTIVATE_TRIAL_URL + f'?tg_id={tg_id}&tariff_id={tariff_id}', headers={'Secret-Key': SECRET_KEY}).status_code == 201 else False

def get_user_permission(tg_id):
    return get_cached_user(tg_id=tg_id).split('_')[-1][:-1]

def get_promocodes(tariff_id: int):
    try:
        return requests.get(PROMOCODES_URL+f'{tariff_id}',headers={'Secret-Key': SECRET_KEY}).json()
    except Exception:
        return None

def get_promocodes_status(tariff_id: int, tg_id: int):
    res = requests.get(ACTIVATED_PROMOCODES_URL+f'?tariff_id={tariff_id}&tg_id={tg_id}',headers={'Secret-Key': SECRET_KEY})

    if res.status_code == 200:
        return True
    return False

def retrieve_promocode(promo_id: int):
    return requests.get(PROMOCODE_URL+f'{promo_id}', headers={'Secret-Key': SECRET_KEY}).json()

def activate_promocode(promo_id: int, tg_id: int):
   requests.post(
        ACTIVATE_PROMOCODE_URL,
        headers={'Secret-Key': SECRET_KEY},
        data={
          'profile': tg_id,
          'promocode': promo_id  
        }
    ).status_code == 200

def get_activated_promocode(tg_id: int, tariff_id: int):
    res = requests.get(GET_ACTIVATED_PROMOCODE_URL+f'?tg_id={tg_id}&tariff_id={tariff_id}',headers={'Secret-Key': SECRET_KEY})
    return res.json() if res.status_code == 200 else None