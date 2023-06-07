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
        headers=headers,
    )
    response.raise_for_status()
    return response.json()


def get_polling(api_key, last_attempt_timestamp):
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {api_key}'}
    payload = {'timestamp': last_attempt_timestamp}
    response = requests.get(
        url,
        headers=headers,
        params=payload,
        timeout=91
    )
    response.raise_for_status()
    return response.json()


def main():
    load_dotenv()
    api_key = os.getenv('DVMN_API_KEY')
    last_attempt_timestamp = None
    while True:
        try:
            response = get_polling(api_key, last_attempt_timestamp)
            if response["status"] == "timeout":
                last_attempt_timestamp = response["timestamp_to_request"]
            else:
                last_attempt_timestamp = response["last_attempt_timestamp"]
                response = get_polling(api_key, last_attempt_timestamp)
                pprint(response)
        except ReadTimeout:
            print('Polling time eceeded')
        except ConnectionError as err:
            for n in range(3):
                sleep(30)
                if n <= 3:
                    response = get_polling(api_key, last_attempt_timestamp)
                    pprint(response)
                else:
                    print(err)


main()
