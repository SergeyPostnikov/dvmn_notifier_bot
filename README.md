# Devman taskcheck Notifier Telegram Bot
This bot notifies about tasks completion in dvmn.org by telegram.
 
## Getting started


### Get config vars

Get your **Telegram chat ID** via [userinfobot](https://telegram.me/userinfobot).

Create your Telegram Bot via [BotFather](https://telegram.me/BotFather) and get a **bot token** to access the HTTP API.

Get your **Devman Authorization token** on [devman API website](https://dvmn.org/api/docs/).

As a result of the steps above you will have 3 config vars:

```
DVMN_API_KEY - your devman api key  
TG_BOT_KEY - your bot api key
TG_USER_ID - your telegram id
```
save them in .env file

### Requirements
for work you had to have `python3`

### Installation
execute next commands

```
git clone https://github.com/SergeyPostnikov/dvmn_notifier_bot.git
cd dvmn_notifier_bot
pip install -r requirements.txt
```
### Activate your bot

```
python3 main.py
```
