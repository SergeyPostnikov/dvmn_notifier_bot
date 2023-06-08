from dotenv import load_dotenv
import os
from requests.exceptions import ReadTimeout, ConnectionError
from time import sleep
from dvmn_handlers import get_polling
import asyncio
import telegram
import pprint


async def get_message(response):
    return pprint.pformat(response)


async def send_message(bot, tg_user_id, response):
    message_text = await get_message(response)
    await bot.send_message(
        text=message_text,
        chat_id=tg_user_id
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
                last_attempt_timestamp = response["last_attempt_timestamp"]
                # response = get_polling(api_key, last_attempt_timestamp)
                await send_message(bot, tg_user_id, response)
        except ReadTimeout:
            print('Polling time exceeded')
        # except ConnectionError as err:
        #     for n in range(3):
        #         sleep(30)
        #         if n <= 3:
        #             response = get_polling(api_key, last_attempt_timestamp)
        #             await send_message(bot, tg_user_id, response)
        #         else:
        #             print(err)


asyncio.run(main())
