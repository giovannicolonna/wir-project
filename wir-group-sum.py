__author__ = 'Federica'

import json
import random


def reservoir_sampling(g_size=20):

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


GROUP_SIZE = 20

beers = []

with open("top-250.json") as data_file:
    beers = json.load(data_file)

# with open("top-us.json") as data_file:
#     beer_list = json.load(data_file)
#     dups = 0
#     flag = True
#     for b1 in beer_list:
#         for b2 in beers:
#             if b1['name'] == b2['name']:
#                 flag = False
#                 dups += 1
#                 break
#         if flag:
#             beers.append(b1)


dups = 0
states = open('states.tsv', 'r')
for line in states:
    sign = line.split('\t')[0].strip()

    with open("top-states-"+sign+".json") as data_file:
        beer_list = json.load(data_file)
        flag = True
        for b1 in beer_list:
            for b2 in beers:
                if b1['name'] == b2['name']:
                    flag = False
                    dups += 1
                    break
            if flag:
                beers.append(b1)

print len(beers)
print dups
