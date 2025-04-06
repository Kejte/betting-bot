from core.constants import SUREBET_EMAIL, SUREBET_PASSWORD, SUREBET_SIGN_IN_URL
import requests
from bs4 import BeautifulSoup

class SessionGenerator:
    
    _session = None

    @classmethod
    def get_session(cls, permission: str = None):
        if permission == 'free':
            return requests.Session()
        if not cls._session:
            header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 YaBrowser/25.2.0.0 Safari/537.36'}

            cls._session = requests.Session()
            cls._session.headers.update({'Referer':SUREBET_SIGN_IN_URL})
            auth_page = cls._session.get(SUREBET_SIGN_IN_URL, headers=header).text

            soup = BeautifulSoup(auth_page, 'lxml')

            auth_token = soup.find('main').find('div', class_='authentication-page-container').find('div', class_='authentication-page').find_all('div')[0].find('form', id='sign-in-form').find('input', {'name': 'authenticity_token'})['value']



            payload = {
                'utf8': '✓',
                'authenticity_token': auth_token,
                'user[js]': 'enabled',
                'user[email]': SUREBET_EMAIL,
                'user[password]': SUREBET_PASSWORD,
                'user[remember_me]': 1,
                'user[desirable_plan_id]': 0
            }

            log_in = cls._session.post(SUREBET_SIGN_IN_URL, data=payload)
            soup = BeautifulSoup(log_in.text, 'lxml')
        return cls._session
        
    