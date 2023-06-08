from dotenv import load_dotenv
import os
from requests.exceptions import ReadTimeout, ConnectionError
from time import sleep
from dvmn_handlers import get_polling
import asyncio
import telegram


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


async def send_message(bot, tg_user_id, response):
    message_text = await get_message(response)
    await bot.send_message(
        text=message_text,
        chat_id=tg_user_id,
        parse_mode='html'
    )
    print(message_text)


async def main():
    load_dotenv()
    api_key = os.getenv('DVMN_API_KEY')
    tg_user_id = os.getenv('TG_USER_ID')
    tg_token = os.getenv('TG_BOT_KEY')
    bot = telegram.Bot(token=tg_token)

    last_attempt_timestamp = None
    while True:
        try:
            response = get_polling(api_key, last_attempt_timestamp)
            if response["status"] == "timeout":
                last_attempt_timestamp = response["timestamp_to_request"]
            else:
                await send_message(bot, tg_user_id, response)
                last_attempt_timestamp = response["last_attempt_timestamp"]
                response = get_polling(api_key, last_attempt_timestamp)
        except ReadTimeout:
            print('Polling time exceeded')
        except ConnectionError as err:
            for n in range(3):
                sleep(30)
                if n <= 3:
                    response = get_polling(api_key, last_attempt_timestamp)
                    await send_message(bot, tg_user_id, response)
                else:
                    print(err)


asyncio.run(main())
