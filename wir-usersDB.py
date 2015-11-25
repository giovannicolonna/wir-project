__author__ = 'Federica'

import json
from collections import OrderedDict, defaultdict


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
            rate = review['rate']

            reviewed_beer = OrderedDict()
            reviewed_beer['beer_name'] = name
            reviewed_beer['style'] = style
            reviewed_beer['abv'] = abv
            reviewed_beer['rate'] = rate
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
with open("data/top-250.json") as data_file:
    beers1 = json.load(data_file)
    create_db(beers1, users_db)

print "Retrieving users from TOP-US beers"
with open("data/top-us.json") as data_file:
    beers2 = json.load(data_file)
    create_db(beers2, users_db)

print "Retrieving users from TOP-STATES beers:"
states = open('states.tsv', 'r')
for line in states:
    sign = line.split('\t')[0].strip()
    print "\t"+line.split('\t')[1].strip()

    with open("data/top-states-"+sign+".json") as data_file:
        beers3 = json.load(data_file)
        create_db(beers3, users_db)

states.close()

db = []
for k, v in users_db.iteritems():
    d = OrderedDict()
    rate = 0.0
    look = 0.0
    smell = 0.0
    taste = 0.0
    feel = 0.0
    overall = 0.0

    # avg = 0.0
    for rev in v:
        try:
            rate += float(rev['rate'])
            look += float(rev['look'])
            smell += float(rev['smell'])
            taste += float(rev['taste'])
            feel += float(rev['feel'])
            overall += float(rev['overall'])

        except TypeError:
            continue

    d['user_ID'] = k
    d['rate'] = rate/len(v)
    d['look'] = look/len(v)
    d['smell'] = smell/len(v)
    d['taste'] = taste/len(v)
    d['feel'] = feel/len(v)
    d['overall'] = overall/len(v)
    db.append(d)


output = open("users.json", 'w')
output.write(json.dumps(db, indent=4))
output.close()

