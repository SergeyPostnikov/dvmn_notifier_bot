from dotenv import load_dotenv
import os
import requests
from pprint import pprint
from requests.exceptions import ReadTimeout, ConnectionError
from time import sleep


def get_reviews(api_key):
    url = 'https://dvmn.org/api/user_reviews/'
    headers = {'Authorization': f'Token {api_key}'}
    response = requests.get(
        url, 
        headers=headers
        )
    response.raise_for_status()
    return response.json()


def get_polling(api_key):
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {api_key}'}
    while True:
        response = requests.get(
            url, 
            headers=headers,
            timeout=60
            )
        response.raise_for_status()
        pprint(response.json())


def main():
    load_dotenv()
    api_key = os.getenv('DVMN_API_KEY')
    
    try:
        get_polling(api_key)
    except ReadTimeout:
        print('Polling time eceeded')
    except ConnectionError as err:
        for n in range(3):
            sleep(30)
            if n <= 3: 
                get_polling(api_key)
            else:
                print(err)


main()