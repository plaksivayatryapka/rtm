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
        self.__players__ = {}
        self.__player_num__ = 0
        self.__host__ = ''
        self.__roles__ = {
            'mafs':[],
            'cits':[],
            'docs':[],
            'coms':[]
        }
        self.__round_time__ = 5
    def add_player(self, adr):
        self.__players__[self.__player_num__ + 1] = {
                                        'adr': adr,
                                        'name': 'Player_' + str(self.__player_num__+1),
                                        'alive': 1,
                                        'vote_kill': None,
                                        'maf': None,
                                        'check_maf': None,
                                        'cure': None
                                      }
        self.__player_num__ += 1

    def everybody(self):
        return [self.__players__[i]['adr'] for i in self.__players__]

    def print_names(self, players):
        message = ''
        for player_id in self.__players__:
            message += str(player_id) + ' - ' + self.__players__[player_id]['name'] + ' \n'
        for id in players:
            bot.sendMessage(id, message)

    def countdown(self, sec, verbose, players):
        for i in range(sec):
            for addr in players:
                if verbose:
                    bot.sendMessage(addr, str(sec - i))
            time.sleep(1)

    def get_id(self, adr):
        for id in self.__players__:
            if (adr == self.__players__[id]['adr']):
                return id
        return 0

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
            g.__host__ = host
            g.add_player(host)
            games_list.append((game_id))
            bot.sendMessage(chat_id, 'game ' + str(game_id) + ' starting')

        if (msg['text'] == '/game_list'):  # Проверка списка игр
            bot.sendMessage(chat_id, str(games_list))

        if (msg['text'] == '/players_adr'):  # Проверка айдишников игроков
            if ('g' in globals()):
                bot.sendMessage(chat_id, g.everybody())

        if (msg['text'] == '/player_names'):  # Проверка списка игроков
            if ('g' in globals()):
                g.print_names([chat_id])

        if (msg['text'] == '/countdown'):  # Всем 3-х секундное ожидание
            if ('g' in globals()):
                g.countdown(3, 1, g.everybody())



        m = re.search('/change_name ', msg['text'])  # Смена имени
        if (m != None):
            new_name = (msg['text'][m.span()[1]:])
            if ('g' in globals()):
                g.__players__[g.get_id(chat_id)]['name'] = new_name

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