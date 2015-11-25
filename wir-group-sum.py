__author__ = 'Federica'

import json
import random
from collections import OrderedDict


def sampling(g_size=20):

    with open("users.json") as data_file:
        input_users = json.load(data_file)

    group = []
    count = 0

    for user in input_users:
        count += 1
        if len(group) < g_size:
            group.append(user)
        else:
            if random.random() <= float(g_size)/count:
                out = random.randint(0, 19)
                group[out] = user

    return group


def dot_product(beer, user):
    s = 0.0
    for b in beer:
        for u in user:
            if b == u:
                s += beer[b]*user[u]
    return s


GROUP_SIZE = 20

beers = []

#  TOP-US beers are contained in TOP-250
with open("data/top-250.json") as data_file:
    beers = json.load(data_file)


dups = 0
states = open('states.tsv', 'r')
for line in states:
    sign = line.split('\t')[0].strip()

    with open("data/top-states-"+sign+".json") as data_file:
        beer_list = json.load(data_file)
        flag = True
        for b1 in beer_list:
            for b2 in beers:
                if b1['name'] == b2['name'] and b1['brewer'] == b2['brewer'] and b1['abv'] == b2['abv']:
                    flag = False
                    dups += 1
                    break
            if flag:
                beers.append(b1)

beers_vector = []
for beer in beers:

    birra = OrderedDict()

    tot_rev = len(beer['reviews'])
    birra['name'] = str(beer['name'].encode('utf-8'))
    birra['rate'] = float(beer['avg'])

    avg_look = 0
    avg_smell = 0
    avg_taste = 0
    avg_feel = 0
    avg_overall = 0

    for review in beer['reviews']:
        avg_look += float(review['look'])
        avg_smell += float(review['smell'])
        avg_taste += float(review['taste'])
        avg_feel += float(review['feel'])
        avg_overall += float(review['overall'])

    birra['look'] = avg_look / tot_rev
    birra['smell'] = avg_smell / tot_rev
    birra['taste'] = avg_taste / tot_rev
    birra['feel'] = avg_feel / tot_rev
    birra['overall'] = avg_overall / tot_rev

    beers_vector.append(birra)

output = open("sum_output2.txt", 'w')
for repetitions in range(0, 100):
    group = sampling(GROUP_SIZE)
    sum = []
    for beer in beers_vector:
        s = 0.0
        for user in group:
            s += dot_product(beer, user)
        sum.append((beer['name'], s))

    sum = sorted(sum, key=lambda x: x[1], reverse=True)[:10]
    for beer in sum:
        output.write(str(beer)+'\n')
    output.write('\n\n')
output.close()

