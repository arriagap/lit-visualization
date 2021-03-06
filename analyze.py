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




def get_top_words(word_freq, word_locs, numwords = 200):
    sorted_freqs = sorted(word_freq, key = lambda tup:tup[1])
    truncated_freqs = sorted_freqs[-numwords:]
    truncated_word_locs = {}
    for freq in sorted_freqs:
        word = freq[0]
        truncated_word_locs[word] = word_locs[word]
    return truncated_freqs, truncated_word_locs




def mark_words_sets(text, getset = 'synset'):
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




def mark_words_individual(text):
    text = n.array(text)
    marks = n.zeros(len(text), dtype = int)
    null_words = n.where(text == '')

#    word_freq = {'-1': len(null_words)}
    word_freq = [('-1', len(null_words))]
    word_locs = {'-1': null_words}
    words_left = text[n.where(text != '')]
    while len(words_left) > 0:
        curr_word = words_left[0]
        wh = n.where(text == curr_word)
        word_freq.append((curr_word, len(wh[0])))
#        word_freq[curr_word] = len(wh[0])
        word_locs[curr_word] = wh
        words_left = words_left[n.where(words_left != curr_word)]
    return word_freq, word_locs
        





def mark_frequency(text):
    dic = PyDictionary()
    word_dic = {}
    maxkey = 0
    keys = []
    for i, word in enumerate(text):
        if word != '':
            if word in keys:
                word_dic[word] += 1
            else:
                word_dic[word] = 1
                keys = word_dic.keys()
    return word_dic

                    



def test_text():
    f = open('ivans.txt', 'rb')
    a = f.readlines()[0:200]
    a = split_text(a)
    a = remove_stopwords(a)
    return a

