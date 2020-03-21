#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 15:45:10 2020

@author: zeynep
"""

SOURCE_FILE_NAME = 'source_list.txt'

"""
Hyperparameters:
    DECK_SIZE is the number of cards in each deck.
    RHO_STAR is the desired value of the RBSC coefficient.
    EPSILON is the tolerated amount of error on RHO_STAR.
    MAX_EPOCH is the maximum number of iterations in picking a card to add or 
    remove.
    RANDOM_MODIFICATION_THRESHOLD is the threshold value for deciding whether to
    make a random modification on a deck (i.e. add or remove a card, even if it
    does not help the algorithm to converge.)
"""
DECK_SIZE = 12
RHO_STAR = 0.90
EPSILON = 0.05
MAX_EPOCH = 100
RANDOM_MODIFICATION_THRESHOLD = 0.9