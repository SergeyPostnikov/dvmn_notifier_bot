from dotenv import load_dotenv
import os
from requests.exceptions import ReadTimeout, ConnectionError
from time import sleep
import telegram
import requests
import logging


logger = logging.getLogger(__file__)


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


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


def get_message(response):
    attempt = response['new_attempts'][0]
    title = attempt['lesson_title']
    link = attempt['lesson_url']
    is_negative = (attempt['is_negative'] == "False")
    message = f"Your lesson <a href='{link}'>'{title}'</a> was"
    if is_negative:
        message += ' "not approved"'
    else:
        message += ' "approved"'
    return message


def do_poll(api_key, tg_user_id, last_attempt_timestamp, bot):
    while True:
        try:
            check = get_check(api_key, last_attempt_timestamp)
            if check["status"] == "timeout":
                last_attempt_timestamp = check["timestamp_to_request"]
            else:
                message_text = get_message(check)
                last_attempt_timestamp = check["last_attempt_timestamp"]
                bot.send_message(
                    text=message_text,
                    chat_id=tg_user_id,
                    parse_mode='html'
                )
                logging.info('Update sent to user')
        except ReadTimeout:
            pass
        except ConnectionError as err:
            logging.exception(err)
            sleep(30)
        except Exception as err:
            logging.exception('Bot failed with error: ')
            logging.exception(err)


if __name__ == '__main__':
    load_dotenv()

    api_key = os.getenv('DVMN_API_KEY')
    tg_user_id = os.getenv('TG_USER_ID')
    tg_admin_id = os.getenv('TG_ADMIN_ID')
    notifier_bot_token = os.getenv('NOTIFIER_BOT_KEY')
    logger_bot_token = os.getenv('LOGGER_BOT_KEY')

    notifier_bot = telegram.Bot(token=notifier_bot_token)
    logger_bot = telegram.Bot(token=logger_bot_token)

    logging.basicConfig(level=logging.ERROR)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(TelegramLogsHandler(logger_bot, tg_admin_id))
    logger.info('Bot started')

    last_attempt_timestamp = None

    do_poll(api_key, tg_user_id, last_attempt_timestamp, notifier_bot)
