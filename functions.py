#! /usr/bin/env python
# -*- coding: utf-8 -*-

def send_starts(players) :

    for key, values in players.items() :
        if values['maf'] == 1 :
            TelegramBot.sendMessage(values['id'], "You're the maf! Type the number of the player to vote for killing. For example: 3") # send message for mafs, where player[i][0] is chat id of user
        if values['com'] == 1 :
            TelegramBot.sendMessage(values['id'], "You're com")
        if values['doc'] == 1 :
            TelegramBot.sendMessage(values['id'], "You're doc")
        for key, values in players.items() :
            mafs = []
            coms = []
            goods = []
            if values['maf'] == 1 :
                mafs.append(key)
            elif values['com'] == 1 :
                coms.append(key)
            else:
                goods.append(key)
        mafs_acquaintance (mafs, coms, goods) # znakomstvo mafov
            
def mafs_acquaintance (players, mafs) :
    
    for maf in mafs :
        TelegramBot.sendMessage(players[maf], mafs)

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
    players = parse_incoming(users_voted, text_voted, players)
    print players
    return players, update_id

def parse_incoming(users_voted, text_voted, players) :
    i = 0
    for user in users_voted :
        for key, values in players.items() :
            if values['id'] == user :
                users_voted[i] = key
                if text_voted[i][0] == 'p' or text_voted[i][0] == 'P':
                    players[key]['check_maf'] = int(text_voted[i][1])                                
                else :
                    players[key]['vote_kill'] = int(text_voted[i][1])
        i = i + 1

    return players

def check_mafs_murder (players, mafs, comissaire_access) : 
    for maf in mafs :
        if players[maf]['alive'] != 0 :
            votes_mafs.append(players[maf]['vote_kill']) # get mafs' votes to one array
            
    if len(set(votes_mafs)) == 1 and set(votes_mafs) != set([None]): # if set consists of one element -> all mafs voted for one person -> kill him
        killed = votes_mafs[0] # variable for number of killed user
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

def check_alive (players, mafs, goods) :
    alive_mafs = 0
    alive_goods = 0
    for maf in mafs :
        if players[maf]['alive'] != 0 :
            alive_mafs = alive_mafs + 1
        if alive_mafs == 0 : # if no mafs alive send message
            for good in goods :
                TelegramBot.sendMessage(players[good]['id'], 'mafs are dead!')
                exit()
    for good in goods :
        if players[good]['alive'] != 0 :
            alive_goods = alive_goods + 1
        if alive_goods == 0 : # if no mafs alive send message
            for maf in mafs :
                TelegramBot.sendMessage(players[maf]['id'], 'goods are dead!')
                exit()

def game(players):
    
    import telepot
    import time
    global telepot
    global TelegramBot
    
    token = '361539776:AAFSBN4saYHbChStFQF2pqkwST9IpVGHJ5g' # bot id. Botname in telegram is realtimemafiabot
    TelegramBot = telepot.Bot(token)

    onstart_update = TelegramBot.getUpdates()
    update_id = int(onstart_update[-1].get('update_id')) + 1

    mafs, coms, goods = send_starts(players)
    
    comissaire_access = True

    while 1:

        players, update_id         = incoming(update_id, players)

        players, comissaire_access = check_mafs_murder (players, mafs, comissaire_access)

        comissaire_access          = comissaire_check (players, coms, mafs, comissaire_access)
        
        players                    = check_goods_murder (players, goods)

        check_alive (players, mafs, goods)
    
        time.sleep(6)
