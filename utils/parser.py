import requests
from bs4 import BeautifulSoup
import fake_useragent

def parse_fork(link):
    try:
        user = fake_useragent.UserAgent().random

        header = {'user-agent': user}

        responce = requests.get(link, headers=header).text

        soup = BeautifulSoup(responce,'lxml')

        block = soup.find('table', id = 'surebets-table')

        bets = block.find_all('tbody', {'class': 'surebet_record'})
        result = []

        for bet in bets:
            trs = bet.find_all('tr')
            profit = trs[0].find('td', class_="header h0").find('span', class_="profit ps-2 cursor-help").text
            time_data = trs[0].find_all('td')[1].find('div', class_="header-data").find('span', class_="time-data")
            start_date = time_data.find('time', class_='te-time').text
            lifetime = time_data.find('span', class_='age ps-2 cursor-help').text
            sport = trs[0].find('span', class_="sport flex-grow-1").text 
            first_booker = trs[1].find('td', class_="booker").find('a', {'rel': "noopener"}).text
            event = trs[1].find('td', {'class': 'event'}).find('a', {'target': "_blank"}).text
            championship = trs[1].find('td', {'class': 'event'}).find('span', class_="minor").text
            bet_on_first_booker = trs[1].find('td', class_="coeff").find('abbr', class_="cursor-help").text
            coef_on_first_booker = trs[1].find('td', class_='value').find('div', class_="d-inline-flex align-items-center justify-content-end").find('a', class_="value_link").text
            second_booker = trs[2].find('td', class_='booker').text
            bet_on_second_booker = trs[2].find('td', class_="coeff").find('abbr', class_="cursor-help").text
            coef_on_second_booker = trs[2].find('td', class_='value').find('div', class_="d-inline-flex align-items-center justify-content-end").find('a', class_="value_link").text
            start_date = start_date.replace('\xa0',' ').replace('\n', '').strip()
            date, time = start_date.split(' ')
            if int(time.split(':')[0])+3 < 24:
                time = f'{int(time.split(':')[0])+3}:{time.split(':')[1]}'
            elif int(time.split(':')[0])+3 == 24:
                time = f'00:{time.split(':')[1]}'
            else:
                time = f'{int(time.split(':')[0])+3-24}:{time.split(':')[1]}'
            result.append({
                'profit': profit,
                'start_date': ''.join([date+' ',time]),
                'lifetime': lifetime,
                'sport': sport.replace('\n', '').strip(),
                'first_booker': first_booker,
                'event': event,
                'championship': championship,
                'bet_on_first_booker': bet_on_first_booker,
                'coef_on_first_booker': coef_on_first_booker,
                'second_booker': second_booker.replace('\n', ''),
                'bet_on_second_booker': bet_on_second_booker,
                'coef_on_second_booker': coef_on_second_booker,
            }) 

        return result
    
    except AttributeError:
        return parse_fork(link)






