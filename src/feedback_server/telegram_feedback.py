import telepot
from telepot.loop import MessageLoop

from pprint import pprint
import time
import json
from urllib.request import urlopen

TOKEN=os.getenv('TELEGRAM_BOT_TOKEN')

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

def on_callback_query(msg):
	query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
	print('Callback Query:', query_id, chat_id, query_data)
	if query_data=='yes':
		print("YES")
        #TODO: insert mongodb update query
	elif query_data=='info':
		info=json.dumps(bot.getUpdates(),sort_keys=True, indent=4)
		print("NO")
        #TODO: insert mongodb update query

bot = telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': on_chat_message,
				  'callback_query': on_callback_query}).run_as_thread() 
print('Listening ...')


while 1:
	time.sleep(10)