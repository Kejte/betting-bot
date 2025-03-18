from bs4 import BeautifulSoup
from utils.session_generator import SessionGenerator

def parse_fork(link):
    try:

        session = SessionGenerator.get_session()

        header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 YaBrowser/25.2.0.0 Safari/537.36'}
        
        responce = session.get(link, headers=header).text

        soup = BeautifulSoup(responce,'lxml')

        block = soup.find('table', id = 'surebets-table')

        bets = block.find_all('tbody', {'class': 'surebet_record'})
        result = []

        for bet in bets:
            trs = bet.find_all('tr')
            profit = trs[0].find('td', class_="profit-box").find('span', class_="profit ps-2 cursor-help").text
            start_date = trs[0].find('td', class_='time').find('abbr', class_="cursor-help").text
            lifetime = trs[0].find('span', class_='age ps-2 cursor-help').text
            sport = trs[0].find_all('span', class_="minor")[0].text
            first_booker = trs[0].find('td', class_="booker").find('a', {'rel': "noopener"}).text
            event = trs[1].find('td', {'class': 'event'}).find('a', {'target': "_blank"}).text
            championship = trs[1].find('td', {'class': 'event'}).find('span', class_="minor").text
            bet_on_first_booker = trs[0].find('td', class_="coeff").find('abbr', class_="cursor-help").get('title')
            coef_on_first_booker = trs[0].find('td', class_='value').find('div', class_="d-inline-flex align-items-center justify-content-end").find('a', class_="value_link").text
            second_booker = trs[1].find('td', class_="booker").find('a', {'rel': "noopener"}).text
            bet_on_second_booker = trs[1].find('td', class_="coeff").find('abbr', class_="cursor-help").get('title')
            coef_on_second_booker = trs[1].find('td', class_='value').find('div', class_="d-inline-flex align-items-center justify-content-end").find('a', class_="value_link").text
            start_date = start_date[:5] + ' ' +start_date[5:]
            date, time = start_date.split(' ')[0],start_date.split(' ')[-1]
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
    
    except AttributeError as e:
        print(e)
        return
        return parse_fork(link)






