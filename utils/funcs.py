from utils.caching import cache_forks, get_cached_fork_data
from utils.parser import parse_fork
import importlib
from core.constants import TARIFFS_URL, SECRET_KEY
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
    if 'olimp' != booker:
        profit_on_freebet_bet = freebet * (max(float(fork['coef_on_first_booker']),float(fork['coef_on_second_booker']))-1)
        money_bet = profit_on_freebet_bet / min(float(fork['coef_on_first_booker']),float(fork['coef_on_second_booker']))
        garanted_profit = profit_on_freebet_bet - money_bet
        percents = garanted_profit/(freebet/100)
    else:
        if 'olimp' in fork['first_booker']:
            profit_on_freebet_bet = freebet * (float(fork['coef_on_first_booker'])-1)
            money_bet = profit_on_freebet_bet / float(fork['coef_on_second_booker'])
        else:
            profit_on_freebet_bet = freebet * (float(fork['coef_on_second_booker'])-1)
            money_bet = profit_on_freebet_bet / float(fork['coef_on_first_booker'])
        garanted_profit = profit_on_freebet_bet - money_bet
        percents = garanted_profit/(freebet/100)
    return money_bet,garanted_profit,percents

def get_freebet_forks(bookers: str, max_coeff: float, freebet: int):
    freebet_forks = get_cached_fork_data(f'FREEBET_{bookers.split('_')[0]}_{max_coeff}')
    if not freebet_forks:
        forks = get_cached_fork_data(bookers)
        if not forks:
            module = importlib.import_module('core.constants')
            url = getattr(module,bookers)
            forks = parse_fork(url)
            cache_forks(forks, bookers)
        booker = bookers.split('_')[0].lower()
        if not 'olimp' in bookers.split('_')[0].lower():
            forks = [fork for fork in forks if (booker in fork['first_booker'].lower() and float(fork['coef_on_first_booker']) > 2.05 and float(fork['coef_on_first_booker']) <= max_coeff) or (booker in fork['second_booker'].lower() and float(fork['coef_on_second_booker'])> 2.05 and float(fork['coef_on_second_booker']) <= max_coeff)] 
        else:
            forks = [fork for fork in forks if (booker in fork['first_booker'].lower() and float(fork['coef_on_first_booker']) > 1.6 and float(fork['coef_on_first_booker']) <= max_coeff) or (booker in fork['second_booker'].lower() and float(fork['coef_on_second_booker'])> 1.6 and float(fork['coef_on_second_booker']) <= max_coeff)] 
        forks = sorted(forks, key=lambda fork: calculate_freebet_profit(fork,freebet,booker), reverse=True)
        cache_forks(forks, f'FREEBET_{bookers.split('_')[0]}_{max_coeff}')
        return forks
    return freebet_forks

def get_tariffs():
    return requests.get(TARIFFS_URL,headers={'Secret-Key': SECRET_KEY}).json()
