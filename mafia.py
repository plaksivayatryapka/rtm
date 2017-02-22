#! /usr/bin/env python
# -*- coding: utf-8 -*-

import random
from functions import game

# start conditions

#mafs_count = 3
#coms_count = 1
#docs_count = 1
#cits_count = 3

players = {'0': {'id': 217967871, 'name': 'slavik', 'alive': 1, 'vote_kill': None, 'maf': None, 'check_maf': None, 'cure': None},\
           '1': {'id': 265133215, 'name': 'polya', 'alive': 1, 'vote_kill': None, 'maf': 1}}

game(players)
