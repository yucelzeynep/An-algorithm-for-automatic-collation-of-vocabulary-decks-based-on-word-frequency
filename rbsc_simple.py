#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 08:42:35 2018

@author: zeynep

This function computes the Rank Bi-serial Correlation (RBSC) of two lists.

In this example, the lists contain 15 words each, all English and abstract.

The ranking variable is the number of occurrence of each word in Wiktionary 
word frequency lists.

"""

import numpy as np


def get_vocab_data(fname):
"""
This function reads the input lists into a dictionary variable.
"""
    lines = [line.rstrip('\n') for line in open(fname)]
    
    out_data = {'word':[],\
                'freq':[]}
    
    for line in lines:        
        cells = line.split('\t')        
        out_data['word'].append(cells[0])
        out_data['freq'].append(int ( cells[1]) )
           
    return out_data

def get_rbsc(data1, data2, key):
"""
This function computes RBSC coefficient based on Kerby's simple
difference formula. 
"""
    
    favor, unfavor = 0,0
    for d1 in data1[key]:
        for d2 in data2[key]:
            if int(d1) > int(d2):
                favor += 1
            else:
                unfavor += 1
            
    rbsc = (favor - unfavor) / (favor + unfavor)
    return rbsc
    


if __name__ == "__main__":
    
    fnames = ['deck_A.txt',\
              'deck_B.txt']
    
    vocab_data = []
    
    print('Number of data points:')
    for i, fname in enumerate(fnames):
        temp =  get_vocab_data(fname)
        print('{}\t{}'.format(fname, len(temp['word'])))
        vocab_data.append(temp) 

        
    for i, dataA in enumerate(vocab_data):
        for j, dataB in enumerate(vocab_data):
            if i < j: # so that we do every pair once 
                keys = dataA
                for key in keys:
                    if isinstance(dataA[key][0], int):
                        print('\nComputing RBSC based on {}...'.format(key))

                        rbsc = get_rbsc(dataA, dataB, key)
                        
                        print('RBSC = {:.3f}'.format(rbsc))
