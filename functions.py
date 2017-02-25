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


def set_roles(players_count, phonebook, names, drink_period):
    import random
    players_list = list()
    for i in range(players_count):
        players_list.append(i)
    if players_count == 2:
        mafs_count = 1
        coms_count = 0
        docs_count = 1
        drinker_count = 0

    mafs = list(random.sample(players_list, mafs_count))
    coms = list(random.sample(set(players_list) - set(mafs), coms_count))
    docs = list(random.sample(set(players_list) - set(mafs) - set(coms), docs_count))
    drinkers = list(random.sample(set(players_list) - set(mafs) - set(coms) - set(docs), drinker_count))
    goods = list(set(players_list) - set(mafs))

    players = {}
    for key, value in phonebook.items():
        players[key] = {'id': names[key], 'name': value, 'alive': 1, 'vote_kill': None, 'maf': None, 'com': None,
                        'doc': None, 'drinker': None, 'check_maf': None, 'cure': None, 'drink_with': None, 'maf_killing': None}
        if key in mafs:
            players[key]['maf'] = 1
        if key in coms:
            players[key]['com'] = 1
        if key in docs:
            players[key]['doc'] = 1
        if key in drinkers:
            players[key]['drinker'] = 1
        TelegramBot.sendMessage(players[key]['id'], "Game started")

    drunk = {'number': None, 'period': drink_period, 'started_time': int(time.time()), 'allowed': True}

    return players, mafs, coms, docs, drinkers, drunk, goods


def send_starts(players, mafs, mafs_known):
    for key, value in players.items():
        if value['maf'] == 1:
            TelegramBot.sendMessage(value['id'], "You're the maf! Type the number of the player to vote for killing. For example: 3")
        elif value['com'] == 1:
            TelegramBot.sendMessage(value['id'], "You're com. Type the number of the player you want to check with letter p or P before it. For example: p3\nFor day voting type only number. Example: 3 ")
        elif value['doc'] == 1:
            TelegramBot.sendMessage(value['id'], "You're doc. Type the number of the player you want to cure with letter l or L before it. For example: L3\nFor day voting type only number. Example: 3 ")
        elif value['drinker'] ==1:
            TelegramBot.sendMessage(value['id'], "You're drinker. Type the number of the player you want to stop speaking with letter d or D before it. For example: D3\nFor day voting type only number. Example: 3 ")
        else:
            TelegramBot.sendMessage(value['id'], "You're citizen. For day voting type only number. Example: 3")
    if mafs_known:
            mafs_acquaintance(players, mafs)  # znakomstvo mafov
    return


def mafs_acquaintance(players, mafs):
    for maf in mafs:
        TelegramBot.sendMessage(players[maf]['id'], 'mafs are numbers %s' % mafs)


def check_something_elapsed(players, mafs_able_kill, comissaire_access, start_time, roundtime, drunk):
    if int(time.time()) - start_time > roundtime:
        mafs_able_kill = True
        comissaire_access = True
        start_time = int(time.time())

    if (int(time.time()) - drunk['started_time'] > drunk['period']) and drunk['number'] is not None:
        drunk['allowed'] = True
        TelegramBot.sendMessage(players[drunk['number']]['id'], "You can talk")
        drunk['number'] = None
    return mafs_able_kill, comissaire_access, start_time, drunk


def incoming(players, update_id):
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
    for key, values in players.items():
        print key, values
    return players, update_id, end_game, start_game


def parse_incoming(users_voted, text_voted, players):
    i = 0
    end_game = False
    start_game = False

    for user in users_voted:
        for key, values in players.items():
            if values['id'] == user:  # if user and id matches
                users_voted[i] = key
                if text_voted[i] == '/end':
                    end_game = True
                elif text_voted[i] == '/start':
                    start_game = True
                elif (text_voted[i][0] == 'm' or text_voted[i][0] == 'M') and players[key]['maf'] == 1:
                    if isint(text_voted[i][1]) is True:
                        players[key]['maf_killing'] = int(text_voted[i][1])

                elif (text_voted[i][0] == 'p' or text_voted[i][0] == 'P') and players[key]['com'] == 1:
                    if isint(text_voted[i][1]):
                        players[key]['check_maf'] = int(text_voted[i][1])

                elif (text_voted[i][0] == 'l' or text_voted[i][0] == 'L') and players[key]['doc'] == 1:
                    if isint(text_voted[i][1]):
                        players[key]['cure'] = int(text_voted[i][1])

                elif (text_voted[i][0] == 'd' or text_voted[i][0] == 'D') and players[key]['drinker'] == 1:
                    if isint(text_voted[i][1]):
                        players[key]['drink_with'] = int(text_voted[i][1])

                elif isint(text_voted[i]) and int(text_voted[i]) in players:
                    players[key]['vote_kill'] = int(text_voted[i])
        i += 1

    return players, end_game, start_game


def check_mafs_murder(players, mafs, docs, mafs_able_kill, doctor_cured_info):

    if mafs_able_kill:

        votes_mafs = list()
        for maf in mafs:
            if players[maf]['alive'] != 0:
                votes_mafs.append(players[maf]['maf_killing'])  # get mafs' votes to one array

        if len(set(votes_mafs)) == 1 and set(votes_mafs) != set([None]):  # if set consists of one element -> all mafs voted for one person -> kill him
            mafs_able_kill = False
            killed = votes_mafs[0]  # variable for number of killed user
            cured = 0
            for doc in docs:
                if players[doc]['cure'] == killed:
                    cured = 1
                    if doctor_cured_info is True:
                        for maf in mafs:
                            if players[maf]['alive'] != 0:
                                TelegramBot.sendMessage(players[maf]['id'], "doc cured")
            if cured == 0:
                players[killed]['alive'] = 0
                TelegramBot.sendMessage(players[killed]['id'], "you're dead!")

    return players, mafs_able_kill


def comissaire_check(players, coms, mafs, comissaire_access):
    if comissaire_access:
        for com in coms:
            if players[com]['alive'] != 0 and players[com]['check_maf'] is not None and players[players[com]['check_maf']]['alive']:
                if players[com]['check_maf'] in mafs:
                    TelegramBot.sendMessage(players[com]['id'], 'maf')
                    comissaire_access = False
                    players[com]['check_maf'] = None
                elif (players[com]['check_maf'] not in mafs) and (players[com]['check_maf'] is not None):
                    TelegramBot.sendMessage(players[com]['id'], 'not a maf')
                    comissaire_access = False
                    players[com]['check_maf'] = None
    return comissaire_access


def check_goods_murder(players, all_able_kill, docs, Counter, doctor_cured_info):
    votes = list()
    if all_able_kill is True:
        for key, value in players.items():
            alives = 0
            if value['alive'] == 1:
                alives += 1
                if value['vote_kill'] is not None:
                    votes.append(players[key]['vote_kill'])
        votes_sorting = Counter(votes)
        votes_sorted = votes_sorting.most_common()
        if len(votes_sorted) > 0:
            if (alives / 2 <= votes_sorted[0][1] and alives != 3) or (alives == 3 and votes_sorted[0][1] == 2):
                killed = votes_sorted[0][0]
                all_able_kill = False
                cured = 0
                for doc in docs:
                    if players[doc]['cure'] == killed:
                        cured = 1
                        if doctor_cured_info is True:
                            for key, value in players.items():
                                if players[key]['alive'] != 0:
                                    TelegramBot.sendMessage(players[key]['id'], "doc cured")
                if cured == 0:
                    players[killed]['alive'] = 0
                    TelegramBot.sendMessage(players[killed]['id'], "you're dead!")

    return players, all_able_kill


def drinking(drinkers, players, drunk):
    for drinker in drinkers:
        if players[drinker]['drink_with'] is not None and drunk['allowed'] is True:
            drunk['number'] = players[drinker]['drink_with']
            TelegramBot.sendMessage(players[drunk['number']]['id'], "you're drunk and can't talk for a while. we will notify you")
            players[drinker]['drink_with'] = None
            drunk['drinking_allowed'] = False
            drunk['started_time'] = int(time.time())
    return players, drunk


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
    from collections import Counter
    global telepot
    global TelegramBot
    global time

    players_count = 2

    TelegramBot, update_id = bot_init()

    roundtime = 0.1 * 60
    mafs_known = True
    drink_period = 0.1 * 60
    doctor_cured_info = True

    while 1:
        mafs = list()
        coms = list()
        docs = list()
        drinkers = list()
        goods = list()

        players, mafs, coms, docs, drinkers, drunk, goods = set_roles(players_count, phonebook, names, drink_period)
        send_starts(players, mafs, mafs_known)
        comissaire_access = True
        end_game = False
        mafs_able_kill = True
        all_able_kill = True
        start_time = int(time.time())

        while not end_game:
            players, update_id, end_game, start_game             = incoming(players, update_id)
            mafs_able_kill, comissaire_access, start_time, drunk = check_something_elapsed(players, mafs_able_kill, comissaire_access, start_time, roundtime, drunk)
            players, drunk                                       = drinking(drinkers, players, drunk)
            players, mafs_able_kill                              = check_mafs_murder(players, mafs, docs, mafs_able_kill, doctor_cured_info)
            comissaire_access                                    = comissaire_check(players, coms, mafs, comissaire_access)
            players, all_able_kill                               = check_goods_murder(players, all_able_kill, docs, Counter, doctor_cured_info)
            end_game                                             = check_alive(players, mafs, goods, end_game)
            time.sleep(3)

        while not start_game:
            time.sleep(3)
            players, update_id, end_game, start_game = incoming(players, update_id)

#drinkers, vote_goods
#error input passing
