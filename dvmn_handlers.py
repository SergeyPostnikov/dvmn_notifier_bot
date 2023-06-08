import requests


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
