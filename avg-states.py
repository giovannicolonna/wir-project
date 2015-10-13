__author__ = 'Federica'

import json
import re
import os
import shutil

INPUTFILE = "top-states-"  # si puo' scegliere tra top-us e top250

if os.path.exists("states-tsv"):
    shutil.rmtree("states-tsv")
os.mkdir("states-tsv")

states = []
with open('states.tsv') as states_file:
    for line in states_file:
        states.append(line.split('\t')[0])

for state in states:
    input_json = open(INPUTFILE+state+".json", 'r')
    beers_json = input_json.read()
    input_json.close()

    # lista di birre. Ogni birra e' un dict con i vari campi, tra cui review che e' una lista
    beers = json.loads(beers_json)

    output_file = open("states-tsv/top-"+state+"-vectorialized.tsv", 'w')

    for beer in beers:
        tot_rev = len(beer['reviews'])
        beer_name = str(beer['name'].encode('utf-8'))
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

        avg_look /= tot_rev
        avg_smell /= tot_rev
        avg_taste /= tot_rev
        avg_feel /= tot_rev
        avg_overall /= tot_rev

        output_file.write(beer_name+'\t')

        output_file.write(str(avg_look)+'\t')
        output_file.write(str(avg_smell)+'\t')
        output_file.write(str(avg_taste)+'\t')
        output_file.write(str(avg_feel)+'\t')
        output_file.write(str(avg_overall)+'\n')

    output_file.close()

