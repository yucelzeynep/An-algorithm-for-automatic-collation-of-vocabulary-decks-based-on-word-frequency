#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 08:42:35 2018

@author: zeynep
"""

import numpy as np


def get_vocab_data(fname):
    lines = [line.rstrip('\n') for line in open(fname)]
    
    out_data = {'english':[],\
                'japanese':[], \
                'freq':[]}
    
    for line in lines:        
        cells = line.split('\t')        
        out_data['english'].append(cells[0])
        out_data['japanese'].append(cells[1])
        out_data['freq'].append(int ( cells[2]) )
           
    return out_data

def get_rbsc(data1, data2, key):
    
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
        print('{}\t{}'.format(fname, len(temp['english'])))
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