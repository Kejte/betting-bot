from utils.caching import cache_forks, get_cached_fork_data
from utils.parser import parse_fork
import importlib

def generate_fork_message(fork):
    return    (f'Событие: {fork['event']}\n\n'  
               f'Вид спорта: {fork['sport']}\n\n' 
               f'Лига/Чемпионат: {fork['championship']}\n\n'
               f'Дата начала события: {fork['start_date']}\n\n'
               f'Возраст вилки: {fork['lifetime']}\n\n'
               f'Прибыль: {fork['profit']}\n\n'
               f'Букмекеры: {fork['first_booker']} - {fork['second_booker']} \n\n'
               f'Ставка на первом букмекере: {fork['bet_on_first_booker']} коэффицент - {fork['coef_on_first_booker']}\n\n'
               f'Ставка на втором букмекере: {fork['bet_on_second_booker']} коэффицент - {fork['coef_on_second_booker']}')

def sort_freebet_forks(bookers: str, max_coeff: float):
    forks = get_cached_fork_data(bookers)
    if not forks:
        module = importlib.import_module('core.constants')
        url = getattr(module,bookers)
        forks = parse_fork(url)
        cache_forks(forks, bookers)
    return [fork for fork in forks if (fork['first_booker'] == bookers[0] + bookers.split('_')[0].lower()[1:] and float(fork['coef_on_first_booker']) > 2.1 and float(fork['coef_on_first_booker']) < max_coeff) or (fork['second_booker'] == bookers[0] + bookers.split('_')[0].lower()[1:] and float(fork['coef_on_second_booker']) > 2.1 and float(fork['coef_on_second_booker']) < max_coeff)]
