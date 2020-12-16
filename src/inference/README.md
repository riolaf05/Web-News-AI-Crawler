# Web-News-AI-Crawler
This is a web crawler which uses AI to filter most interesting news from the internet 

### Run:

#### Run on Kubernetes

Apply files into `kubernetes` folder

#### Run on Docker

from ARM (i.e. RaspberryPi):

```console
docker run -it --rm --name = ai_news -e TELEGRAM_BOT_TOKEN = '<token>' -e TELEGRAM_CHAT_ID='<id>' rio05docker/ai_news_server:stateful_arm_2020-12-16
```

from x86 with **Qemu**:

```console
docker run -it --rm -v /usr/bin/qemu-arm-static:/usr/bin/qemu-arm-static --name = ai_news -e TELEGRAM_BOT_TOKEN = '<token>' -e TELEGRAM_CHAT_ID='<id>' rio05docker/ai_news_server:stateful_arm_2020-12-16
```

**Note:**

to send news to **Telegram bot** you must set Telegram **secrets** into `secrets.yaml" file. Those secret must be encoded in base64:

To generate from console:

```console
kubectl create secret generic telegramcredentials \
  --from-literal=TELEGRAM_BOT_TOKEN='<token>' \
  --from-literal=TELEGRAM_CHAT_ID='<chat_id>'
```

To generate manually:

```console
echo -n "XXX:YYYY" | base64 
```

where XXX:YYYY is Telegram Bot ID.

To get Telegram group ID, add bot to group then go to:

```console
https://api.telegram.org/boXXX:YYY/getUpdates
```

To retrieve values:

```console
kubectl get secret telegramcredentials -o jsonpath='{.data}'
echo '<output>' | base64 --decode
```