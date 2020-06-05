# Web-News-AI-Crawler
This is a web crawler which uses AI to filter most interesting news from the internet 

### Run:

from ARM (i.e. RaspberryPi):

```console
docker run -it --rm --name = ai_news -e TELEGRAM_BOT_TOKEN = '<token>' -e TELEGRAM_CHAT_ID='<id>' rio05docker/ai_news_server:rpi3_develop_89714b6a3deaedd9672f73525ccc435cac5cd9ee
```

from x86:

```console
docker run -it --rm -v /usr/bin/qemu-arm-static:/usr/bin/qemu-arm-static --name = ai_news -e TELEGRAM_BOT_TOKEN = '<token>' -e TELEGRAM_CHAT_ID='<id>' rio05docker/ai_news_server:rpi3_develop_89714b6a3deaedd9672f73525ccc435cac5cd9ee
```

**Note:**

to send news to **Telegram bot** you must set Telegram secrets into `secrets.yaml" file. Those secret must be encoded in base64:

```console
echo -n "XXX:YYYY" | base64 
```

where XXX:YYYY is Telegram Bot ID.

To get Telegram group ID, add bot to group then go to:

```console
https://api.telegram.org/boXXX:YYY/getUpdates
```
