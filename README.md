# Web-News-AI-Crawler
This is a web crawler which uses AI to filter most interesting news from the internet 

### Installation

0. requiered: Python3 and Docker

1. Install MondgoDB and create database:

```console
docker run -d --restart=unless-stopped --name rpi3-mongodb3 --restart unless-stopped -v /home/pi/volume/mongodb/db:/data/db -v /home/pi/volume/mongodb/configdb:/data/configdb -p 27017:27017 -p 28017:28017 andresvidal/rpi3-mongodb3:latest mongod --auth 

docker exec -it rpi3-mongodb3 mongo admin

db.createUser(
  {
    user: "<user>",
    pwd: "<psw>",
    roles: [ { role: "readWrite", db: "rss_news" } ]
  }
)

db.auth("<user>", "<psw>")

```

2. Install cronjobs with sudo

3. Install dependencies:

```console
pip3 install -r requierements.txt

sudo apt-get install libatlas-base-dev libhdf5-dev python-h5py
```

4. Put writer and reader scripts into /home/pi/Scripts/

5. Start backend server: 

add the following line to: /etc/rc.local (be sure to leave the line exit 0 at the end)

```console
rm /home/pi/volume/mongodb/db/mongod.lock
nohup python3 /home/pi/Scripts/backend/api-server.py &
```

6. Add the Telegram TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID to ~/.profile

7. Reboot
