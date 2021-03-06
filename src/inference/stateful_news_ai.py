#reader
#Thanks to: https://alvinalexander.com/python/python-script-read-rss-feeds-database
import sys
sys.path.insert(1, '/opt/conda/lib/python3.6/site-packages')
import feedparser
import time
#from subprocess import check_output
import telepot
import requests
import json
import re
import os
import io
#import pandas as pd
#import tensorflow as tf
import keras
from keras.models import load_model
from keras import backend as K
import numpy as np
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import configparser
import pymongo

model = None

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

config = configparser.ConfigParser()
config.read('config.ini')

mongo_url = config['mongodb']['mongo_url']
mongo_port = config['mongodb']['mongo_port']
database_name = config['mongodb']['database_name']
collection_name = config['mongodb']['collection_name']

def filter_data(string):
    '''
    Removes usless characters
    '''
    filtered = string.replace('<p class="p1"><span class="s1">',' ')
    filtered = filtered.replace('<p ',' ')
    filtered = filtered.replace('<dev>',' ')
    return filtered

def preprocess_data(stored_contents):
    from keras.preprocessing.text import text_to_word_sequence, one_hot
    from keras.preprocessing.sequence import pad_sequences

    #see: https://machinelearningmastery.com/prepare-text-data-deep-learning-keras/

    # tokenize the document
    word_sequence=text_to_word_sequence(filter_data(stored_contents))
    words = set(word_sequence) #set() "groups by" the characters filtering duplicaded ones
    vocab_size=len(words) #getting vocabulary size, this will be the input
    tokenized_array=one_hot(stored_contents, round(vocab_size)) #one hot encoding input data

    #data_to_predict = pad_sequences(tokenized_array, maxlen = 9000)
    #return data_to_predict
    return tokenized_array

def send_message(news_url):
    bot = telepot.Bot(TELEGRAM_BOT_TOKEN)
    chat_id=TELEGRAM_CHAT_ID
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='like', callback_data='yes'), InlineKeyboardButton(text='dont like', callback_data='yes')]])
    bot.sendMessage(chat_id, news_url, reply_markup=keyboard)

def send_data_to_ai(model, content):
    print('\n')
    print("Content: ", content)
    data = {"success": False, "predictions": []}
    data_to_predict=preprocess_data(content)
    print('\n')
    print("Predicting..")
    model._make_predict_function()
    results = model.predict( np.array( [data_to_predict,] ))
    print('\n')
    print("Result: ", results)
    print('\n')
    data["predictions"] = []
    for prob in results:
        r = float(prob)
        data["predictions"].append(r)
    # indicate that the request was a success
    data["success"] = True
    return data['predictions'][0]

def write_mongo(link, text):
    myclient = pymongo.MongoClient("mongodb://{}:{}/".format(mongo_url, mongo_port))
    mydb = myclient[database_name]
    mycol = mydb[collection_name]
    mydict = {
              "url" : link,
              "text" : text,
              "like" : False
              }
    try:
        mydoc = mycol.find({"url": link})
        if mydoc.count() != 0:
            myquery = { "url": link }
            newvalues = { "$set": { "text" : text, "like": False } }
            mycol.update_one(myquery, newvalues)
        else:
            x = mycol.insert_one(mydict)
    except Exception as e:
        print(e)

# Open the rss file with read only permit and read line by line
f = open('feed_list.txt', "r")
lines = f.readlines()

print('\n')
print("Loading model..")
model=load_model('models/rss_model.h5') #requieres keras 2.2.4!!!

#Test
#feed = feedparser.parse('http://techcrunch.com/feed/')
#feed_name=feed['feed']['title']

for url in lines:
    try:
        print('\n')
        print("Reading: ", url)
        feed = feedparser.parse(url)
        feed_name=feed['feed']['title']
        print('\n')
        print("##########Reading feed: ", feed_name)
        print('\n')
        for post in feed.entries:
            print("Title: ", post['title'])
            if re.match(r'^TechCrunch', post['title']): #TODO add more feeds to parse
                if send_data_to_ai(post['content'][0]['value']) > 0.7:
                    write_mongo(post['link'], post['content'][0]['value']) #TODO send to nosql db after interence (change?)
                    send_message(post['link'])
                print('\n')
            else:
                if send_data_to_ai(model, post['summary']) > 0.7:
                    write_mongo(post['link'], post['summary']) #TODO send to nosql db after interence (change?)
                    send_message(post['link'])
                print('\n')
    except Exception as e:
        print("Error while reading feed", feed_name)
        print("Exception: ", e)
