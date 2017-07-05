import pickle
import re
import copy
import numpy as n

def split_text(txt, punctuation_file = 'filtering_files/punctuation.txt'):
    p_file = open(punctuation_file)
    p_list = p_file.readlines()
    for i in range(len(p_list)):
        # need to remove the returns from the list
        p_list[i] = re.sub('\n', '', p_list[i])
    new_txt = []
    for line in txt:
        newline = copy.deepcopy(line)
        if "'s" in newline:
            newline = re.sub("'s") 
        for p in p_list:
            if p in newline:

                if p == '?':
                    p = '\?'
                if p == '*':
                    p = '\*'
                newline = re.sub(p, '', newline)
        if '\n' in newline:
            newline = re.sub('\n', '', newline)
        new_txt += newline.split(' ') 
    new_txt = [a.upper() for a in new_txt if a != '']
    return new_txt




def remove_stopwords(txt, stop_words_file = 'filtering_files/stop_words_eng.txt'):
    stop_file = open(stop_words_file)
    stop_list = stop_file.readlines()
    for i in range(len(stop_list)):
        stop_list[i] = re.sub('\n', '', stop_list[i])
    stop_list = split_text(stop_list)
    for i, word in enumerate(txt):
        if word in stop_list:
            txt[i] = ''
    return txt
    

def get_synset(word):
    pass


def test():
    f = open('byron.txt', 'rb')
    a = f.readlines()
    a = split_text(a)
    a = remove_stopwords(a)
    return a

