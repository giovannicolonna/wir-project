__author__ = 'Federica'

import json
from collections import OrderedDict, defaultdict


def read_json(json):
    with open(json) as data_file:
        data = json.load(data_file)
    return data


def create_db(data, db):
    for beer in data:

        name = beer['name']
        style = beer['style']
        abv = beer['abv']

        for review in beer['reviews']:

            user_ID = review['reviewer']
            look = review['look']
            smell = review['smell']
            taste = review['taste']
            feel = review['feel']
            overall = review['overall']

            reviewed_beer = OrderedDict()
            reviewed_beer['beer_name'] = name
            reviewed_beer['style'] = style
            reviewed_beer['abv'] = abv
            reviewed_beer['look'] = look
            reviewed_beer['smell'] = smell
            reviewed_beer['taste'] = taste
            reviewed_beer['feel'] = feel
            reviewed_beer['overall'] = overall

            db['user_ID'] = user_ID
            if len(db[user_ID]) == 0:
                db[user_ID] = []
            db[user_ID].append(reviewed_beer)


users_db = defaultdict(lambda: list(OrderedDict()))

print "Retrieving users from TOP-250 beers"
with open("top-250.json") as data_file:
    beers1 = json.load(data_file)
    create_db(beers1, users_db)

print "Retrieving users from TOP-US beers"
with open("top-us.json") as data_file:
    beers2 = json.load(data_file)
    create_db(beers2, users_db)

print "Retrieving users from TOP-STATES beers:"
states = open('states.tsv', 'r')
for line in states:
    sign = line.split('\t')[0].strip()
    print "\t"+line.split('\t')[1].strip()

    with open("top-states-"+sign+".json") as data_file:
        beers3 = json.load(data_file)
        create_db(beers3, users_db)

states.close()


output = open("users.json", 'w')
output.write(json.dumps(users_db, indent=4))
output.close()



