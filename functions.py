#! /usr/bin/env python
# -*- coding: utf-8 -*-


def isint(data):
    try:
        int(data)
        return True
    except ValueError:
        return False


def bot_init():
    token = '361539776:AAFSBN4saYHbChStFQF2pqkwST9IpVGHJ5g'  # bot id. Botname in telegram is realtimemafiabot
    TelegramBot = telepot.Bot(token)

    onstart_update = TelegramBot.getUpdates()
    update_id = int(onstart_update[-1].get('update_id')) + 1
    return TelegramBot, update_id


def set_roles(players_count, phonebook, names):
    import random
    players_list = list()
    for i in range(players_count):
        players_list.append(i)
    if players_count == 2:
        mafs_count = 1
        coms_count = 0
        docs_count = 1

    mafs = list(random.sample(players_list, mafs_count))
    coms = list(random.sample(set(players_list) - set(mafs), coms_count))
    docs = list(random.sample(set(players_list) - set(mafs) - set(coms), docs_count))
    goods = list(set(players_list) - set(mafs))

    players = {}
    for key, value in phonebook.items():
        players[key] = {'id': names[key], 'name': value, 'alive': 1, 'vote_kill': None, 'maf': None, 'com': None,
                        'doc': None, 'check_maf': None, 'cure': None}
        if key in mafs:
            players[key]['maf'] = 1
        if key in coms:
            players[key]['com'] = 1
        if key in docs:
            players[key]['doc'] = 1

    return players, mafs, coms, docs, goods


def send_starts(players, mafs, coms, docs, mafs_known):

    for maf in mafs:
        TelegramBot.sendMessage(players[maf]['id'], "You're the maf! Type the number of the player to vote for killing. For example: 3")
    for com in coms:
        TelegramBot.sendMessage(players[com]['id'], "You're com")
    for doc in docs:
        TelegramBot.sendMessage(players[doc]['id'], "You're doc")

    if mafs_known:
        mafs_acquaintance(players, mafs)  # znakomstvo mafov
    return


def mafs_acquaintance(players, mafs):
    for maf in mafs:
        TelegramBot.sendMessage(players[maf]['id'], 'mafs are %s' % mafs)


def incoming(update_id, players):
    users_voted = list()
    text_voted = list()
    updates = TelegramBot.getUpdates(offset=update_id)
    update_id += len(updates)
    for message in updates:
        users_voted.append(int(message.get('message').get('from').get('id')))
        text_voted.append(message.get('message').get('text'))

    print 'u_v = ', users_voted
    print 't_v = ', text_voted
    players, end_game, start_game = parse_incoming(users_voted, text_voted, players)
    print players
    return players, update_id, end_game, start_game


def parse_incoming(users_voted, text_voted, players):
    i = 0
    end_game = False
    start_game = False

    for user in users_voted:
        for key, values in players.items():
            if values['id'] == user:
                users_voted[i] = key
                if text_voted[i] == '/end':
                    end_game = True
                elif text_voted[i] == '/start':
                    start_game = True
                elif text_voted[i][0] == 'p' or text_voted[i][0] == 'P':
                    players[key]['check_maf'] = int(text_voted[i][1])
                elif text_voted[i][0] == 'l' or text_voted[i][0] == 'L':
                    players[key]['cure'] = int(text_voted[i][1])
                elif isint(text_voted[i]) and int(text_voted[i]) in players:
                    players[key]['vote_kill'] = int(text_voted[i])
        i += 1

    return players, end_game, start_game


def check_round_elapsed(mafs_able_kill, comissaire_access, start_time, roundtime):
    if int(time.time()) - start_time > roundtime:
        mafs_able_kill = True
        comissaire_access = True
        start_time = int(time.time())
    return mafs_able_kill, comissaire_access, start_time


def check_mafs_murder(players, mafs, docs, mafs_able_kill):

    if mafs_able_kill:

        votes_mafs = list()
        for maf in mafs:
            if players[maf]['alive'] != 0:
                votes_mafs.append(players[maf]['vote_kill'])  # get mafs' votes to one array

        if len(set(votes_mafs)) == 1 and set(votes_mafs) != set([None]):  # if set consists of one element -> all mafs voted for one person -> kill him
            mafs_able_kill = False
            killed = votes_mafs[0]  # variable for number of killed user
            cured = 0
            for doc in docs:
                if players[doc]['cure'] == killed:
                    cured = 1
            if cured == 0:
                players[killed]['alive'] = 0
                TelegramBot.sendMessage(players[killed]['id'], "you're dead!")
    return players, mafs_able_kill


def comissaire_check(players, coms, mafs, comissaire_access):
    if comissaire_access:
        for com in coms:
            if players[com]['alive'] != 0:
                if players[com]['check_maf'] in mafs:
                    TelegramBot.sendMessage(players[com]['id'], 'maf')
                    comissaire_access = False
                    players[com]['check_maf'] = None
                elif (players[com]['check_maf'] not in mafs) and (players[com]['check_maf'] is not None):
                    TelegramBot.sendMessage(players[com]['id'], 'not a maf')
                    comissaire_access = False
                    players[com]['check_maf'] = None
    return comissaire_access


def check_goods_murder(players, goods):
    votes_goods = list()
    for good in goods:
        if players[good]['alive'] != 0:
            votes_goods.append(players[good]['vote_kill'])
    if len(set(votes_goods)) == 1 and set(votes_goods) != set([None]):
        killed = votes_goods[0]
        players[killed]['alive'] = 0
        TelegramBot.sendMessage(players[killed]['id'], "you're dead!")
    return players


def check_alive(players, mafs, goods, end_game):
    alive_mafs = 0
    alive_goods = 0
    for maf in mafs:
        if players[maf]['alive'] != 0:
            alive_mafs += + 1
        if alive_mafs == 0:  # if no mafs alive send message
            for good in goods:
                TelegramBot.sendMessage(players[good]['id'], 'mafs are dead!')
                end_game = True
    for good in goods:
        if players[good]['alive'] != 0:
            alive_goods += + 1
        if alive_goods == 0:  # if no mafs alive send message
            for maf in mafs:
                TelegramBot.sendMessage(players[maf]['id'], 'goods are dead!')
                end_game = True
    return end_game


def game(phonebook, names):
    import telepot
    import time
    global telepot
    global TelegramBot
    global time
    players_count = 2

    TelegramBot, update_id = bot_init()

    roundtime = 0.1 * 60
    mafs_known = True

    while 1:

        players, mafs, coms, docs, goods = set_roles(players_count, phonebook, names)

        print 'start players=', players

        send_starts(players, mafs, coms, docs, mafs_known)

        comissaire_access = True
        end_game = False
        mafs_able_kill = True
        start_time = int(time.time())

        while not end_game:
            players, update_id, end_game, start_game = incoming(update_id, players)

            mafs_able_kill, comissaire_access, start_time = check_round_elapsed(mafs_able_kill, comissaire_access, start_time, roundtime)

            players, mafs_able_kill = check_mafs_murder(players, mafs, docs, mafs_able_kill)

            comissaire_access = comissaire_check(players, coms, mafs, comissaire_access)

            players = check_goods_murder(players, goods)

            end_game = check_alive(players, mafs, goods, end_game)

            time.sleep(5)
            print 'endgame=', end_game

        while not start_game :
            players, update_id, end_game, start_game = incoming(update_id, players)
            time.sleep(10)
