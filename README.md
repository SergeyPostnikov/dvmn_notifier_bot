# Devman taskcheck Notifier Telegram Bot
This bot notifies about tasks completion in dvmn.org by telegram.
 
## Getting started


### Get config vars

Get your **Telegram chat ID** via [userinfobot](https://telegram.me/userinfobot).

Create your Telegram Bot via [BotFather](https://telegram.me/BotFather) and get a **bot token** to access the HTTP API.

Get your **Devman Authorization token** on [devman API website](https://dvmn.org/api/docs/).

As a result of the steps above you will have 3-5 config vars:

```
DVMN_API_KEY - your devman api key  
NOTIFIER_BOT_KEY - your bot api key
LOGGER_BOT_KEY - your logger bot api key
TG_USER_ID - your telegram id
TG_ADMIN_ID - id whome to sent logs of your bot

```
save them in .env file

small notice:  
you could use same TG_ADMIN_ID and TG_USER_ID then all info will be in one profile.  
you could use same NOTIFIER_BOT_KEY and LOGGER_BOT_KEY then all info will be in one chat. 

## Run locally on pc
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
cd dvmn_bot
python3 main.py
```

## Running with Docker
The project contains a Dockerfile that allows you to create an image and container for the project.
Docker must be installed and running.

To create the image, use `docker build` with the image name specified using `-t`:
```
docker build . -t notification_bot
```

To create the container, use docker run with the container name specified using --name and the path to the .env file specified using --env-file:
```
docker run --name notification_bot --env-file=./.env -it notification_bot
```

After the container with the bot is created, it will be launched and ready to work.

