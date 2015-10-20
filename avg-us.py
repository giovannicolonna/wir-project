__author__ = 'Federica'

import json
import re
import sys
import os
import shutil

# INPUTFILE can take values "top-250", "top-us", "top-states"
INPUTFILE = sys.argv[1]

if INPUTFILE == "top-states":
    if os.path.exists("states-tsv"):
        shutil.rmtree("states-tsv")
    os.mkdir("states-tsv")

    states = []
    with open('states.tsv') as states_file:
        for line in states_file:
            states.append(line.split('\t')[0])

    for state in states:
        input_json = open(INPUTFILE+"-"+state+".json", 'r')
        beers_json = input_json.read()
        input_json.close()

    # List of beers. Each beer is a dict. The 'review' field is a list as well
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

else:
    input_json = open(INPUTFILE+".json", 'r')
    beers_json = input_json.read()
    input_json.close()

# List of beers. Each beer is a dict. The 'review' field is a list as well
    beers = json.loads(beers_json)

    output_file = open(INPUTFILE+"-vectorialized.tsv", 'w')

    for beer in beers:
        tot_rev = len(beer['reviews'])
        beer_name = str(beer['name'].encode('utf-8'))

        # avg_look = 0
        # avg_smell = 0
        # avg_taste = 0
        # avg_feel = 0
        # avg_overall = 0

    # weighted
        tot_weight = 0
        w_avg_look = 0
        w_avg_smell = 0
        w_avg_taste = 0
        w_avg_feel = 0
        w_avg_overall = 0
        position = str(beer['position'])

        for review in beer['reviews']:

            # avg_look += float(review['look'])
            # avg_smell += float(review['smell'])
            # avg_taste += float(review['taste'])
            # avg_feel += float(review['feel'])
            # avg_overall += float(review['overall'])

            weight = review['reviewerScore']
            weight = float(re.sub(",", "", weight))
            tot_weight += weight

            w_avg_look += float(review['look']) * weight
            w_avg_smell += float(review['smell']) * weight
            w_avg_taste += float(review['taste']) * weight
            w_avg_feel += float(review['feel']) * weight
            w_avg_overall += float(review['overall']) * weight

        # avg_look /= tot_rev
        # avg_smell /= tot_rev
        # avg_taste /= tot_rev
        # avg_feel /= tot_rev
        # avg_overall /= tot_rev

        w_avg_look /= tot_weight
        w_avg_smell /= tot_weight
        w_avg_taste /= tot_weight
        w_avg_feel /= tot_weight
        w_avg_overall /= tot_weight

        output_file.write(beer_name+'\t')

        # output_file.write(str(avg_look)+'\t')
        # output_file.write(str(avg_smell)+'\t')
        # output_file.write(str(avg_taste)+'\t')
        # output_file.write(str(avg_feel)+'\t')
        # output_file.write(str(avg_overall)+'\t')

    # print on file weighted characteristics
        output_file.write(str(w_avg_look)+'\t')
        output_file.write(str(w_avg_smell)+'\t')
        output_file.write(str(w_avg_taste)+'\t')
        output_file.write(str(w_avg_feel)+'\t')
        output_file.write(str(w_avg_overall)+'\t')

        output_file.write(str(position)+'\n')

    output_file.close()
