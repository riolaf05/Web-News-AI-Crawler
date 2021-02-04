import os
import telepot
from telepot.loop import MessageLoop
import pymongo
from pprint import pprint
import time
import json
from urllib.request import urlopen
import configparser

TOKEN=os.getenv('TELEGRAM_BOT_TOKEN')

config = configparser.ConfigParser()
config.read('config.ini')

mongo_url = config['mongodb']['mongo_url']
mongo_port = config['mongodb']['mongo_port']
database_name = config['mongodb']['database_name']
collection_name = config['mongodb']['collection_name']

def update_mongo(msg, like):
    #connect to mongoDB
    myclient = pymongo.MongoClient("mongodb://{}:{}/".format(mongo_url, mongo_port))
    mydb = myclient[database_name]
    mycol = mydb[collection_name]
    #update
    myquery = { "url": msg }
    newvalues = { "$set": { "like": like } }
    mycol.update_one(myquery, newvalues)

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

def on_callback_query(msg):
    query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, chat_id, query_data)
    if query_data=='like':
        update:mongo( msg['message']['text'], True)
    elif query_data=='dislike':
        #info=json.dumps(bot.getUpdates(),sort_keys=True, indent=4)
        update:mongo( msg['message']['text'], False)

bot = telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread() 
print('Listening ...')


while 1:
    time.sleep(10)
