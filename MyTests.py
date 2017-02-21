import sys
import random
import time
import telepot
from pprint import pprint



def wait4game(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    if content_type == 'text':
        if (msg['text'] == 'game'):
            game_id = int(str(chat_id) + str(random.randrange(0,100)))
            bot.sendMessage(chat_id, str(game_id))
            return game_id





token = '371150676:AAFNeZ7lPfeuftBxUaXuc_Drrj6jgzvW4rA'
bot = telepot.Bot(token)
onstart_update = bot.getUpdates()
if (onstart_update != []):
    update_id = int(onstart_update[-1].get('update_id')) + 1
    bot.getUpdates(offset=update_id)
#help_for_bot_programmer = onstart_update[-1].get('message').get('from').get('id')
#bot.sendMessage(help_for_bot_programmer, 'your id (last message in botchat) is %s' % help_for_bot_programmer)
#print('last update id = ', update_id)

gameid = bot.message_loop(wait4game)
print('waiting for game ...')
if (gameid != None):
    print('game ' + str(gameid) +' starting...')
# Keep the program running.
while 1:
    time.sleep(10)