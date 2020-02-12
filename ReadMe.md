# Alertmanager-Telegram gateway

Simple gateway for sending notification from Alertmanager to Telegram via webhook. 

## Requirements

- python 3.5+
- tornado 6.0.2+
- virtualenv

## Installation

```
git clone https://github.com/toxatoor/alertmanager-telegram-gw /opt/telegram-gw
virtualenv -p /usr/bin/python3.5 /opt/telegram-gw
/opt/telegram-gw/bin/pip install -r /opt/telegram-gw/requirements.txt
cp /opt/telegram-gw/telegram-gw.service /etc/systemd/system 
vi /etc/systemd/system/telegram-gw.service # change BOT_ID to valid 
systemctl daemon-reload 
systemctl enable telegram-gw.service 
systemctl start telegram-gw.service
```

Add recievers to alertmanager.yml as shown in example, prometheus rules as shown in rules.yml.

## Configuration 

Service reads configuration from environment:

- BOT_ID (required) - Telegram bot token.
- BIND_ADDR (optional, default to 127.0.0.1) - address to listen on.
- BIND_PORT (optional, default to 8888) - port to listen on.

## Alert values 

Currently it uses just a few of available fields in alertmanager's json (due to personal historical reasons):

- status (mapped to "OK/PROBLEM"). 
- labels.hostname as referred host. 
- annotations.summary as a alert message body. 

Message template is static, hardcoded. One can use [Markdown](https://core.telegram.org/bots/api#markdown-style) in summary. 

## Performance 

Not really great - around 400 msg/sec on a single-core VM. 

## Why not https://github.com/metalmatze/alertmanager-bot ?.. 

- The gateway is not really the bot - it's just a notification service.
- It sends alert directly to users, but not to the channel - to keep subscription on an alertmanager side completely. 
- As well as alert grouping, distribution to different groups of users, etc. 

## Cons

- The code is auwful.  
- Error handling is limited. 
- Might have issues with async io under heavy load. 

## TODO

- Customizable message templates. 
- Dynamic variables (labels, etc). 
- Customizable values mapping. 
- Better error handling. 
- Cleanup query rounting. 
- Check coroutine corner cases. 
