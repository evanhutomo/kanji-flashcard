#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import random
from collections import Counter
import json


# function buat ngilangin u character di dictionary
def encode_dict(d, codec='utf8'):
    """this function basically get rid the 'u' for unicode on the key of the dictionary"""
    ks = d.keys()
    for k in ks:
        val = d.pop(k)
        if isinstance(val, unicode):
            val = val.encode(codec)
        elif isinstance(val, dict):
            val = encode_dict(val, codec)
        if isinstance(k, unicode):
            k = k.encode(codec)
        d[k] = val
    return d

# Fetch JSON global
def jsonparse(path):
    with open(path) as json_data:
        data = json.load(json_data)
        return data

# ------ KANJI's data ------
def reload_data():
    global dict_kanjis
    global qlist
    global checklist
    dict_kanjis = encode_dict(jsonparse('../datas/kanjis.json'))
    for key, value in dict_kanjis.items():
        qlist.append(key)
        checklist.append(int(key))
# ------ KANJI's data ------

# GLOBAL
dict_kanjis = encode_dict(jsonparse('../datas/kanjis.json'))
qlist = []
checklist = []
# GLOBAL

dict_menu = encode_dict(jsonparse('../datas/util.json'))
# ----------------------------------------------------------------------------------------------------------------------

def test():
    path = "../datas/kanjis.json"
    print(os.path.isfile(path))

def menu():
    reload_data()
    print(dict_menu["banner"]["3"] + "\n" + \
          dict_menu["banner"]["4"] + "\n" + \
          dict_menu["menu"]["option_menu"][0] + "\n" + \
          dict_menu["menu"]["option_menu"][1] + "\n" + \
          dict_menu["menu"]["option_menu"][2] + "\n"
          )
    input_option = raw_input("> : ").lower()
    if input_option == 'q':
        quit()
    elif str(input_option) == '1':
        menu_data()
    elif str(input_option) == '2':
        qlist = []
        for key, value in dict_kanjis.items():
            qlist.append(key)
        amt_q = raw_input(dict_menu["question"]["quiz"][0] % len(qlist)).lower().strip()
        if amt_q == 'q': quit()
        while amt_q.isdigit() == False:
            print(dict_menu["response"]["quiz"][0])
            amt_q = raw_input(dict_menu["question"]["quiz"][0] % len(qlist)).lower().strip()
        amt_q = int(amt_q)
        while amt_q > len(qlist):
            amt_q = int(raw_input(dict_menu["response"]["quiz"][1] % len(qlist)).lower().strip())
        main2(amt_q)
    elif str(input_option) == '3':
        search_page('search')
    else:
        quit()

def menu_data():
    print(dict_menu["menu"]["input_data"][0])
    print(dict_menu["menu"]["input_data"][1])
    print(dict_menu["menu"]["input_data"][2])

    input_option = raw_input("> : ").lower()
    if input_option == "q":
        quit()
    elif input_option == "1":
        insert_data()
    elif input_option == "2":
        update_data()
    elif input_option == "3":
        delete_data()
    else:
        quit()

def search_page(type):
    if type == 'update':
        _upt = 'Update'
    elif type == 'search':
        _upt = 'Search'
    elif type == 'delete':
        _upt = 'Delete'

    type_name = ["ROMAJI", "KANJI", "ENGLISH"]
    search_type_input = raw_input(_upt + " by (1)"+ type_name[0] +", (2)"+ type_name[1] +", (3)"+ type_name[2] + " : ").lower().strip()
    if search_type_input == "1":
        _abrv = "rm"
        _tpname = type_name[0]
    elif search_type_input == "2":
        _abrv = "kj"
        _tpname = type_name[1]
    elif search_type_input == "3":
        _abrv = "en"
        _tpname = type_name[2]

    if search_type_input == "1" or search_type_input == "2" or search_type_input == "3":
        search_input = raw_input("Search by "+ _tpname +" : ").lower().strip()
        flag = 0
        for chk in qlist:
            if dict_kanjis[chk][_abrv] == search_input:
                flag = 0
                id_word = chk
                break
            else:
                flag = 1

        if flag == 1 and type == "search":
            print(_tpname + " \'%s\' NOT FOUND!\n"
                  "Want to input it?(y)(n) " % search_input)
            input_option = raw_input("> : ").lower().strip()
            if input_option == 'y':
                insert_data()
            else:
                recentpos("m")
        else:
            print(_tpname + " \'%s\' FOUND!" % search_input)
            print dict_menu["banner"]["6"]
            # UPDATE
            if type == 'update':
                for k in dict_kanjis[id_word]:
                    if k != "kanji_part":
                        print(k + " : " + dict_kanjis[id_word][k])

                print dict_menu["banner"]["7"]
                kj_input = raw_input(dict_menu["question"]["input_data"][1]).lower().strip()
                if kj_input == 'q': quit()
                kj_spc_input = raw_input(dict_menu["question"]["input_data"][2]).lower().strip()
                if kj_spc_input == 'q': quit()
                rm_input = raw_input(dict_menu["question"]["input_data"][3]).lower().strip()
                if rm_input == 'q': quit()
                en_input = raw_input(dict_menu["question"]["input_data"][4]).lower().strip()
                if en_input == 'q': quit()
                meaning_input = raw_input(dict_menu["question"]["input_data"][5]).lower().strip()
                if meaning_input == 'q': quit()
                kj_spc_input = kj_spc_input.split()

                # forming kanji param
                print dict_menu["banner"]["2"]
                kanji_hatsuon = {}
                for i in kj_spc_input:
                    kanji_hatsuon[i] = raw_input("%s : " % i).lower().strip()
                    if kanji_hatsuon[i] == 'q': quit()

                new_dict_input = {
                    str(id_word): {
                        'kj': kj_input,
                        'rm': rm_input,
                        'en': en_input,
                        'meaning': meaning_input,
                        "kanji_part": kanji_hatsuon
                    }
                }

                with open('../datas/kanjis.json') as f:
                    datajson = json.load(f)
                datajson.update(new_dict_input)
                with open('../datas/kanjis.json', 'w') as f:
                    json.dump(datajson, f, sort_keys=True, indent=2)
                print dict_menu["banner"]["6"]
                recentpos("m")
            elif type == 'delete':
                for k in dict_kanjis[id_word]:
                    if k != "kanji_part":
                        print(k + " : " + dict_kanjis[id_word][k])

                print(dict_menu["banner"]["6"])
                _tempname = dict_kanjis[id_word]["kj"]
                del_input = raw_input(dict_menu["question"]["delete_data"][0] % _tempname)
                if del_input == "y":
                    for i in qlist:
                        dict_kanjis.pop(id_word)
                        break
                    print(dict_menu["banner"]["9"])
                    open("../datas/kanjis.json", "w").write(
                        json.dumps(dict_kanjis, sort_keys=True, indent=4, separators=(',', ': '))
                    )
                if del_input == "n":
                    recentpos("m")
            elif type == 'search':
                recentpos("m")
    else:
        recentpos("m")

def update_data():
    print(dict_menu["menu"]["input_data"][1])
    search_page('update')

def delete_data():
    print(dict_menu["menu"]["input_data"][2])
    search_page('delete')

def recentpos(param):
    if param == "m":
        menu()
    elif param == "q":
        quit()


def insert_data():
    print(dict_menu["menu"]["input_data"][0])

    kj_input = raw_input(dict_menu["question"]["input_data"][1]).lower().strip()
    if kj_input == 'q':quit()
    # check the existence of inputed kanji
    list_existence = []
    for chk in qlist:
        if dict_kanjis[chk]['kj'] == kj_input:
            list_existence.append('T')
        else:
            list_existence.append('F')
    if 'T' in list_existence:
        print("Data %s already EXIST!" % kj_input)
        insert_data()
    else:
        print("Data is NEW!")
    lastid = int(max(checklist)) + 1  # add 1 on last id, if 言語 are valid unique

    kj_spc_input = raw_input(dict_menu["question"]["input_data"][2]).lower().strip()
    if kj_spc_input == 'q': quit()
    rm_input = raw_input(dict_menu["question"]["input_data"][3]).lower().strip()
    if rm_input == 'q': quit()
    en_input = raw_input(dict_menu["question"]["input_data"][4]).lower().strip()
    if en_input == 'q': quit()
    meaning_input = raw_input(dict_menu["question"]["input_data"][5]).lower().strip()
    if meaning_input == 'q': quit()
    kj_spc_input = kj_spc_input.split()

    # forming kanji param
    print dict_menu["banner"]["2"]
    kanji_hatsuon = {}
    for i in kj_spc_input:
        kanji_hatsuon[i] = raw_input("%s : " % i).lower().strip()
        if kanji_hatsuon[i] == 'q': quit()

    new_dict_input =    {
            str(lastid): {
                'kj': kj_input,
                'rm': rm_input,
                'en': en_input,
                'meaning': meaning_input,
                "kanji_part": kanji_hatsuon
            }
        }

    with open('../datas/kanjis.json') as f:
        datajson = json.load(f)
    datajson.update(new_dict_input)
    with open('../datas/kanjis.json', 'w') as f:
        json.dump(datajson, f, sort_keys=True, indent=2)
    print dict_menu["banner"]["1"]
    recentpos("m")

def get_answer(ans, idq, type):
    qlist = []
    for key, value in dict_kanjis.items():
        qlist.append(key)

    sol = dict_kanjis[idq]

    if type == 'rm':
        if sol['rm'] == ans:
            print "CORRECT, " + sol['rm']
        else:
            print "WRONG, it's " + sol['rm']
    elif type == 'en':
        if sol['en'] == ans:
            print "CORRECT, " + sol['en']
        else:
            print "WRONG, it's " + sol['en']

def main2(amt_q):
    qlist = []

    for key, value in dict_kanjis.items():
        qlist.append(key)

    rand_qlist = random.sample(qlist, amt_q)
    # rand_qlist = random.sample(qlist, len(qlist)) # we use random question list for the multiple question

    # get the list of strings
    score = []

    for idq in rand_qlist:
        print(dict_menu["banner"]["6"])
        # for pick one random question
        question = dict_kanjis[idq]
        # print(dict.keys())
        rm_input = raw_input("ROMAJI of %s" % str(question['kj']) + " is : ").lower().strip()
        if rm_input == 'q':break
        get_answer(rm_input, idq, 'rm')

        en_input = raw_input("ENGLISH of %s" % str(question['kj']) + " is : ").lower().strip()
        if en_input == 'q': break
        get_answer(rm_input, idq, 'en')

        if rm_input != 'q' and en_input != 'q':
            if question['rm'] == rm_input and \
               question['en'] == en_input:
                score.append('T')
            else:
                score.append('F')
        else:
            break
    print(dict_menu["banner"]["6"])

    # SCORING
    false_score = 0
    true_score  = 0
    for k, v in Counter(score).items():
        if k == 'T':
            true_score = v
        elif k == 'F':
            false_score = v

    print('TRUE  : %d' % true_score)
    print('FALSE : %d' % false_score)
    recentpos("m")

if __name__=="__main__":
    reload_data()
    print(dict_menu["banner"]["5"])
    recentpos("m")

    # readfile()
    # jsonwrite()

    # for key in dict.iterkeys():
    #     print key
    # for value in dict.itervalues():
    #     print value

    # write to JSON
    # a_dict = {'new_key':'new_value',
    #           'root':[
    #               1,2,3,4,5
    #           ],
    #           'aaa':{
    #               'bb':'bb value',
    #               'cc':'cc value'
    #           }
    #           }
    #
    # with open('test.json') as f:
    #     data = json.load(f)
    #
    # data.update(a_dict)
    #
    # with open('test.json', 'w') as f:
    #     json.dump(data, f)



