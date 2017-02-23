#! /usr/bin/env python
# -*- coding: utf-8 -*-

def send_starts(players) :
    mafs = []
    coms = []
    goods = []
    for key, values in players.items() :
        print values
        if values['maf'] == 1 :
            mafs.append(key)
            TelegramBot.sendMessage(values['id'], "You're the maf! Type the number of the player to vote for killing. For example: 3") # send message for mafs, where player[i][0] is chat id of user
        elif values['com'] == 1 :
            coms.append(key)
            goods.append(key)
            TelegramBot.sendMessage(values['id'], "You're com")
        elif values['doc'] == 1 :
            goods.append(key)
            TelegramBot.sendMessage(values['id'], "You're doc")
        else:
            goods.append(key)
    mafs_acquaintance(players, mafs) # znakomstvo mafov
    return mafs, coms, goods
            
def mafs_acquaintance (players, mafs) :
    
    for maf in mafs :
        TelegramBot.sendMessage(players[maf]['id'], 'mafs are %s' %mafs)

def incoming(update_id, players) :
    users_voted = list()
    text_voted = list()
    updates = TelegramBot.getUpdates(offset = update_id)
    update_id = update_id + len(updates)
    for message in updates :
        users_voted.append(int(message.get('message').get('from').get('id')))
        text_voted.append(message.get('message').get('text'))
    print 'u_v = ', users_voted
    print 't_v = ', text_voted
    players, end_game, start_game = parse_incoming(users_voted, text_voted, players)
    print players
    return players, update_id, end_game, start_game

def parse_incoming(users_voted, text_voted, players) :
    i = 0
    end_game = False
    start_game = False
    for user in users_voted :
        for key, values in players.items() :
            if values['id'] == user :
                users_voted[i] = key
                if text_voted[i] == '/end':
                        end_game = True
                elif text_voted[i] == '/start':
                        start_game = True
                elif text_voted[i][0] == 'p' or text_voted[i][0] == 'P':
                    players[key]['check_maf'] = int(text_voted[i][1])                                
                else :
                    players[key]['vote_kill'] = int(text_voted[i])
                
        i = i + 1

    return players, end_game, start_game

def check_mafs_murder (players, mafs, comissaire_access) :
    votes_mafs = list()
    #print 'cmm=', players
    for maf in mafs :
        if players[maf]['alive'] != 0 :
            votes_mafs.append(players[maf]['vote_kill']) # get mafs' votes to one array
            
    if len(set(votes_mafs)) == 1 and set(votes_mafs) != set([None]): # if set consists of one element -> all mafs voted for one person -> kill him
        killed = votes_mafs[0] # variable for number of killed user
        #print 'killed=', killed
        players[killed]['alive'] = 0
        comissaire_access = True
        TelegramBot.sendMessage(players[killed]['id'], "you're dead!")
    return players, comissaire_access
        
def comissaire_check (players, coms, mafs, comissaire_access) :
    if comissaire_access == True :
        for com in coms :
            if players[com]['alive'] != 0 :
                if players[com]['check_maf'] in mafs :
                    TelegramBot.sendMessage(players[com]['id'], 'maf')
                    comissaire_access = False
                    players[com]['check_maf'] = None
                elif (players[com]['check_maf'] not in mafs) and (players[com]['check_maf'] != None) :
                    TelegramBot.sendMessage(players[com]['id'], 'not a maf')
                    comissaire_access = False
                    players[com]['check_maf'] = None
    return comissaire_access
            
def check_goods_murder (players, goods) :
    votes_goods = list()
    for good in goods :
        if players[good]['alive'] != 0 :
            votes_goods.append(players[good]['vote_kill'])
    if len(set(votes_goods)) == 1 and set(votes_goods) != set([None]):
        killed = votes_goods[0]
        players[killed]['alive'] = 0
        TelegramBot.sendMessage(players[killed]['id'], "you're dead!")
    return players

def check_alive (players, mafs, goods, end_game) :
    alive_mafs = 0
    alive_goods = 0
    for maf in mafs :
        if players[maf]['alive'] != 0 :
            alive_mafs = alive_mafs + 1
        if alive_mafs == 0 : # if no mafs alive send message
            for good in goods :
                TelegramBot.sendMessage(players[good]['id'], 'mafs are dead!')
                end_game = True
    for good in goods :
        if players[good]['alive'] != 0 :
            alive_goods = alive_goods + 1
        if alive_goods == 0 : # if no mafs alive send message
            for maf in mafs :
                TelegramBot.sendMessage(players[maf]['id'], 'goods are dead!')
                end_game = True
    return end_game
                
def game():
    
    import telepot
    import time
    import random
    global telepot
    global TelegramBot
    
    token = '361539776:AAFSBN4saYHbChStFQF2pqkwST9IpVGHJ5g' # bot id. Botname in telegram is realtimemafiabot
    TelegramBot = telepot.Bot(token)
    players_count = 2
    
    onstart_update = TelegramBot.getUpdates()
    update_id = int(onstart_update[-1].get('update_id')) + 1
    
    phonebook = {0 : 'slavik', 1 : 'polya'}
    names = [217967871, 265133215]
    
    while 1: 
        
        players_list = list()
        for i in range(players_count) :
            players_list.append(i)
        if players_count == 2 :
            mafs_count = 1
            coms_count = 1
            docs_count = 0
        mafs = random.sample(players_list, mafs_count)
        coms = random.sample(set(players_list).difference(mafs), coms_count)
        #print 'mafs=', mafs, 'coms=', coms
        
        players = {}
        for key, value in phonebook.items() :
            players[key] = {'id' : names[key], 'name' : value, 'alive' : 1, 'vote_kill': None , 'maf' : None, 'com' : None, 'doc' : None, 'check_maf': None, 'cure': None}
            if key in mafs :
                players[key]['maf'] = 1
            if key in coms :
                players[key]['com'] = 1
            #if key in docs :
            #   players[key]['doc'] = 1
                
        print 'start players=', players
        mafs, coms, goods = send_starts(players)
    
        comissaire_access = True
        end_game = False
        while end_game == False:

            players, update_id, end_game, start_game         = incoming(update_id, players)

            players, comissaire_access = check_mafs_murder (players, mafs, comissaire_access)

            comissaire_access          = comissaire_check (players, coms, mafs, comissaire_access)
        
            players                    = check_goods_murder (players, goods)

            end_game = check_alive (players, mafs, goods, end_game)

            time.sleep(6)
            print 'endgame=', end_game
    
        while start_game == False:
            players, update_id, end_game, start_game = incoming(update_id, players)
            time.sleep(10)
    
