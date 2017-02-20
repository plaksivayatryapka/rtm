#! /usr/bin/env python
# -*- coding: utf-8 -*-

''' in real world everybody holds the smartfone with telegram app,
everybody started his own chat with bot and chat_ids are recorded manually to player[i][0] fields.
Nearby the user lays the paper with his number in the app, bot and script (for example "1").

Start of the game means this python script started. Users receive messages with their roles,
discuss something and type in botchat user numbers they want to act (kill, cure, etc)
Killing action (from mafs or goods) executes if everybody chooses same user and doctor didn't cured.
Users can change their vote at any time'''

import telepot
import random

token = ' ' # bot id. Botname in telegram is realtimemafiabot
TelegramBot = telepot.Bot(token)

# "player" list stores all info during the game. Every game must start with this settings. Format:

player[0][0] = 217967871 # chat id of player with number 0. needed for messaging
player[0][1] = 1 # is alive. 0 = dead, 2 = can't talk
player[0][2] = [] # vote for killing/curing/etc.
player[1][0] = 123456798 # second user
# etc

# start conditions

mafs_count = 3
comms_count = 1
docs_count = 1
cits_count = 3

# randomly generate roles using start conditions. Final result, for example:

mafs = [0, 2, 4] # this means that users with 0 2 4 numbers in real world are mafs.
goods = [1, 3, 5, 6, 7]
comms = [1]
docs = [3]
cits = [5, 6, 7]

votes_mafs = [] # list for mafs' votes for killing

# tell everybody the role

for maf in mafs :
    TelegramBot.sendMessage(player[maf][0], "You're the maf!") # send message for mafs, where player[i][0] is chat id of user
for comm in comms : # cycle needed because there may be more than one doc
    TelegramBot.sendMessage(player[comm][0], "You're the comissaire!") # send message for mafs
for doc in docs :
    TelegramBot.sendMessage(player[doc][0], "You're the doctor!") # send message for mafs
for cit in cits :
    TelegramBot.sendMessage(player[cit][0], "You're the citizen!") # send message for mafs

# check for incomming messages from users and put data to "player" list. Users send only vote data and it is stored in player[x][2]
# some code

# parse incoming data

    # check for mafs votes, kill, cure

for i in mafs :
    if player[maf][1] != 0 : # if alive
        votes_mafs.append(player[i][2]) # get mafs' votes to one array

if set(votes_mafs) == 1 : # if set consists of one element -> all mafs voted for one person -> kill him
    killed = votes_mafs[0] # variable for number of killed user
    player[killed][1] = 0
    
    for doc in docs : 
        if player[doc][2] == votes_mafs[0] : # if any doctor voted for killed user make him alive
            player[killed][1] = 1
    
    if player[killed][1] == 0 :
        TelegramBot.sendMessage(player[killed][0], "You're dead =(") # send message for dead user

    # check for good votes and kill

# same thing for goods

# check if any maf is alive

alive_mafs = 0
for maf in mafs :
    if player[maf][1] == 1 :
        alive_mafs = alive_mafs + 1
    if alive_mafs == 0 : # if no mafs alive send message
        for good in goods :
            TelegramBot.sendMessage(player[good][0], 'mafs are dead!')
        
