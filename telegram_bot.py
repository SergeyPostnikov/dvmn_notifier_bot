import telegram
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
tg_user_id = os.getenv('TG_USER_ID')
tg_token = os.getenv('TG_BOT_KEY')
bot = telegram.Bot(token=tg_token)


async def get_updates():
    updates = await bot.get_updates()
    return updates[0].message.from_user.id


async def main():
    chat_id = await get_updates()
    print(chat_id)
    status = await bot.send_message(chat_id=chat_id, text='Hi John!')
    print(status)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    