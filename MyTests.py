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
        self.__started__ = 0
        self.__current_round__ = 0
        self.__game_id__ = 0
        self.__players__ = {}
        self.__player_num__ = 0
        self.__host__ = ''
        self.__roles__ = {
            'maf_num':0,
            'cit_num':0,
            'doc_num':0,
            'com_num':0,
        }
        self.__round_time__ = 5
    def add_player(self, adr):
        self.__players__[self.__player_num__ + 1] = {
                                        'adr': adr,
                                        'name': 'Player_' + str(self.__player_num__+1),
                                        'alive': 1,
                                        'pointer': 0,
                                        'acted': 0,
                                        'role': None
                                      }
        self.__player_num__ += 1

    # выбор адресов соответствующих подгрупп
    def everybody(self):
        return [self.__players__[i]['adr'] for i in self.__players__]

    def alive(self):
        arr = []
        for i in self.__players__:
            if self.__players__[i]['alive']:
                arr.append(self.__players__[i]['adr'])
        return arr

    def mafs(self):
        arr = []
        for i in self.__players__:
            if (self.__players__[i]['role'] == 'maf'):
                arr.append(self.__players__[i]['adr'])
        return arr

    def cits(self):
        arr = []
        for i in self.__players__:
            if (self.__players__[i]['role'] == 'cit'):
                arr.append(self.__players__[i]['adr'])
        return arr

    def coms(self):
        arr = []
        for i in self.__players__:
            if (self.__players__[i]['role'] == 'com'):
                arr.append(self.__players__[i]['adr'])
        return arr

    def docs(self):
        arr = []
        for i in self.__players__:
            if (self.__players__[i]['role'] == 'doc'):
                arr.append(self.__players__[i]['adr'])
        return arr

    def say(self, players, message):
        for id in players:
            bot.sendMessage(id, message)

    def report_status(self, players):
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

    def reload_abilities(self):
        for i in self.__players__:
            self.__players__[i]['acted'] = 0

    # функция обновления игры
    def refresh(self, ):
        None

def msg_handler(adr, msg):
    if (msg == '/start_game'):  # Хостится игра
        host = adr
        game_id = random.randrange(0,100)
        print('game ' + str(game_id) + ' starting...')
        global g
        g = game()
        g.__game_id__ = game_id
        g.__host__ = host
        g.add_player(host)
        games_list.append((game_id))
        bot.sendMessage(adr, 'game ' + str(game_id) + ' starting')

    if (msg == '/go'):  # Комплектуется и запускается игра
        if ('g' in globals()):
            if adr == g.__host__:
                # Укомплектовка состава
                if (len(g.__players__) >= g.__roles__['maf_num'] + g.__roles__['doc_num'] + g.__roles__['com_num']):
                    everybody = [i+1 for i in range(len(g.__players__))]
                    mafs = random.sample(everybody, g.__roles__['maf_num'])
                    rest = [i for i in everybody if i not in mafs]
                    docs = random.sample(rest, g.__roles__['doc_num'])
                    rest = [i for i in rest if i not in docs]
                    coms = random.sample(rest, g.__roles__['com_num'])
                    cits = [i for i in rest if i not in coms]
                    g.__roles__['cit_num'] = len(cits)
                    # присвоение ролей
                    for i in mafs:
                        g.__players__[i]['role'] = 'maf'
                    for i in docs:
                        g.__players__[i]['role'] = 'doc'
                    for i in coms:
                        g.__players__[i]['role'] = 'com'
                    for i in cits:
                        g.__players__[i]['role'] = 'cit'
                    # Объявление ролей
                    g.say(g.mafs(), 'YOU ARE MAFIA')
                    g.say(g.cits(), 'YOU ARE CITIZEN')
                    g.say(g.coms(), 'YOU ARE COMMISAIRE')
                    g.say(g.docs(), 'YOU ARE DOCTOR')
                    # Знакомство мафии
                    maf_list_msg = ''
                    for player_id in g.__players__:
                        if g.__players__[player_id]['role'] == 'maf':
                            maf_list_msg += str(player_id) + ' - ' + g.__players__[player_id]['name'] + ' \n'
                    g.say(g.mafs(), 'YOUR COLLEAGUES:')
                    g.say(g.mafs(), maf_list_msg)
                    # Начало игры
                    g.__started__ = 1
                    g.__current_round__ = 1
                    g.say(g.everybody(), 'GAME IS STARTED')
                    g.say(g.everybody(), 'ROUND 1')

    if (msg == '/game_list'):  # Проверка списка игр
        bot.sendMessage(adr, str(games_list))

    if (msg == '/players_adr'):  # Проверка айдишников игроков
        if ('g' in globals()):
            bot.sendMessage(adr, g.everybody())

    if (msg == '/player_names'):  # Проверка списка игроков
        if ('g' in globals()):
            g.report_status([adr])

    if (msg == '/countdown'):  # Всем 3-х секундное ожидание
        if ('g' in globals()):
            g.countdown(3, 1, g.everybody())

    m = re.search('/mafs ', msg) # Число мафов
    if (m != None):
        maf_num = int(msg[m.span()[1]: ])
        g.__roles__['maf_num'] = maf_num

    m = re.search('/docs ', msg) # Число докторов
    if (m != None):
        doc_num = int(msg[m.span()[1]: ])
        g.__roles__['doc_num'] = doc_num

    m = re.search('/coms ', msg) # Число коммисаров
    if (m != None):
        com_num = int(msg[m.span()[1]: ])
        g.__roles__['com_num'] = com_num


    m = re.search('/change_name ', msg)  # Смена имени
    if (m != None):
        new_name = (msg[m.span()[1]:])
        if ('g' in globals()):
            g.__players__[g.get_id(adr)]['name'] = new_name

    m = re.search('/connect ', msg) # Коннект к игре
    if (m != None):
        connect_to = int(msg[m.span()[1]: ])
        if (connect_to in games_list):
            if (g.__players__ == {}):
                bot.sendMessage(adr, 'connected')
                g.add_player(adr) # добавляем игрока
            elif (adr not in list(g.__players__.keys())):
                bot.sendMessage(adr, 'connected')
                g.add_player(adr) # добавляем игрока
            else:
                bot.sendMessage(adr, 'you are already connected')

def time_handler(time_stamp):
    if ('g' in globals()):
        if g.__started__:
            time_stamp += 1
        if (time_stamp == int(g.__round_time__ * 30)): # половина времени прошло
            mins = int(time_stamp/60)
            secs = time_stamp - mins*60
            g.say(g.everybody(), str(mins) + ' Min ' + str(secs) + ' Sec left...')
        if (int(g.__round_time__ * 60) - time_stamp == 60): # осталась минута
            g.say(g.everybody(), 'One minute left...')
        if (time_stamp == g.__round_time__ * 60): # время раунда вышло
            g.reload_abilities()
            time_stamp = 0
            g.countdown(3, 1, g.everybody())
            g.__current_round__ += 1
            g.say(g.everybody(),'ROUND ' + str(g.__current_round__))
            g.report_status(g.everybody())
    return time_stamp


token = '371150676:AAFNeZ7lPfeuftBxUaXuc_Drrj6jgzvW4rA'
bot = telepot.Bot(token)
# Очистка кэша
onstart_update = bot.getUpdates()
if (onstart_update != []):
    update_id = int(onstart_update[-1].get('update_id')) + 1
    bot.getUpdates(offset=update_id)

# Основной луп
#bot.message_loop(main)
#print('waiting for game ...')
offset = 0
time_stamp = 0

# Basic loop
while 1:
    time_stamp = time_handler(time_stamp)
    print(time_stamp)
    pkgs = bot.getUpdates(offset = offset)
    if pkgs != []: # сообщение/я пришло... обрабатываем
        msg_num = len(pkgs) # число пришедших пакетов
        for pkg in pkgs:    # обрабатываем последовательно
            adr = pkg['message']['from']['id']
            msg = pkg['message']['text']
            msg_handler(adr, msg)
        offset = int(pkgs[-1].get('update_id')) + 1

    # проверка на окончание кона
    # в случае если все все сделали свои дела
    cont = 0
    if('g' in globals()):
        if g.__started__:
            for i in g.__players__:
                if (g.__players__[i]['acted'] == 0):
                    cont = 1
            if ~cont:
                time_stamp = g.__round_time__*60-1



    time.sleep(1)