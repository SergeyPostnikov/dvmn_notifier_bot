from dotenv import load_dotenv
import os
from requests.exceptions import ReadTimeout, ConnectionError
from time import sleep
import asyncio
import telegram
import requests


def get_check(api_key, last_attempt_timestamp):
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


async def get_message(response):
    attempt = response['new_attempts'][0]
    title = attempt['lesson_title']
    link = attempt['lesson_url']
    is_negative = (attempt['is_negative'] == "False")
    message = \
        f'Your lesson <a href="{link}">"{title}"</a> \
        was valdated with result - ' + \
        ' "approved"' * is_negative +\
        ' "not approved"' * (not is_negative)
    return message


async def do_poll(api_key, tg_user_id, last_attempt_timestamp, bot):
    while True:
        try:
            response = get_check(api_key, last_attempt_timestamp)
            if response["status"] == "timeout":
                last_attempt_timestamp = response["timestamp_to_request"]
            else:
                message_text = await get_message(response)
                await bot.send_message(
                    text=message_text,
                    chat_id=tg_user_id,
                    parse_mode='html'
                )
                last_attempt_timestamp = response["last_attempt_timestamp"]
                response = get_check(api_key, last_attempt_timestamp)
        except ReadTimeout:
            pass
        except ConnectionError:
            sleep(30)


if __name__ == '__main__':
    load_dotenv()
    api_key = os.getenv('DVMN_API_KEY')
    tg_user_id = os.getenv('TG_USER_ID')
    tg_token = os.getenv('TG_BOT_KEY')
    bot = telegram.Bot(token=tg_token)

    last_attempt_timestamp = None

    asyncio.run(do_poll(api_key, tg_user_id, last_attempt_timestamp, bot))
