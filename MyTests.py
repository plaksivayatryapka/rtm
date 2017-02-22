import re
import sys
import random
import time
import telepot
from pprint import pprint

global games_list
games_list = []

class game(object):
    def __init__(self):
        self.__game_id__ = 0
        self.__players__ = {217967871:{'name': 'slavik',
                                        'alive': 1,
                                        'vote_kill': None,
                                        'maf': None,
                                        'check_maf': None,
                                        'cure': None
                            }          }
        self.__player_num__ = 0
    def add_player(self, player_id):
        self.__players__[player_id] = { 'name': 'Player_' + str(self.__player_num__+1),
                                        'alive': 1,
                                        'vote_kill': None,
                                        'maf': None,
                                        'check_maf': None,
                                        'cure': None
                                      }
        self.__player_num__ += 1



def countdown(sec, verbose, players):
    for i in range(sec):
        for addr in list(players.keys()):
            if verbose:
                bot.sendMessage(addr, str(i+1))
        time.sleep(1)

def main(msg):
    content_type, chat_type, chat_id = telepot.glance(msg) # расшифровка сообщения
    if content_type == 'text':

        if (msg['text'] == '/start_game'):  # Хостится игра
            host = chat_id
            game_id = random.randrange(0,100)
            print('game ' + str(game_id) + ' starting...')
            global g
            g = game()
            g.__game_id__ = game_id
            games_list.append((game_id))
            bot.sendMessage(chat_id, 'game ' + str(game_id) + ' starting')

        if (msg['text'] == '/game_list'):  # Проверка списка игр
            bot.sendMessage(chat_id, str(games_list))

        if (msg['text'] == '/player_list'):  # Проверка списка игроков
            if ('g' in globals()):
                bot.sendMessage(chat_id, list(g.__players__.keys()))

        if (msg['text'] == '/player_names'):  # Проверка списка игроков
            if ('g' in globals()):
                for id in g.__players__:
                    bot.sendMessage(chat_id, g.__players__[id]['name'])

        if (msg['text'] == '/countdown'):  # Всем 3-х секундное ожидание
            if ('g' in globals()):
                countdown(3, 1, g.__players__)

        m = re.search('/change_name ', msg['text'])  # Смена имени
        if (m != None):
            new_name = (msg['text'][m.span()[1]:])
            if ('g' in globals()):
                g.__players__[chat_id]['name'] = new_name



        m = re.search('/connect ', msg['text']) # Коннект к игре
        if (m != None):
            connect_to = int(msg['text'][m.span()[1]: ])
            if (connect_to in games_list):
                if (g.__players__ == {}):
                    bot.sendMessage(chat_id, 'connected')
                    g.add_player(chat_id) # добавляем игрока
                elif (chat_id not in list(g.__players__.keys())):
                    bot.sendMessage(chat_id, 'connected')
                    g.add_player(chat_id) # добавляем игрока
                else:
                    bot.sendMessage(chat_id, 'you are already connected')





token = '371150676:AAFNeZ7lPfeuftBxUaXuc_Drrj6jgzvW4rA'
bot = telepot.Bot(token)
# Очистка кэша
onstart_update = bot.getUpdates()
if (onstart_update != []):
    update_id = int(onstart_update[-1].get('update_id')) + 1
    bot.getUpdates(offset=update_id)

# Основной луп
bot.message_loop(main)
print('waiting for game ...')



# Keep the program running.
while 1:
    time.sleep(10)