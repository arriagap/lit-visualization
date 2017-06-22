from parser import *
from nltk.corpus import wordnet as wn
from PyDictionary import PyDictionary
import numpy as n


def get_lemmaset(word, recursive = True):
    ### Doesn't seem to be optimal for automation
    syn_list = wn.synsets(word)
    #Lemmas are like associated words?
    lemmas = [word]
    for syn in syn_list:
        lemmas += syn.lemma_names()
        lemmas.append(syn.name().split('.')[0])
    lemmas = set(lemmas)

    recursive = [word]
    for lemma in lemmas:
        syn_list = wn.synsets(lemma)
        for syn in syn_list:
            recursive.append(syn.name().split('.')[0])
            recursive += syn.lemma_names()
    recursive = set(recursive)
    if recursive is True:
        return list(recursive)
    else:
        return list(lemmas)


def get_base(word, dic):
    morph = wn.morphy(word.lower())
    if morph is not None:
        synonyms = dic.synonym(morph)
        return synonyms.append(morph)
    else:
        return [word]

def get_synset(word, dic):
    synsets = wn.synsets(word)
    syn_list = [word]
    for syn in synsets:
        syn_name = syn.name().split('.')[0]
        if syn_name not in syn_list: 
            syn_list.append(syn_name)
            dic_syns = dic.synonym(syn_name)
            for dic_syn in dic_syns:
                if dic_syn not in syn_list:
                    syn_list.append(dic_syn)
    return syn_list

def get_recursive_synset(word, dic):
    syn_list = get_synset(word, dic)
    total_synlist = []
    for syn in syn_list:
        total_synlist += get_synset(syn, dic)
    return list(set(total_synlist))


def main_key(word_dic, marks, text):
    main_key_list = [word_dic[str(i)][0] for i in marks]
    main_key_list = [x for x in main_key_list if x[0] != '']
    # make it so that it counts the number of time
    return zip(main_key_list, text)


def mark_words(text, getset = 'synset'):
    dic = PyDictionary()
    marks = n.zeros(len(text), dtype = int)
    word_dic = {'-1': ['']}
    maxkey = 0
    for i, word in enumerate(text):
        if word == '':
            marks[i] = -1
        else:
            key = 0
            found = 0
            if getset == 'synset':
                synset = get_synset(word, dic)
            elif getset == 'lemmas':
                synset = get_lemmaset(word)
            while found == 0 and key < maxkey: 
                if word in word_dic[str(key)]:
                    marks[i] = key
                    found = 1
                else:
                    syn_ind = 0 
                    while found == 0 and syn_ind < len(synset):
                        if synset[syn_ind] in word_dic[str(key)]:
                            marks[i] = key
                            found = 1
                            word_dic[str(key)].append(word)
                        else:
                            syn_ind += 1
                    key += 1
            if found == 0:
                if getset == 'synset':
                    newsyns = get_synset(word, dic)
                elif getset == 'lemmas':
                    newsyns = get_lemmaset(word)
                word_dic[str(maxkey)] = newsyns
                marks[i] = int(maxkey)
                maxkey += 1
    return word_dic, marks
                    



def test_text():
    f = open('byron.txt', 'rb')
    a = f.readlines()
    a = split_text(a)
    a = remove_stopwords(a)
    return a

