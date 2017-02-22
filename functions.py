#! /usr/bin/env python
# -*- coding: utf-8 -*-

def send_starts(players, mafs, coms) :

    for maf in mafs :
        TelegramBot.sendMessage(players[maf][0], "You're the maf!") # send message for mafs, where player[i][0] is chat id of user
    for com in coms : # cycle needed because there may be more than one comm
        TelegramBot.sendMessage(players[com][0], "You're the comissaire!") # send message for mafs

def parse_incoming(users_voted, text_voted, phonebook, places, players) :
    for i in range(len(users_voted)) :
        if users_voted[i] == phonebook.get('slavik') :
            users_voted[i] = places.get('slavik')
        elif users_voted[i] == phonebook.get('polya') :
            users_voted[i] = places.get('polya')
    i = 0
    for user in users_voted :
        if text_voted[i][0] == 'p' or text_voted[i][0] == 'P':
            players[user][3] = int(text_voted[i][1])
        else :
            players[user][2] = int(text_voted[i])
        i = i + 1
    return players

def incoming(update_id, players, phonebook, places) :
    users_voted = list()
    text_voted = list()
    updates = TelegramBot.getUpdates(offset = update_id)
    update_id = update_id + len(updates)
    for message in updates :
        users_voted.append(int(message.get('message').get('from').get('id')))
        text_voted.append(message.get('message').get('text'))
    print ('u_v = ', users_voted)
    print ('t_v = ', text_voted)
    players = parse_incoming(users_voted, text_voted, phonebook, places, players)
    print (players)
    return players, update_id

def check_mafs_murder (players, mafs, comissaire_access) :
    votes_mafs = list()
    for maf in mafs :
        if players[maf][1] != 0 : # if alive
            votes_mafs.append(players[maf][2]) # get mafs' votes to one array
            
    if len(set(votes_mafs)) == 1 and set(votes_mafs) != set([None]): # if set consists of one element -> all mafs voted for one person -> kill him
        killed = votes_mafs[0] # variable for number of killed user
        players[killed][1] = 0
        comissaire_access = True
        TelegramBot.sendMessage(players[killed][0], "you're dead!")
    return players, comissaire_access
        
def comissaire_check (players, coms, mafs, comissaire_access) :
    if comissaire_access == True :
        for com in coms :
            if players[com][1] != 0 :
                if players[com][3] in mafs :
                    TelegramBot.sendMessage(players[com][0], 'maf')
                    comissaire_access = False
                    players[com][3] = None
                elif (players[com][3] not in mafs) and (players[com][3] != None) :
                    TelegramBot.sendMessage(players[com][0], 'not a maf')
                    comissaire_access = False
                    players[com][3] = None
    return comissaire_access
            
def check_goods_murder (players, goods) :
    votes_goods = list()
    for good in goods :
        if players[good][1] != 0 :
            votes_goods.append(players[good][2])
    if len(set(votes_goods)) == 1 and set(votes_goods) != set([None]):
        killed = votes_goods[0]
        players[killed][1] = 0
        TelegramBot.sendMessage(players[killed][0], "you're dead!")
    return players

def check_alive (players, mafs, goods) :
    alive_mafs = 0
    alive_goods = 0
    for maf in mafs :
        if players[maf][1] == 1 :
            alive_mafs = alive_mafs + 1
        if alive_mafs == 0 : # if no mafs alive send message
            for good in goods :
                TelegramBot.sendMessage(players[good][0], 'mafs are dead!')
                exit()
    for good in goods :
        if players[good][1] == 1 :
            alive_goods = alive_goods + 1
        if alive_goods == 0 : # if no mafs alive send message
            for maf in mafs :
                TelegramBot.sendMessage(players[maf][0], 'goods are dead!')
                exit()

def game(phonebook, places, players, mafs, goods, coms):
    
    import telepot
    import time
    global telepot
    global TelegramBot
    token = '361539776:AAFSBN4saYHbChStFQF2pqkwST9IpVGHJ5g' # bot id. Botname in telegram is realtimemafiabot
    TelegramBot = telepot.Bot(token)

    onstart_update = TelegramBot.getUpdates()
    update_id = int(onstart_update[-1].get('update_id')) + 1
    help_for_bot_programmer = onstart_update[-1].get('message').get('from').get('id')
    TelegramBot.sendMessage(help_for_bot_programmer, 'your id (last message in botchat) is %s' % help_for_bot_programmer)
    print ('last update id = ', update_id)

    send_starts(players, mafs, coms)
    
    comissaire_access = True

    while 1:

        players, update_id         = incoming(update_id, players, phonebook, places)

        players, comissaire_access = check_mafs_murder (players, mafs, comissaire_access)

        comissaire_access          = comissaire_check (players, coms, mafs, comissaire_access)
        
        players                    = check_goods_murder (players, goods)

        check_alive (players, mafs, goods)
    
        time.sleep(6)