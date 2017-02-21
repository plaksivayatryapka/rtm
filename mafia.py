#! /usr/bin/env python
# -*- coding: utf-8 -*-

''' in real world everybody holds the smartfone with telegram app,
everybody started his own chat with bot and chat_ids are recorded manually to player[i][0] fields.
Near the user lays the paper with his number written on it (for example "1").

Start of the game means this python script started. Users receive messages with their roles,
discuss something and type in botchat user numbers they want to act (kill, cure, etc)
Killing action (from mafs or goods) executes if everybody chooses same user and doctor didn't cured.
Users can change their vote at any time '''

import random
from functions import game

# "player" list stores all info during the game. Every game must start with this settings. Format:

phonebook = dict(slavik = 217967871, polya = 265133215)
places = dict(slavik = 0, polya = 1)

players = [[None for x in range(9)] for y in range(4)]  # generate table
players[0][0] = phonebook.get('slavik') # chat id of player with number 0. needed for messaging
players[0][1] = 1 # is alive. 0 = dead, 2 = can't talk
players[0][2] = None # vote for killing
players[1][0] = phonebook.get('polya') # second user
players[1][1] = 1
players[1][2] = None # vote for killing
players[1][3] = None # vote for check/cure etc

#players[0][0] =  third player
#players[3][1] = 1 # is alive. 0 = dead, 2 = can't talk
#players[3][2] = []
# etc

# start conditions

#mafs_count = 3
#coms_count = 1
#docs_count = 1
#cits_count = 3

# randomly generate roles using start conditions. Final result, for example:

#mafs = [0, 2, 4] # this means that users with 0 2 4 numbers in real world are mafs.
mafs = [0]
goods = [1] # good citizens player id
coms = [1] # comissaire player id

game(phonebook, places, players, mafs, goods, coms)
