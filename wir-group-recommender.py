__author__ = 'Federica'

import json
import random
import sys
import os
import math
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
                out = random.randint(0, g_size-1)
                group[out] = user

    return group


def dot_product(beer, user):
    s = 0.0
    for b in beer:
        for u in user:
            if b == u:
                s += beer[b]*user[u]
    return s


GROUP_SIZE = 5
PATH = "Recommendations"

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


def of_sum(bv, g):
    sum = []
    for b in bv:
        s = 0.0
        for user in g:
            s += dot_product(b, user)
        sum.append((b['name'], s))

    return sorted(sum, key=lambda x: x[1], reverse=True)[:10]


def of_min(bv, g):
    mins = []
    for b in bv:
        min = sys.maxint
        min_beer = ''
        for user in g:
            x = dot_product(b, user)
            if x < min:
                min = x
                min_beer = b['name']
        mins.append((min_beer, min))

    return sorted(mins, key=lambda y: y[1], reverse=True)[:10]


def of_fair(bv, g, k=0.5):
    fair = []
    for b in bv:
        sums = []
        for user in g:
            sums.append(dot_product(b, user))

        std = 0.0
        for s in sums:
            std += s*s
        std /= len(sums)
        std = math.sqrt(std)

        s = 0.0
        for i in sums:
            s += i
        fair.append((b['name'], s+k*std))

    return sorted(fair, key=lambda y: y[1], reverse=True)[:10]


def of_mix(bv, g, k=0.5):
    mix = []
    for b in bv:
        sum = 0.0
        min = sys.maxint
        for user in g:
            x = dot_product(b, user)
            sum += x
            if x < min:
                min = x
        mix.append((b['name'], sum+k*min))

    return sorted(mix, key=lambda y: y[1], reverse=True)[:10]


if not os.path.exists(PATH):
    os.mkdir(PATH)

for repetitions in range(0, 100):

    output = open(PATH+"/output_group"+str(repetitions)+".txt", 'w')

    group = sampling(GROUP_SIZE)

    sum = of_sum(beers_vector, group)
    min = of_min(beers_vector, group)
    fair = of_fair(beers_vector, group, 0.5)
    mix = of_mix(beers_vector, group, 0.5)

    output.write("---------- SUM ----------\n")
    for beer in sum:
        output.write(str(beer)+'\n')
    output.write('\n\n')

    output.write("---------- MIN ----------\n")
    for beer in min:
        output.write(str(beer)+'\n')
    output.write('\n\n')

    output.write("---------- FAIR ---------\n")
    for beer in fair:
        output.write(str(beer)+'\n')
    output.write('\n\n')

    output.write("---------- MIX ----------\n")
    for beer in mix:
        output.write(str(beer)+'\n')
    output.close()

    print repetitions



