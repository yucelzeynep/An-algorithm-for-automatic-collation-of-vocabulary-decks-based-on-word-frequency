#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 12:26:30 2019

@author: zeynep

This program builds 2 decks of flash-cards with a desired difficulty relation.

For this example, we consider the cards to involve a country on the front side and 
its capital on the back.

We consider the -a priori- familiarity of the users to the capital to be in 
direct relation with the difficulty of concerning card.

This familiarity is considered to be proportional to the exposure of the users 
to the capitals in the news. Since our pool of subjects is entirely Japanese,
we rank the cards with respect to the number of Japanese Google news search results.

Please see [1] for achieving number of search results in Python. 

We organize the input file such that it includes the following columns, 
 col1: country in katakana 
 col2: capital in katakana 
 col3: country in English 
 col4: capital in English 
 col5: number of search results for country 
 col6: number of search results for capital

So as to achieve a desired level of relative difficulty, we adopt an approach based on 
Rank Bi-serial Correlation (RBSC). 

For a simple example on RBSC, please see rbsc_simple.py under this repository.

For further details on the algorithm, please refer to [2].


**References**
[1] https://github.com/anthonyhseb/googlesearch

[2] Zeynep Yücel, Parisa Supitayakul, Akito Monden, Pattara Leelaprute
An algorithm for automatic collation of vocabulary decks based on word frequency
IEICE Transactions on Information and Systems, 2020 (in press)



"""

import numpy as np
from importlib import reload

# The file preferences.py describes the hyper-parameters
import preferences
reload(preferences)

def get_rbsc(deck_E, deck_H):
    """
    The input of this function is arranged such that first input (E) is easier 
    than the second input (H), i.e. first input has higher ranks on the average 
    than second input.
    
    This is relevant to understand what is 'favoring' evidence and what is 
    'unfavoring' evidence.
    """
    rho = 0 # rho is RBSC coefficient
    favor, unfavor = 0, 0
    for i in deck_E:
        for j in deck_H:
            if int(i[2]) > int(j[2]):
                favor += 1
            else:
                unfavor += 1
    rho = (favor - unfavor) / (favor + unfavor)
            
    return rho


def init_decks(all_list):
    """
    Get 2*DECK_SIZE unique random indices. The range of indices is 
    [0, n_tot_cards-1]
    
    We will put the cards in the first half of this array to one deck, and the 
    second half to another deck (deck1 and deck2). That is, deck1 and deck2 are 
    initialized with arbitrary cards.
        
    Then, we compute median ranks of the decks, and set deck_E to the 
    easier one (i.e. the one with lower ranks) and deck_H to the harder one 
    (i.e. the one with lower ranks) of this pair.
    """

    random_indices = []
    while len(random_indices) < 2*preferences.DECK_SIZE:
        j = np.random.randint( len(all_list) )
        if j not in random_indices:
            random_indices.append(j)
    
    deck1_ind = random_indices[0:preferences.DECK_SIZE]
    deck2_ind = random_indices[preferences.DECK_SIZE:]
    
    deck1 = all_list[deck1_ind]
    deck2 = all_list[deck2_ind]
    
    """
    Here, We switch from (deck1, deck2) to (deck_E, deck_H).
    """
    rank_median_1 =  np.median([int(k[2]) for k in deck1 ])
    rank_median_2 =  np.median([int(k[2]) for k in deck2 ])
    
    if rank_median_1 > rank_median_2:   
        deck_E, deck_H = deck1, deck2
        deck_E_ind, deck_H_ind = deck1_ind, deck2_ind
        rank_median_E, rank_median_H = rank_median_1, rank_median_2
    else:
        deck_E, deck_H = deck2, deck1
        deck_E_ind, deck_H_ind = deck2_ind, deck1_ind 
        rank_median_E, rank_median_H = rank_median_2, rank_median_1
    
    del deck1, deck2, deck1_ind, deck2_ind, rank_median_1, rank_median_2
    
    return deck_E, deck_H, deck_E_ind, deck_H_ind, rank_median_E, rank_median_H

def pick_card_to_add(deck_E_ind, deck_H_ind, rank_median_X, all_list, easy_or_hard):
    """
    This function picks a card from among all the cards to add to a deck. 
    Specifically, it returns the index of the card rather than the card 
    (i.e. word) itself.
    
    The picked card has to be:
        new (not already picked for the other decks)
        easier/harder as desired (the input key is easy_or_hard)
        picked in less than MAX_EPOCH steps (otherwise we return -1 as index)
        
    Sometimes, the algorithm gets stuck since MAX_EPOCH is reached, and no card 
    can be found, no matter which one is picked.
    
    To avoid such cases, we randomly modify the deck in a small portion of the 
    cases, and proceed. This helps to avoid infinite loops. Sometimes, we do not 
    move in the desired direction but we at least get out of the local minima. 
    """
        
    rand_ind_to_add_X = -1
    epoch_add = 0
    while True:
        epoch_add += 1
        rand_ind_to_add_X = np.random.randint( len(all_list) )
        
        if easy_or_hard == 'easy':
            # The desired card to add is an easy card
            if \
            epoch_add < preferences.MAX_EPOCH and \
            (\
             rand_ind_to_add_X not in deck_E_ind and \
             rand_ind_to_add_X not in deck_H_ind and \
             (int(all_list[rand_ind_to_add_X][2]) > rank_median_X)\
             ): # Here is where we check whether it is easy (rank is higher than median rank of the deck)
                break
        elif easy_or_hard == 'hard': # The desired card to add is a hard card
            if \
            epoch_add < preferences.MAX_EPOCH and \
            (\
             rand_ind_to_add_X not in deck_E_ind and \
             rand_ind_to_add_X not in deck_H_ind and \
             (int(all_list[rand_ind_to_add_X][2]) < rank_median_X)\
             ): # Were is where we check whether is hard (rank is lower than median rank of the deck)
                break      
        else:
            print('Desired card difficulty is not recognized. Enter either easy or hard')
            
        if epoch_add >= preferences.MAX_EPOCH:
            if np.sign( np.random.uniform(0, 1) - preferences.RANDOM_MODIFICATION_THRESHOLD ) > 0:
                """
                Return a random card index, even if it does not satisfy the condition 
                (of being easy or hard as desired)
                
                We do this to avoid local minimas. However, the index still has 
                to unique (not already in the decks).
                """
                while True:
                    rand_ind_to_add_X = np.random.randint( len(all_list) )
                    if \
                    (\
                     rand_ind_to_add_X not in deck_E_ind and \
                     rand_ind_to_add_X not in deck_H_ind):
                        break
                        
                    
                break
                
            rand_ind_to_add_X = -1
            break
        
    return rand_ind_to_add_X, epoch_add
                
     
def pick_card_to_rem(deck_X_ind, rank_median_X, easy_or_hard):
    """
    This function picks a card to remove from a deck.
    
    The picked card has to be:
        easier/harder as desired (the input key is easy_or_hard)
        picked in less than MAX_EPOCH steps (otherwise return -1 as index)
        
    Usually MAX_EPOCH is never a problem here.
    """
        
    rand_ind_to_rem_X = -1
    epoch_rem = 0
    while True:
        rand_ind_to_rem_X = deck_X_ind[ np.random.randint(preferences.DECK_SIZE) ]
        
        if easy_or_hard == 'easy':
            # The desired card to remove is an easy card
            if \
            epoch_rem < preferences.MAX_EPOCH and \
            int(all_list[rand_ind_to_rem_X][2]) > rank_median_X:
                # Here is where we check whether is easy, rank is higher than median rank of the deck
                break
        elif easy_or_hard == 'hard':
            # The desired card to remove is a hard card
            if \
            epoch_rem < preferences.MAX_EPOCH and \
            int(all_list[rand_ind_to_rem_X][2]) < rank_median_X: 
                # Here is where we check whether is hard, rank is lower than median rank of the deck
                break
        else:
            print('Desired card difficulty is not recognized. Enter either easy or hard')
        
        if epoch_rem >= preferences.MAX_EPOCH:
            if np.sign( np.random.uniform(0, 1) - preferences.RANDOM_MODIFICATION_THRESHOLD ) > 0:
                """
                Return a random card index, even if it does not satisfy the 
                condition (of being easy or hard as desired)
                
                I do this to avoid local minimas. Here there is no other 
                condition.
                """
                break            
            rand_ind_to_rem_X = -1
            break
                
    return rand_ind_to_rem_X, epoch_rem

                

def update_decks(deck_E, deck_H, \
                 deck_E_ind, deck_H_ind, \
                 rank_median_E, rank_median_H):
 
    """
    Compute RBSC coefficient rho and update the decks such that 
    RHO_STAR - EPSILON < rho < RHO_STAR + EPSILON
    """
    rho = get_rbsc(deck_E, deck_H)
    
    while not ( (preferences.RHO_STAR - preferences.EPSILON < rho)  and (rho < preferences.RHO_STAR + preferences.EPSILON) ) :
        rho_old = rho
        if rho <= preferences.RHO_STAR - preferences.EPSILON :  
            
            """
            If rho is too low, increase it by:
                Adding an easy card (with high rank) to E 
                Removing a hard card (with low rank) from E
                Adding a hard card (with low rank) to H 
                Removing an easy card (with high rank) from H
            """
            
            # add easy card to E and remove hard card from E
            rand_ind_to_add_E, epoch_add = pick_card_to_add(deck_E_ind, \
                                                            deck_H_ind, \
                                                            rank_median_E, \
                                                            all_list, 'easy')
            rand_ind_to_rem_E, epoch_rem = pick_card_to_rem(deck_E_ind, \
                                                            rank_median_E, 'hard')             
            
            # add hard card to H and remove easy card from H
            rand_ind_to_add_H, epoch_add = pick_card_to_add(deck_E_ind, \
                                                            deck_H_ind, \
                                                            rank_median_H, \
                                                            all_list, 'hard')
            rand_ind_to_rem_H, epoch_rem = pick_card_to_rem(deck_H_ind, \
                                                            rank_median_H, 'easy')
                        
        elif rho >= preferences.RHO_STAR + preferences.EPSILON : 
            """
            If rho is too high, decrease it by:
                Adding a hard card (with low rank) to E 
                Removing an easy card (with high rank) from E
                Adding an easy card (with high rank) to H 
                Removing a hard card (with low rank) from H
            """
          
            # add hard card to E and remove easy card from E
            rand_ind_to_add_E, epoch_add = pick_card_to_add(deck_E_ind, \
                                                            deck_H_ind, \
                                                            rank_median_E, \
                                                            all_list, 'hard')
            rand_ind_to_rem_E, epoch_rem = pick_card_to_rem(deck_E_ind, \
                                                            rank_median_E, 'easy')              
            
            # add easy card to H and remove hard card from H
            rand_ind_to_add_H, epoch_add = pick_card_to_add(deck_E_ind, \
                                                            deck_H_ind, \
                                                            rank_median_H, \
                                                            all_list, 'easy')
            rand_ind_to_rem_H, epoch_rem = pick_card_to_rem(deck_H_ind, \
                                                            rank_median_H, 'hard')
                
        
        """
        The above gives us the indices of the cards to be added and removed. 
        
        Below, we actually add and remove those cards and update deck parameters.
        """
        
        if rand_ind_to_add_E > -1 and rand_ind_to_rem_E > -1 and \
        rand_ind_to_add_H > -1 and rand_ind_to_rem_H > -1:
            deck_E_ind.remove(rand_ind_to_rem_E)
            deck_E_ind.append(rand_ind_to_add_E)
            deck_H_ind.remove(rand_ind_to_rem_H)
            deck_H_ind.append(rand_ind_to_add_H)
        
        deck_E = all_list[deck_E_ind]
        deck_H = all_list[deck_H_ind]
        
        rank_median_E = int ( np.median([int(k[2]) for k in deck_E ]) )
        rank_median_H = int ( np.median([int(k[2]) for k in deck_H ]) )
                
        rho = get_rbsc(deck_E, deck_H)
        
        #print('Rho Before\t {}\t After\t {}'.format(rho_old, rho))
    return rho, deck_E, deck_H
        
if __name__ == "__main__":

    fname = preferences.SOURCE_FILE_NAME
    
    all_list = np.loadtxt(fname,\
                           delimiter='\t', usecols=(0,1,5,2,3), \
                           skiprows=8,\
                           dtype=np.str  
                           )
    
    deck_E, deck_H, deck_E_ind, deck_H_ind, rank_median_E, rank_median_H = \
    init_decks(all_list)
    
    rho, deck_E, deck_H = \
    update_decks(deck_E, deck_H, deck_E_ind, deck_H_ind, rank_median_E, rank_median_H)
    
    print('deck_E\n {}'.format(deck_E))
    print('deck_H\n {}'.format(deck_H))
    print('Rho = {0:.4f}'.format(rho))
        
